/* -*- c++ -*- */
/*
 * Copyright 2005 Free Software Foundation, Inc.
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

/*
 * WARNING: This file is automatically generated by
 * generate_gr_rational_resampler_base_XXX.py Any changes made to this
 * file will be overwritten.
 */

#ifndef @GUARD_NAME@
#define	@GUARD_NAME@

#include <gr_block.h>

class @NAME@;
typedef boost::shared_ptr<@NAME@> @SPTR_NAME@;
@SPTR_NAME@
gr_make_@BASE_NAME@ (unsigned interpolation,
		     unsigned decimation,
		     const std::vector<@TAP_TYPE@> &taps);

class @FIR_TYPE@;

/*!
 * \brief Rational Resampling Polyphase FIR filter with @I_TYPE@ input, @O_TYPE@ output and @TAP_TYPE@ taps
 * \ingroup filter_blk
 */
class @NAME@ : public gr_block
{
 private:
  unsigned 			d_history;
  unsigned 			d_interpolation, d_decimation;
  unsigned 			d_ctr;
  std::vector<@TAP_TYPE@>	d_new_taps;
  bool				d_updated;
  std::vector<@FIR_TYPE@ *> d_firs;

  friend @SPTR_NAME@ 
  gr_make_@BASE_NAME@ (unsigned interpolation, unsigned decimation, const std::vector<@TAP_TYPE@> &taps);


  /*!
   * Construct a FIR filter with the given taps
   */
  @NAME@ (unsigned interpolation, unsigned decimation,
	  const std::vector<@TAP_TYPE@> &taps);

  void install_taps (const std::vector<@TAP_TYPE@> &taps);

 public:
  ~@NAME@ ();
  unsigned history () const { return d_history; }
  void  set_history (unsigned history) { d_history = history; }

  unsigned interpolation() const { return d_interpolation; }
  unsigned decimation() const { return d_decimation; }

  void set_taps (const std::vector<@TAP_TYPE@> &taps);

  void forecast (int noutput_items, gr_vector_int &ninput_items_required);
  int  general_work (int noutput_items,
		     gr_vector_int &ninput_items,
		     gr_vector_const_void_star &input_items,
		     gr_vector_void_star &output_items);
};
 

#endif
