/* -*- c++ -*- */
/*
 * Copyright 2006,2010,2011 Free Software Foundation, Inc.
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

#include <digital_costas_loop_cc.h>
#include <gr_io_signature.h>
#include <gr_expj.h>
#include <gr_sincos.h>
#include <gr_math.h>

#define M_TWOPI (2*M_PI)

digital_costas_loop_cc_sptr
digital_make_costas_loop_cc (float loop_bw, int order
			     ) throw (std::invalid_argument)
{
  return gnuradio::get_initial_sptr(new digital_costas_loop_cc 
				    (loop_bw, order));
}

digital_costas_loop_cc::digital_costas_loop_cc (float loop_bw, int order
						) throw (std::invalid_argument)
  : gr_sync_block ("costas_loop_cc",
		   gr_make_io_signature (1, 1, sizeof (gr_complex)),
		   gr_make_io_signature2 (1, 2, sizeof (gr_complex), sizeof(float))),
    d_max_freq(1.0), d_min_freq(-1.0),
    d_loop_bw(loop_bw),
    d_order(order), d_phase_detector(NULL)
{
  // Set the damping factor for a critically damped system
  d_damping = sqrtf(2.0f)/2.0f;

  // Set the bandwidth, which will then call update_gains()
  set_loop_bandwidth(loop_bw);

  // Set up the phase detector to use based on the constellation order
  switch(d_order) {
  case 2:
    d_phase_detector = &digital_costas_loop_cc::phase_detector_2;
    break;

  case 4:
    d_phase_detector = &digital_costas_loop_cc::phase_detector_4;
    break;

  case 8:
    d_phase_detector = &digital_costas_loop_cc::phase_detector_8;
    break;

  default: 
    throw std::invalid_argument("order must be 2, 4, or 8");
    break;
  }

  // Initialize loop values
  d_freq = 0;
  d_phase = 0;
}

float
digital_costas_loop_cc::phase_detector_8(gr_complex sample) const
{
  /* This technique splits the 8PSK constellation into 2 squashed
     QPSK constellations, one when I is larger than Q and one where
     Q is larger than I. The error is then calculated proportionally
     to these squashed constellations by the const K = sqrt(2)-1.

     The signal magnitude must be > 1 or K will incorrectly bias
     the error value. 

     Ref: Z. Huang, Z. Yi, M. Zhang, K. Wang, "8PSK demodulation for
     new generation DVB-S2", IEEE Proc. Int. Conf. Communications,
     Circuits and Systems, Vol. 2, pp. 1447 - 1450, 2004.
  */

  float K = (sqrt(2.0) - 1);
  if(fabsf(sample.real()) >= fabsf(sample.imag())) {
    return ((sample.real()>0 ? 1.0 : -1.0) * sample.imag() -
	    (sample.imag()>0 ? 1.0 : -1.0) * sample.real() * K);
  }
  else {
    return ((sample.real()>0 ? 1.0 : -1.0) * sample.imag() * K -
	    (sample.imag()>0 ? 1.0 : -1.0) * sample.real());
  }
}

float
digital_costas_loop_cc::phase_detector_4(gr_complex sample) const
{

  return ((sample.real()>0 ? 1.0 : -1.0) * sample.imag() -
	  (sample.imag()>0 ? 1.0 : -1.0) * sample.real());
}

float
digital_costas_loop_cc::phase_detector_2(gr_complex sample) const
{
  return (sample.real()*sample.imag());
}

/*******************************************************************
    SET FUNCTIONS
*******************************************************************/

void
digital_costas_loop_cc::set_loop_bandwidth(float bw) 
{
  if(bw < 0) {
    throw std::out_of_range ("digital_costas_loop_cc: invalid bandwidth. Must be >= 0.");
  }
  
  d_loop_bw = bw;
  update_gains();
}

void
digital_costas_loop_cc::set_damping_factor(float df) 
{
  if(df < 0 || df > 1.0) {
    throw std::out_of_range ("digital_costas_loop_cc: invalid damping factor. Must be in [0,1].");
  }
  
  d_damping = df;
  update_gains();
}

