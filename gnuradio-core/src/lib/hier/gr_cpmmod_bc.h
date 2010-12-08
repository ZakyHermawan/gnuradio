/* -*- c++ -*- */
/*
 * Copyright 2010 Free Software Foundation, Inc.
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

#include <gr_top_block.h>
#include <gr_char_to_float.h>
#include <gr_interp_fir_filter_fff.h>
#include <gr_frequency_modulator_fc.h>
#include <gr_cpm.h>


class gr_cpmmod_bc;
typedef boost::shared_ptr<gr_cpmmod_bc> gr_cpmmod_bc_sptr;


gr_cpmmod_bc_sptr
gr_make_cpmmod_bc(int type, float h, unsigned samples_per_sym, unsigned L, double beta=0.3);

/*!
 * \brief Generic CPM modulator
 *
 * \ingroup modulation_blk
 *
 * Parameters:
 * * \p type: The modulation type. Can be one of LREC, LRC, LSRC, TFM or GAUSSIAN. See
 *            gr_cpm::phase_response() for a detailed description.
 * * \p h: The modulation index. h*PI is the maximum phase change that can occur
 *         between two symbols, i.e., if you only send ones, the phase will increase
 *         by h*PI every \p samples_per_sym samples. Set this to 0.5 for Minimum Shift
 *         Keying variants.
 * * \p samples_per_sym: Samples per symbol.
 * * \p L: The length of the phase duration in symbols. For L=1, this yields full-
 *         response CPM symbols, for L > 1, it yields partial-response.
 * * \p beta: For LSRC, this is the rolloff factor. For Gaussian pulses, this is the 3 dB
 *            time-bandwidth product.
 *
 * Examples:
 * * Setting h = 0.5, L = 1, type = LREC yields MSK.
 * * Setting h = 0.5, type = GAUSSIAN and beta = 0.3 yields GMSK as used in GSM.
 *
 * The input of this block are symbols from an M-ary alphabet
 * \pm1, \pm3, ..., \pm(M-1). Usually, M = 2 and therefore, the
 * valid inputs are \pm1.
 * The modulator will silently accept any other inputs, though.
 * The output is the phase-modulated signal.
 */
class gr_cpmmod_bc : public gr_hier_block2
{
	friend gr_cpmmod_bc_sptr gr_make_cpmmod_bc(int type, float h, unsigned samples_per_sym, unsigned L, double beta);
	gr_cpmmod_bc(gr_cpm::cpm_type type, float h, unsigned samples_per_sym, unsigned L, double beta);

	std::vector<float> d_taps;

	gr_char_to_float_sptr d_char_to_float;
	gr_interp_fir_filter_fff_sptr d_pulse_shaper;
	gr_frequency_modulator_fc_sptr d_fm;


 public:
	//! Return the phase response FIR taps
	 std::vector<float> get_taps() { return d_taps; };
};

