/* -*- c++ -*- */
/*
 * Copyright 2009,2010 Free Software Foundation, Inc.
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


#ifndef INCLUDED_GR_PFB_CLOCK_SYNC_CCF_H
#define	INCLUDED_GR_PFB_CLOCK_SYNC_CCF_H

#include <gr_block.h>

class gr_pfb_clock_sync_ccf;
typedef boost::shared_ptr<gr_pfb_clock_sync_ccf> gr_pfb_clock_sync_ccf_sptr;
gr_pfb_clock_sync_ccf_sptr gr_make_pfb_clock_sync_ccf (double sps, float loop_bw,
						       const std::vector<float> &taps,
						       unsigned int filter_size=32,
						       float init_phase=0,
						       float max_rate_deviation=1.5,
						       int osps=1);

class gr_fir_ccf;

/*!
 * \class gr_pfb_clock_sync_ccf
 *
 * \brief Timing synchronizer using polyphase filterbanks
 *
 * \ingroup filter_blk
 * 
 * This block performs timing synchronization for PAM signals by minimizing the
 * derivative of the filtered signal, which in turn maximizes the SNR and 
 * minimizes ISI.
 *
 * This approach works by setting up two filterbanks; one filterbank contains the 
 * signal's pulse shaping matched filter (such as a root raised cosine filter),
 * where each branch of the filterbank contains a different phase of the filter.
 * The second filterbank contains the derivatives of the filters in the first 
 * filterbank. Thinking of this in the time domain, the first filterbank contains
 * filters that have a sinc shape to them. We want to align the output signal to
 * be sampled at exactly the peak of the sinc shape. The derivative of the sinc
 * contains a zero at the maximum point of the sinc (sinc(0) = 1, sinc(0)' = 0).
 * Furthermore, the region around the zero point is relatively linear. We make
 * use of this fact to generate the error signal.
 *
 * If the signal out of the derivative filters is d_i[n] for the ith filter, and
 * the output of the matched filter is x_i[n], we calculate the error as:
 *    e[n] = (Re{x_i[n]} * Re{d_i[n]} + Im{x_i[n]} * Im{d_i[n]}) / 2.0
 * This equation averages the error in the real and imaginary parts. There are two
 * reasons we multiply by the signal itself. First, if the symbol could be positive
 * or negative going, but we want the error term to always tell us to go in the 
 * same direction depending on which side of the zero point we are on. The sign of
 * x_i[n] adjusts the error term to do this. Second, the magnitude of x_i[n] scales
 * the error term depending on the symbol's amplitude, so larger signals give us
 * a stronger error term because we have more confidence in that symbol's value.
 * Using the magnitude of x_i[n] instead of just the sign is especially good for
 * signals with low SNR.
 *
 * The error signal, e[n], gives us a value proportional to how far away from the zero
 * point we are in the derivative signal. We want to drive this value to zero, so we
 * set up a second order loop. We have two variables for this loop; d_k is the filter
 * number in the filterbank we are on and d_rate is the rate which we travel through
 * the filters in the steady state. That is, due to the natural clock differences between
 * the transmitter and receiver, d_rate represents that difference and would traverse
 * the filter phase paths to keep the receiver locked. Thinking of this as a second-order
 * PLL, the d_rate is the frequency and d_k is the phase. So we update d_rate and d_k
 * using the standard loop equations based on two error signals, d_alpha and d_beta.
 * We have these two values set based on each other for a critically damped system, so in
 * the block constructor, we just ask for "gain," which is d_alpha while d_beta is
 * equal to (gain^2)/4.
 *
 * The clock sync block needs to know the number of samples per symbol (sps), because it
 * only returns a single point representing the symbol. The sps can be any positive real
 * number and does not need to be an integer. The filter taps must also be specified. The
 * taps are generated by first conceiving of the prototype filter that would be the signal's
 * matched filter. Then interpolate this by the number of filters in the filterbank. These
 * are then distributed among all of the filters. So if the prototype filter was to have
 * 45 taps in it, then each path of the filterbank will also have 45 taps. This is easily
 * done by building the filter with the sample rate multiplied by the number of filters
 * to use.
 *
 * The number of filters can also be set and defaults to 32. With 32 filters, you get a
 * good enough resolution in the phase to produce very small, almost unnoticeable, ISI.
 * Going to 64 filters can reduce this more, but after that there is very little gained
 * for the extra complexity.
 *
 * The initial phase is another settable parameter and refers to the filter path the
 * algorithm initially looks at (i.e., d_k starts at init_phase). This value defaults 
 * to zero, but it might be useful to start at a different phase offset, such as the mid-
 * point of the filters.
 *
 * The final parameter is the max_rate_devitation, which defaults to 1.5. This is how far
 * we allow d_rate to swing, positive or negative, from 0. Constraining the rate can help
 * keep the algorithm from walking too far away to lock during times when there is no signal.
 *
 */

class gr_pfb_clock_sync_ccf : public gr_block
{
 private:
  /*!
   * Build the polyphase filterbank timing synchronizer.
   * \param sps (double) The number of samples per symbol in the incoming signal
   * \param loop_bw (float) The bandwidth of the control loop; set's alpha and beta.
   * \param taps (vector<int>) The filter taps.
   * \param filter_size (uint) The number of filters in the filterbank (default = 32).
   * \param init_phase (float) The initial phase to look at, or which filter to start 
   *                           with (default = 0).
   * \param max_rate_deviation (float) Distance from 0 d_rate can get (default = 1.5).
   * \param osps (int) The number of output samples per symbol (default=1).
   *
   */
  friend gr_pfb_clock_sync_ccf_sptr gr_make_pfb_clock_sync_ccf (double sps, float loop_bw,
								const std::vector<float> &taps,
								unsigned int filter_size,
								float init_phase,
								float max_rate_deviation,
								int osps);