void
digital_costas_loop_cc::set_alpha(float alpha)
{
  if(alpha < 0 || alpha > 1.0) {
    throw std::out_of_range ("digital_costas_loop_cc: invalid alpha. Must be in [0,1].");
  }
  d_alpha = alpha;
}

void
digital_costas_loop_cc::set_beta(float beta)
{
  if(beta < 0 || beta > 1.0) {
    throw std::out_of_range ("digital_costas_loop_cc: invalid beta. Must be in [0,1].");
  }
  d_beta = beta;
}

void
digital_costas_loop_cc::set_frequency(float freq)
{
  if(freq > d_max_freq)
    d_freq = d_min_freq;
  else if(freq < d_min_freq)
    d_freq = d_max_freq;
  else
    d_freq = freq;
}

void
digital_costas_loop_cc::set_phase(float phase)
{
  d_phase = phase;
  while(d_phase>M_TWOPI)
    d_phase -= M_TWOPI;
  while(d_phase<-M_TWOPI)
    d_phase += M_TWOPI;
}

   
/*******************************************************************
    GET FUNCTIONS
*******************************************************************/


float
digital_costas_loop_cc::get_loop_bandwidth() const
{
  return d_loop_bw;
}

float
digital_costas_loop_cc::get_damping_factor() const
{
  return d_damping;
}

float
digital_costas_loop_cc::get_alpha() const
{
  return d_alpha;
}

float
digital_costas_loop_cc::get_beta() const
{
  return d_beta;
}

float
digital_costas_loop_cc::get_frequency() const
{
  return d_freq;
}

float
digital_costas_loop_cc::get_phase() const
{
  return d_phase;
}


/*******************************************************************
*******************************************************************/


void
digital_costas_loop_cc::update_gains()
{
  float denom = (1.0 + 2.0*d_damping*d_loop_bw + d_loop_bw*d_loop_bw);
  d_alpha = (4*d_damping*d_loop_bw) / denom;
  d_beta = (4*d_loop_bw*d_loop_bw) / denom;
}

int
digital_costas_loop_cc::work (int noutput_items,
			      gr_vector_const_void_star &input_items,
			      gr_vector_void_star &output_items)
{
  const gr_complex *iptr = (gr_complex *) input_items[0];
  gr_complex *optr = (gr_complex *) output_items[0];
  float *foptr = (float *) output_items[1];

  bool write_foptr = output_items.size() >= 2;

  float error;
  gr_complex nco_out;
  
  if (write_foptr) {

    for (int i = 0; i < noutput_items; i++){
      nco_out = gr_expj(-d_phase);
      optr[i] = iptr[i] * nco_out;
      
      error = (*this.*d_phase_detector)(optr[i]);
      error = gr_branchless_clip(error, 1.0);
	
      d_freq = d_freq + d_beta * error;
      d_phase = d_phase + d_freq + d_alpha * error;

      while(d_phase>M_TWOPI)
	d_phase -= M_TWOPI;
      while(d_phase<-M_TWOPI)
	d_phase += M_TWOPI;

      if (d_freq > d_max_freq)
	d_freq = d_min_freq;
      else if (d_freq < d_min_freq)
	d_freq = d_max_freq;
      
      foptr[i] = d_freq;
    } 
  } else {
    for (int i = 0; i < noutput_items; i++){
      nco_out = gr_expj(-d_phase);
      optr[i] = iptr[i] * nco_out;
      
      error = (*this.*d_phase_detector)(optr[i]);
      error = gr_branchless_clip(error, 1.0);
      
      d_freq = d_freq + d_beta * error;
      d_phase = d_phase + d_freq + d_alpha * error;
      
      while(d_phase>M_TWOPI)
	d_phase -= M_TWOPI;
      while(d_phase<-M_TWOPI)
	d_phase += M_TWOPI;
      
      if (d_freq > d_max_freq)
	d_freq = d_min_freq;
      else if (d_freq < d_min_freq)
	d_freq = d_max_freq;
      
    }
  }
  return noutput_items;
}
