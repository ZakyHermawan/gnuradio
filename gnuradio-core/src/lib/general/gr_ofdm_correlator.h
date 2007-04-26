/* -*- c++ -*- */
/*
 * Copyright 2006 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
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

#ifndef INCLUDED_GR_OFDM_CORRELATOR_H
#define INCLUDED_GR_OFDM_CORRELATOR_H


#include <gr_block.h>
#include <vector>

class gr_ofdm_correlator;
typedef boost::shared_ptr<gr_ofdm_correlator> gr_ofdm_correlator_sptr;

gr_ofdm_correlator_sptr 
gr_make_ofdm_correlator (unsigned int occupied_carriers, unsigned int vlen,
			 unsigned int cplen,
			 std::vector<gr_complex> known_symbol1, 
			 std::vector<gr_complex> known_symbol2);

/*!
 * \brief take a vector of complex constellation points in from an FFT
 * and performs a correlation and equalization.
 * \inblock blocks
 *
 * This block takes the output of an FFT of a received OFDM symbol and finds the 
 * start of a frame based on two known symbols. It also looks at the surrounding
 * bins in the FFT output for the correlation in case there is a large frequency
 * shift in the data. This block assumes that the fine frequency shift has already
 * been corrected and that the samples fall in the middle of one FFT bin.
 *
 * It then uses one of those known
 * symbosl to estimate the channel response overa all subcarriers and does a simple 
 * 1-tap equalization on all subcarriers. This corrects for the phase and amplitude
 * distortion caused by the channel.
 */

class gr_ofdm_correlator : public gr_block
{
  /*! 
   * \brief Build an OFDM correlator and equalizer.
   * \param occupied_carriers   The number of subcarriers with data in the received symbol
   * \param vlen                The size of the FFT vector (occupied_carriers + unused carriers)
   * \param known_symbol1       A vector of complex numbers representing a known symbol at the
   *                            start of a frame (usually a BPSK PN sequence)
   * \param known_symbol2       A vector of complex numbers representing a known symbol at the
   *                            start of a frame after known_symbol1 (usually a BPSK PN sequence). 
   *                            Both of these start symbols are differentially correlated to compensate
   *                            for phase changes between symbols. 
   */
  friend gr_ofdm_correlator_sptr
  gr_make_ofdm_correlator (unsigned int occupied_carriers, unsigned int vlen,
			   unsigned int cplen,
			   std::vector<gr_complex> known_symbol1, 
			   std::vector<gr_complex> known_symbol2);
  
 protected:
  gr_ofdm_correlator (unsigned int occupied_carriers, unsigned int vlen,
		      unsigned int cplen,
		      std::vector<gr_complex> known_symbol1, 
		      std::vector<gr_complex> known_symbol2);
  
 private:
  unsigned char slicer(gr_complex x);
  bool correlate(const gr_complex *previous, const gr_complex *current, int zeros_on_left);
  void calculate_equalizer(const gr_complex *previous, 
			   const gr_complex *current, int zeros_on_left);
  gr_complex coarse_freq_comp(int freq_delta, int count);
  
  unsigned int d_occupied_carriers;  // !< \brief number of subcarriers with data
  unsigned int d_vlen;               // !< \brief length of FFT vector
  unsigned int d_cplen;              // !< \brief length of cyclic prefix in samples
  unsigned int d_freq_shift_len;     // !< \brief number of surrounding bins to look at for correlation
  std::vector<gr_complex> d_known_symbol1, d_known_symbol2; // !< \brief known symbols at start of frame
  std::vector<gr_complex> d_diff_corr_factor; // !< \brief factor used in correlation
  std::vector<gr_complex> d_hestimate; // !< channel estimate
  signed int d_coarse_freq; // !< \brief search distance in number of bins
  unsigned int d_phase_count;        // !< \brief accumulator for coarse freq correction
  float d_snr_est;  // !< an estimation of the signal to noise ratio

  void forecast(int noutput_items, gr_vector_int &ninput_items_required);

 public:
  /*!
   * \brief Return an estimate of the SNR of the channel
   */
  float snr() { return d_snr_est; }

  ~gr_ofdm_correlator(void);
  int general_work(int noutput_items,
		   gr_vector_int &ninput_items,
		   gr_vector_const_void_star &input_items,
		   gr_vector_void_star &output_items);
};


#endif