  bool			            d_updated;
  double                            d_sps;
  double                            d_sample_num;
  float                             d_loop_bw;
  float                             d_damping;
  float                             d_alpha;
  float                             d_beta;

  int                               d_nfilters;
  int                               d_taps_per_filter;
  std::vector<gr_fir_ccf*>          d_filters;
  std::vector<gr_fir_ccf*>          d_diff_filters;
  std::vector< std::vector<float> > d_taps;
  std::vector< std::vector<float> > d_dtaps;

  float                             d_k;
  float                             d_rate;
  float                             d_rate_i;
  float                             d_rate_f;
  float                             d_max_dev;
  int                               d_filtnum;
  int                               d_osps;
  float                             d_error;

  /*!
   * Build the polyphase filterbank timing synchronizer.
   */
  gr_pfb_clock_sync_ccf (double sps, float loop_bw,
			 const std::vector<float> &taps,
			 unsigned int filter_size,
			 float init_phase,
			 float max_rate_deviation,
			 int osps);
  
  void create_diff_taps(const std::vector<float> &newtaps,
			std::vector<float> &difftaps);

public:
  ~gr_pfb_clock_sync_ccf ();

  /*! \brief update the system gains from omega and eta
   *
   *  This function updates the system gains based on the loop
   *  bandwidth and damping factor of the system.
   *  These two factors can be set separately through their own
   *  set functions.
   */
  void update_gains();
  
  /*!
   * Resets the filterbank's filter taps with the new prototype filter
   */
  void set_taps (const std::vector<float> &taps,
		 std::vector< std::vector<float> > &ourtaps,
		 std::vector<gr_fir_ccf*> &ourfilter);

  /*!
   * Returns all of the taps of the matched filter
   */
  std::vector< std::vector<float> > get_taps();

  /*!
   * Returns all of the taps of the derivative filter
   */
  std::vector< std::vector<float> > get_diff_taps();

  /*!
   * Returns the taps of the matched filter for a particular channel
   */
  std::vector<float> get_channel_taps(int channel);

  /*!
   * Returns the taps in the derivative filter for a particular channel
   */
  std::vector<float> get_diff_channel_taps(int channel);

  /*!
   * Return the taps as a formatted string for printing
   */
  std::string get_taps_as_string();

  /*!
   * Return the derivative filter taps as a formatted string for printing
   */
  std::string get_diff_taps_as_string();


  /*******************************************************************
    SET FUNCTIONS
  *******************************************************************/
  

  /*!
   * \brief Set the loop bandwidth
   *
   * Set the loop filter's bandwidth to \p bw. This should be between 
   * 2*pi/200 and 2*pi/100  (in rads/samp). It must also be a positive
   * number.
   *
   * When a new damping factor is set, the gains, alpha and beta, of the loop
   * are recalculated by a call to update_gains().
   *
   * \param bw    (float) new bandwidth
   *
   */
  void set_loop_bandwidth(float bw);

  /*!
   * \brief Set the loop damping factor
   *
   * Set the loop filter's damping factor to \p df. The damping factor
   * should be sqrt(2)/2.0 for critically damped systems.
   * Set it to anything else only if you know what you are doing. It must
   * be a number between 0 and 1.
   *
   * When a new damping factor is set, the gains, alpha and beta, of the loop
   * are recalculated by a call to update_gains().
   *
   * \param df    (float) new damping factor
   *
   */
  void set_damping_factor(float df);

  /*!
   * \brief Set the loop gain alpha
   *
   * Set's the loop filter's alpha gain parameter.
   *
   * This value should really only be set by adjusting the loop bandwidth
   * and damping factor.
   *
   * \param alpha    (float) new alpha gain
   *
   */
  void set_alpha(float alpha);

  /*!
   * \brief Set the loop gain beta
   *
   * Set's the loop filter's beta gain parameter.
   *
   * This value should really only be set by adjusting the loop bandwidth
   * and damping factor.
   *
   * \param beta    (float) new beta gain
   *
   */
  void set_beta(float beta);

  /*!
   * Set the maximum deviation from 0 d_rate can have
   */  
  void set_max_rate_deviation(float m)
  {
    d_max_dev = m;
  }
  
  /*******************************************************************
    GET FUNCTIONS
  *******************************************************************/

  /*!
   * \brief Returns the loop bandwidth
   */
  float get_loop_bandwidth() const;

  /*!
   * \brief Returns the loop damping factor
   */
  float get_damping_factor() const;

  /*!
   * \brief Returns the loop gain alpha
   */
  float get_alpha() const;

  /*!
   * \brief Returns the loop gain beta
   */
  float get_beta() const;

  /*!
   * \brief Returns the current clock rate
   */
  float get_clock_rate() const;

  /*******************************************************************
  *******************************************************************/

  bool check_topology(int ninputs, int noutputs);

  int general_work (int noutput_items,
		    gr_vector_int &ninput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items);
};

#endif
