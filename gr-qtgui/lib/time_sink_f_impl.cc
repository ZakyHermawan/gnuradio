/* -*- c++ -*- */
/*
 * Copyright 2011-2013 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "time_sink_f_impl.h"
#include <gnuradio/io_signature.h>
#include <gnuradio/block_detail.h>
#include <gnuradio/buffer.h>
#include <string.h>
#include <volk/volk.h>
#include <gnuradio/fft/fft.h>
#include <qwt_symbol.h>

namespace gr {
  namespace qtgui {
    
    time_sink_f::sptr
    time_sink_f::make(int size, double samp_rate,
		      const std::string &name,
		      int nconnections,
		      QWidget *parent)
    {
      return gnuradio::get_initial_sptr
	(new time_sink_f_impl(size, samp_rate, name, nconnections, parent));
    }

    time_sink_f_impl::time_sink_f_impl(int size, double samp_rate,
				       const std::string &name,
				       int nconnections,
				       QWidget *parent)
      : sync_block("time_sink_f",
                   io_signature::make(nconnections, nconnections, sizeof(float)),
                   io_signature::make(0, 0, 0)),
	d_size(size), d_samp_rate(samp_rate), d_name(name),
	d_nconnections(nconnections), d_parent(parent)
    {
      d_main_gui = NULL;

      d_index = 0;

      for(int i = 0; i < d_nconnections; i++) {
	d_residbufs.push_back(fft::malloc_double(d_size));
	memset(d_residbufs[i], 0, d_size*sizeof(double));
      }

      // Set alignment properties for VOLK
      const int alignment_multiple =
	volk_get_alignment() / sizeof(float);
      set_alignment(std::max(1,alignment_multiple));

      d_tags = std::vector< std::vector<gr::tag_t> >(d_nconnections);

      initialize();

      d_size += 1;         // trick the next line into updating
      set_nsamps(size);
      set_trigger_mode(TRIG_MODE_AUTO, TRIG_SLOPE_POS, 0, 0, 0);
      d_initial_delay = d_trigger_delay;
    }

    time_sink_f_impl::~time_sink_f_impl()
    {
      if(!d_main_gui->isClosed())
        d_main_gui->close();

      // d_main_gui is a qwidget destroyed with its parent
      for(int i = 0; i < d_nconnections; i++) {
	fft::free(d_residbufs[i]);
      }
    }

    bool
    time_sink_f_impl::check_topology(int ninputs, int noutputs)
    {
      return ninputs == d_nconnections;
    }

    void
    time_sink_f_impl::initialize()
    {
      if(qApp != NULL) {
	d_qApplication = qApp;
      }
      else {
	int argc=0;
	char **argv = NULL;
	d_qApplication = new QApplication(argc, argv);
      }

      d_main_gui = new TimeDisplayForm(d_nconnections, d_parent);
      d_main_gui->setNPoints(d_size);
      d_main_gui->setSampleRate(d_samp_rate);

      // initialize update time to 10 times a second
      set_update_time(0.1);
    }

    void
    time_sink_f_impl::exec_()
    {
      d_qApplication->exec();
    }

    QWidget*
    time_sink_f_impl::qwidget()
    {
      return d_main_gui;
    }

    PyObject*
    time_sink_f_impl::pyqwidget()
    {
      PyObject *w = PyLong_FromVoidPtr((void*)d_main_gui);
      PyObject *retarg = Py_BuildValue("N", w);
      return retarg;
    }

    void
    time_sink_f_impl::set_y_axis(double min, double max)
    {
      d_main_gui->setYaxis(min, max);
    }

    void
    time_sink_f_impl::set_update_time(double t)
    {
      //convert update time to ticks
      gr::high_res_timer_type tps = gr::high_res_timer_tps();
      d_update_time = t * tps;
      d_main_gui->setUpdateTime(t);
      d_last_time = 0;
    }

    void
    time_sink_f_impl::set_title(const std::string &title)
    {
      d_main_gui->setTitle(title.c_str());
    }

    void
    time_sink_f_impl::set_line_label(int which, const std::string &label)
    {
      d_main_gui->setLineLabel(which, label.c_str());
    }

    void
    time_sink_f_impl::set_line_color(int which, const std::string &color)
    {
      d_main_gui->setLineColor(which, color.c_str());
    }

    void
    time_sink_f_impl::set_line_width(int which, int width)
    {
      d_main_gui->setLineWidth(which, width);
    }

    void
    time_sink_f_impl::set_line_style(int which, int style)
    {
      d_main_gui->setLineStyle(which, (Qt::PenStyle)style);
    }

    void
    time_sink_f_impl::set_line_marker(int which, int marker)
    {
      d_main_gui->setLineMarker(which, (QwtSymbol::Style)marker);
    }

    void
    time_sink_f_impl::set_line_alpha(int which, double alpha)
    {
      d_main_gui->setMarkerAlpha(which, (int)(255.0*alpha));
    }

    void
    time_sink_f_impl::set_trigger_mode(trigger_mode mode,
                                       trigger_slope slope,
                                       float level,
                                       float delay, int channel,
                                       const std::string &tag_key)
    {
      d_trigger_mode = mode;
      d_trigger_slope = slope;
      d_trigger_level = level;
      d_trigger_delay = static_cast<int>(delay*d_samp_rate);
      d_trigger_channel = channel;
      d_trigger_tag_key = pmt::intern(tag_key);
      d_triggered = false;
      d_trigger_count = 0;

      if(d_trigger_delay >= d_size) {
        GR_LOG_WARN(d_logger, boost::format("Trigger delay (%1%) outside of display range (%2%).") \
                    % d_trigger_delay % d_size);
        d_trigger_delay = d_size-1;
      }

      d_main_gui->setTriggerMode(d_trigger_mode);
      d_main_gui->setTriggerSlope(d_trigger_slope);
      d_main_gui->setTriggerLevel(d_trigger_level);
      d_main_gui->setTriggerDelay(delay);
      d_main_gui->setTriggerChannel(d_trigger_channel);
      d_main_gui->setTriggerTagKey(tag_key);

      set_history(d_trigger_delay + 2);
      declare_sample_delay(d_trigger_delay+1);
    }

    void
    time_sink_f_impl::set_size(int width, int height)
    {
      d_main_gui->resize(QSize(width, height));
    }

    std::string
    time_sink_f_impl::title()
    {
      return d_main_gui->title().toStdString();
    }

    std::string
    time_sink_f_impl::line_label(int which)
    {
      return d_main_gui->lineLabel(which).toStdString();
    }

    std::string
    time_sink_f_impl::line_color(int which)
    {
      return d_main_gui->lineColor(which).toStdString();
    }

    int
    time_sink_f_impl::line_width(int which)
    {
      return d_main_gui->lineWidth(which);
    }

    int
    time_sink_f_impl::line_style(int which)
    {
      return d_main_gui->lineStyle(which);
    }

    int
    time_sink_f_impl::line_marker(int which)
    {
      return d_main_gui->lineMarker(which);
    }

    double
    time_sink_f_impl::line_alpha(int which)
    {
      return (double)(d_main_gui->markerAlpha(which))/255.0;
    }

    void
    time_sink_f_impl::set_nsamps(const int newsize)
    {
      gr::thread::scoped_lock lock(d_mutex);

      if(newsize != d_size) {
	// Resize residbuf and replace data
	for(int i = 0; i < d_nconnections; i++) {
	  fft::free(d_residbufs[i]);
	  d_residbufs[i] = fft::malloc_double(newsize);

	  memset(d_residbufs[i], 0, newsize*sizeof(double));
	}

	// Set new size and reset buffer index 
	// (throws away any currently held data, but who cares?) 
	d_size = newsize;
	d_index = 0;

	d_main_gui->setNPoints(d_size);
      }
    }

    void
    time_sink_f_impl::set_samp_rate(const double samp_rate)
    {
      gr::thread::scoped_lock lock(d_mutex);
      d_samp_rate = samp_rate;
      d_main_gui->setSampleRate(d_samp_rate);
    }

    int
    time_sink_f_impl::nsamps() const
    {
      return d_size;
    }

    void
    time_sink_f_impl::enable_stem_plot(bool en)
    {
      d_main_gui->setStem(en);
    }

    void
    time_sink_f_impl::enable_menu(bool en)
    {
      d_main_gui->enableMenu(en);
    }

    void
    time_sink_f_impl::enable_grid(bool en)
    {
      d_main_gui->setGrid(en);
    }

    void
    time_sink_f_impl::enable_autoscale(bool en)
    {
      d_main_gui->autoScale(en);
    }

    void
    time_sink_f_impl::enable_semilogx(bool en)
    {
      d_main_gui->setSemilogx(en);
    }

    void
    time_sink_f_impl::enable_semilogy(bool en)
    {
      d_main_gui->setSemilogy(en);
    }

    void
    time_sink_f_impl::enable_tags(int which, bool en)
    {
      if(which == -1) {
        for(int n = 0; n < d_nconnections; n++) {
          d_main_gui->setTagMenu(n, en);
        }
      }
      else
        d_main_gui->setTagMenu(which, en);
    }

    void
    time_sink_f_impl::reset()
    {
      d_index = 0;
    }

    void
    time_sink_f_impl::_npoints_resize()
    {
      int newsize = d_main_gui->getNPoints();
      set_nsamps(newsize);
    }

    void
    time_sink_f_impl::_gui_update_trigger()
    {
      d_trigger_mode = d_main_gui->getTriggerMode();
      d_trigger_slope = d_main_gui->getTriggerSlope();
      d_trigger_level = d_main_gui->getTriggerLevel();
      d_trigger_channel = d_main_gui->getTriggerChannel();

      float delayf = d_main_gui->getTriggerDelay();
      int delay = static_cast<int>(delayf*d_samp_rate);

      if(delay != d_trigger_delay) {
        // We restrict the delay to be within the window of time being
        // plotted. This also restrict it to be less than the number
        // of output items since we cannot set the history greater
        // than this. We can probably get around this latter part by
        // not using history and doing more work inside 'work' to keep
        // track of things.
        int maxn;
        
        // If we have built the detail and buffers, we're stuck with
        // the max number of item; otherwise the buffer will be built
        // around this value so we just don't want to go over d_size.
        int correction = 5; // give us a bit of room at the edge.
        block_detail_sptr d = detail();
        if(d) {
          int max_possible = d->input(d_trigger_channel)->max_possible_items_available()/2 - d_initial_delay;
          maxn = std::max(1, std::min(max_possible, d_size) - correction);
        }
        else {
          maxn = d_size-correction;
          d_initial_delay = d_trigger_delay; // store this value before we create a d_detail
        }

        if(delay > maxn) {
          GR_LOG_WARN(d_logger, boost::format("Trigger delay (%1% / %2% sec) outside of max range (%3% / %4% sec)") \
                      % delay % delayf % maxn % (maxn/d_samp_rate));
          delay = maxn - d_initial_delay;
          delayf = delay/d_samp_rate;
        }

        d_trigger_delay = delay;
        d_main_gui->setTriggerDelay(delayf);
        set_history(d_trigger_delay+1);
      }

      std::string tagkey = d_main_gui->getTriggerTagKey();
      d_trigger_tag_key = pmt::intern(tagkey);
    }

    bool
    time_sink_f_impl::_test_trigger_slope(const float *in) const
    {
      float x0, x1;
      x0 = in[0];
      x1 = in[1];

      if(d_trigger_slope == TRIG_SLOPE_POS)
        return ((x0 <= d_trigger_level) && (x1 > d_trigger_level));
      else
        return ((x0 >= d_trigger_level) && (x1 < d_trigger_level));
    }

    int
    time_sink_f_impl::work(int noutput_items,
			   gr_vector_const_void_star &input_items,
			   gr_vector_void_star &output_items)
    {
      int n=0, idx=0;
      int trigger_index=0;
      const float *in;

      _npoints_resize();
      _gui_update_trigger();

      for(int i=0; i < noutput_items; i+=d_size) {

        // If auto or normal trigger, look for the trigger
        trigger_index = i;
        if((d_trigger_mode != TRIG_MODE_FREE) && !d_triggered) {

          if(d_trigger_mode == TRIG_MODE_TAG) {
            uint64_t nr = nitems_read(d_trigger_channel/2);

            // Look for tags past the delay so we can subtract delay
            // to calculate the trigger_index without it going
            // negative.
            std::vector<gr::tag_t> tags;
            get_tags_in_range(tags, d_trigger_channel/2,
                              nr + trigger_index + d_trigger_delay,
                              nr + trigger_index + d_trigger_delay + noutput_items,
                              d_trigger_tag_key);
            if(tags.size() > 0) {
              d_index = 0;
              d_triggered = true;
              d_trigger_count = 0;
              trigger_index = tags[0].offset - nr - trigger_index - d_trigger_delay;
              break;
            }
            else
              trigger_index = noutput_items;
          }
          else {
            for(; trigger_index < noutput_items; trigger_index++) {
              d_trigger_count++;

              // Test if trigger has occurred based on the input stream,
              // channel number, and slope direction
              in = (const float*)input_items[d_trigger_channel];
              if(_test_trigger_slope(&in[trigger_index + d_trigger_delay])) {
                d_triggered = true;
                d_trigger_count = 0;
                break;
              }
            }
           
            // If using auto trigger mode, trigger periodically even
            // without a trigger event.
            if((d_trigger_mode == TRIG_MODE_AUTO) && (d_trigger_count > d_size)) {
              d_triggered = true;
              d_trigger_count = 0;
            }
          }

          i = trigger_index;
        }

	unsigned int datasize = noutput_items - trigger_index;
	unsigned int resid = d_size-d_index;
	idx = 0;

        // If we're in trigger mode, test if we have triggered
        if((d_trigger_mode == TRIG_MODE_FREE) || d_triggered) {
          // If we have enough input for one full plot, do it
          if(datasize >= resid) {
            // Fill up residbufs with d_size number of items
            for(n = 0; n < d_nconnections; n++) {
              in = (const float*)input_items[idx];
              volk_32f_convert_64f_u(&d_residbufs[n][d_index],
                                     &in[trigger_index], resid);

              uint64_t nr = nitems_read(idx);
              std::vector<gr::tag_t> tags;
              get_tags_in_range(tags, idx, nr + trigger_index,
                                nr + trigger_index + resid);
              for(size_t t = 0; t < tags.size(); t++) {
                tags[t].offset = tags[t].offset - (nr + trigger_index) + d_index;
              }
              d_tags[idx].insert(d_tags[idx].end(), tags.begin(), tags.end());

              idx++;
            }

            // Update the plot if it's time
            if(gr::high_res_timer_now() - d_last_time > d_update_time) {
              d_last_time = gr::high_res_timer_now();
              d_qApplication->postEvent(d_main_gui,
                                        new TimeUpdateEvent(d_residbufs, d_size, d_tags));
            }

            d_index = 0;
            trigger_index += resid;
            d_triggered = false;

            for(n = 0; n < d_nconnections; n++) {
              d_tags[n].clear();
            }
          }

          // Otherwise, copy what we received into the residbufs for next time
          else {
            for(n = 0; n < d_nconnections; n++) {
              in = (const float*)input_items[idx];
              volk_32f_convert_64f_u(&d_residbufs[n][d_index],
                                     &in[trigger_index], datasize);

              uint64_t nr = nitems_read(idx);
              std::vector<gr::tag_t> tags;
              get_tags_in_range(tags, idx, nr + trigger_index,
                                nr + trigger_index + datasize);

              for(size_t t = 0; t < tags.size(); t++) {
                tags[t].offset = tags[t].offset - (nr + trigger_index) + d_index;
              }
              d_tags[idx].insert(d_tags[idx].end(), tags.begin(), tags.end());

              idx++;
            }
            d_index += datasize;
            trigger_index += datasize;
          }
        }
      }

      return trigger_index;
    }

  } /* namespace qtgui */
} /* namespace gr */
