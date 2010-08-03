/* -*- c++ -*- */
/*
 * Copyright 2004,2007,2008,2010 Free Software Foundation, Inc.
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

#include <gr_fft_vcc_fftw.h>
#include <gr_io_signature.h>
#include <gri_fft.h>
#include <math.h>
#include <string.h>

gr_fft_vcc_sptr
gr_make_fft_vcc_fftw (int fft_size, bool forward, const std::vector<float> &window, bool shift)
{
  return gnuradio::get_initial_sptr(new gr_fft_vcc_fftw (fft_size, forward, window, shift));
}

gr_fft_vcc_fftw::gr_fft_vcc_fftw (int fft_size, bool forward,
				  const std::vector<float> &window, bool shift)
  : gr_fft_vcc("fft_vcc_fftw", fft_size, forward, window, shift)
{
  d_fft = new gri_fft_complex (d_fft_size, forward);
}

gr_fft_vcc_fftw::~gr_fft_vcc_fftw ()
{
  delete d_fft;
}

int
gr_fft_vcc_fftw::work (int noutput_items,
		  gr_vector_const_void_star &input_items,
		  gr_vector_void_star &output_items)
{
  const gr_complex *in = (const gr_complex *) input_items[0];
  gr_complex *out = (gr_complex *) output_items[0];

  unsigned int input_data_size = input_signature()->sizeof_stream_item (0);
  unsigned int output_data_size = output_signature()->sizeof_stream_item (0);

  int count = 0;

  while (count++ < noutput_items){
    
    // copy input into optimally aligned buffer
    
    if (d_window.size()){
      gr_complex *dst = d_fft->get_inbuf();
      for (unsigned int i = 0; i < d_fft_size; i++)		// apply window
	dst[i] = in[i] * d_window[i];
    }
    else {
      if(!d_forward && d_shift) {  // apply an ifft shift on the data
	gr_complex *dst = d_fft->get_inbuf();
	unsigned int len = (unsigned int)(floor(d_fft_size/2.0)); // half length of complex array
	memcpy(&dst[0], &in[len], sizeof(gr_complex)*(d_fft_size - len));
	memcpy(&dst[d_fft_size - len], &in[0], sizeof(gr_complex)*len);
      }
      else {
	memcpy (d_fft->get_inbuf(), in, input_data_size);
      }
    }
    
    // compute the fft
    d_fft->execute ();
    
    // copy result to our output
    if(d_forward && d_shift) {  // apply a fft shift on the data
      unsigned int len = (unsigned int)(ceil(d_fft_size/2.0));
      memcpy(&out[0], &d_fft->get_outbuf()[len], sizeof(gr_complex)*(d_fft_size - len));
      memcpy(&out[d_fft_size - len], &d_fft->get_outbuf()[0], sizeof(gr_complex)*len);
    }
    else {
      memcpy (out, d_fft->get_outbuf (), output_data_size);
    }
    
    in  += d_fft_size;
    out += d_fft_size;
  }
  
  return noutput_items;
}

