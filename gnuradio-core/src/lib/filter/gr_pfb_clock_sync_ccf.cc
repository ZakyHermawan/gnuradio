/* -*- c++ -*- */
/*
 * Copyright 2009 Free Software Foundation, Inc.
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
#include "config.h"
#endif

#include <cstdio>
#include <cmath>

#include <gr_pfb_clock_sync_ccf.h>
#include <gr_fir_ccf.h>
#include <gr_fir_util.h>
#include <gr_io_signature.h>
#include <gr_math.h>

gr_pfb_clock_sync_ccf_sptr gr_make_pfb_clock_sync_ccf (double sps, float gain,
						       const std::vector<float> &taps,
						       unsigned int filter_size,
						       float init_phase,
						       float max_rate_deviation)
{
  return gr_pfb_clock_sync_ccf_sptr (new gr_pfb_clock_sync_ccf (sps, gain, taps,
								filter_size,
								init_phase,
								max_rate_deviation));
}

int ios[] = {sizeof(gr_complex), sizeof(float), sizeof(float), sizeof(float)};
std::vector<int> iosig(ios, ios+sizeof(ios)/sizeof(int));
gr_pfb_clock_sync_ccf::gr_pfb_clock_sync_ccf (double sps, float gain,
					      const std::vector<float> &taps,
					      unsigned int filter_size,
					      float init_phase,
					      float max_rate_deviation)
  : gr_block ("pfb_clock_sync_ccf",
	      gr_make_io_signature (1, 1, sizeof(gr_complex)),
	      gr_make_io_signaturev (1, 4, iosig)),
    d_updated (false), d_nfilters(filter_size),
    d_max_dev(max_rate_deviation)
{
  d_nfilters = filter_size;
  d_sps = floor(sps);

  // Store the last filter between calls to work
  // The accumulator keeps track of overflow to increment the stride correctly.
  // set it here to the fractional difference based on the initial phaes
  set_alpha(gain);
  set_beta(0.25*gain*gain);
  d_k = init_phase;
  d_rate = (sps-floor(sps))*(double)d_nfilters;
  d_filtnum = (int)floor(d_k);

  d_filters = std::vector<gr_fir_ccf*>(d_nfilters);
  d_diff_filters = std::vector<gr_fir_ccf*>(d_nfilters);

  // Create an FIR filter for each channel and zero out the taps
  std::vector<float> vtaps(0, d_nfilters);
  for(unsigned int i = 0; i < d_nfilters; i++) {
    d_filters[i] = gr_fir_util::create_gr_fir_ccf(vtaps);
    d_diff_filters[i] = gr_fir_util::create_gr_fir_ccf(vtaps);
  }

  // Now, actually set the filters' taps
  std::vector<float> dtaps;
  create_diff_taps(taps, dtaps);
  set_taps(taps, d_taps, d_filters);
  set_taps(dtaps, d_dtaps, d_diff_filters);
}

gr_pfb_clock_sync_ccf::~gr_pfb_clock_sync_ccf ()
{
  for(unsigned int i = 0; i < d_nfilters; i++) {
    delete d_filters[i];
  }
}

void
gr_pfb_clock_sync_ccf::set_taps (const std::vector<float> &newtaps,
				 std::vector< std::vector<float> > &ourtaps,
				 std::vector<gr_fir_ccf*> &ourfilter)
{
  int i,j;

  unsigned int ntaps = newtaps.size();
  d_taps_per_filter = (unsigned int)ceil((double)ntaps/(double)d_nfilters);

  // Create d_numchan vectors to store each channel's taps
  ourtaps.resize(d_nfilters);
  
  // Make a vector of the taps plus fill it out with 0's to fill
  // each polyphase filter with exactly d_taps_per_filter
  std::vector<float> tmp_taps;
  tmp_taps = newtaps;
  while((float)(tmp_taps.size()) < d_nfilters*d_taps_per_filter) {
    tmp_taps.push_back(0.0);
  }
  
  // Partition the filter
  for(i = 0; i < d_nfilters; i++) {
    // Each channel uses all d_taps_per_filter with 0's if not enough taps to fill out
    ourtaps[d_nfilters-1-i] = std::vector<float>(d_taps_per_filter, 0);
    for(j = 0; j < d_taps_per_filter; j++) {
      ourtaps[d_nfilters - 1 - i][j] = tmp_taps[i + j*d_nfilters];
    }
    
    // Build a filter for each channel and add it's taps to it
    ourfilter[i]->set_taps(ourtaps[d_nfilters-1-i]);
  }

  // Set the history to ensure enough input items for each filter
  set_history (d_taps_per_filter + d_sps);

  d_updated = true;
}

void
gr_pfb_clock_sync_ccf::create_diff_taps(const std::vector<float> &newtaps,
					std::vector<float> &difftaps)
{
  difftaps.clear();
  difftaps.push_back(0); //newtaps[0]);
  for(unsigned int i = 1; i < newtaps.size()-1; i++) {
    float tap = newtaps[i+1] - newtaps[i-1];
    difftaps.push_back(tap);
  }
  difftaps.push_back(0);//-newtaps[newtaps.size()-1]);
}

void
gr_pfb_clock_sync_ccf::print_taps()
{
  unsigned int i, j;
  printf("[ ");
  for(i = 0; i < d_nfilters; i++) {
    printf("[%.4e, ", d_taps[i][0]);
    for(j = 1; j < d_taps_per_filter-1; j++) {
      printf("%.4e,", d_taps[i][j]);
    }
    printf("%.4e],", d_taps[i][j]);
  }
  printf(" ]\n");
}

void
gr_pfb_clock_sync_ccf::print_diff_taps()
{
  unsigned int i, j;
  printf("[ ");
  for(i = 0; i < d_nfilters; i++) {
    printf("[%.4e, ", d_dtaps[i][0]);
    for(j = 1; j < d_taps_per_filter-1; j++) {
      printf("%.4e,", d_dtaps[i][j]);
    }
    printf("%.4e],", d_dtaps[i][j]);
  }
  printf(" ]\n");
}


std::vector<float>
gr_pfb_clock_sync_ccf::channel_taps(int channel)
{
  std::vector<float> taps;
  unsigned int i;
  for(i = 0; i < d_taps_per_filter; i++) {
    taps.push_back(d_taps[channel][i]);
  }
  return taps;
}

std::vector<float>
gr_pfb_clock_sync_ccf::diff_channel_taps(int channel)
{
  std::vector<float> taps;
  unsigned int i;
  for(i = 0; i < d_taps_per_filter; i++) {
    taps.push_back(d_dtaps[channel][i]);
  }
  return taps;
}


int
gr_pfb_clock_sync_ccf::general_work (int noutput_items,
				     gr_vector_int &ninput_items,
				     gr_vector_const_void_star &input_items,
				     gr_vector_void_star &output_items)
{
  gr_complex *in = (gr_complex *) input_items[0];
  gr_complex *out = (gr_complex *) output_items[0];

  float *err, *outrate, *outk;
  if(output_items.size() > 2) {
    err = (float *) output_items[1];
    outrate = (float*)output_items[2];
    outk = (float*)output_items[3];
  }
  
  if (d_updated) {
    d_updated = false;
    return 0;		     // history requirements may have changed.
  }

  // We need this many to process one output
  int nrequired = ninput_items[0] - d_taps_per_filter;

  int i = 0, count = 0;
  float error, error_r, error_i;

  // produce output as long as we can and there are enough input samples
  while((i < noutput_items) && (count < nrequired)) {
    d_filtnum = (int)floor(d_k);

    // Keep the current filter number in [0, d_nfilters]
    // If we've run beyond the last filter, wrap around and go to next sample
    // If we've go below 0, wrap around and go to previous sample
    while(d_filtnum >= d_nfilters) {
      d_k -= d_nfilters;
      d_filtnum -= d_nfilters;
      count += 1;
    }
    while(d_filtnum < 0) {
      d_k += d_nfilters;
      d_filtnum += d_nfilters;
      count -= 1;
    }

    out[i] = d_filters[d_filtnum]->filter(&in[count]);
    gr_complex diff = d_diff_filters[d_filtnum]->filter(&in[count]);
    error_r  = out[i].real() * diff.real();
    error_i  = out[i].imag() * diff.imag();
    error = (error_i + error_r) / 2.0;       // average error from I&Q channel

    // Run the control loop to update the current phase (k) and tracking rate
    d_k = d_k + d_alpha*error + d_rate;
    d_rate = d_rate + d_beta*error;
    
    // Keep our rate within a good range
    d_rate = gr_branchless_clip(d_rate, d_max_dev);

    i++;
    count += (int)floor(d_sps);

    if(output_items.size() > 2) {
      err[i] = error;
      outrate[i] = d_rate;
      outk[i] = d_k;
    }
  }
  consume_each(count);

  return i;
}
