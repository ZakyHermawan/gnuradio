/* -*- c++ -*- */
/*
 * Copyright 2006, 2011 Free Software Foundation, Inc.
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

#ifndef INCLUDED_GR_CONSTELLATION_DECODER2_CB_H
#define INCLUDED_GR_CONSTELLATION_DECODER2_CB_H

#include <gr_block.h>
#include <gr_constellation.h>
#include <vector>

class gr_constellation_decoder2_cb;
typedef boost::shared_ptr<gr_constellation_decoder2_cb> gr_constellation_decoder2_cb_sptr;

gr_constellation_decoder2_cb_sptr 
gr_make_constellation_decoder2_cb (gr_constellation_sptr constellation);

/*!
 * \brief Constellation Decoder
 * \ingroup coding_blk
 *
 */
class gr_constellation_decoder2_cb : public gr_block
{

 private:
  gr_constellation_sptr d_constellation;
  unsigned int d_dim;

  friend gr_constellation_decoder2_cb_sptr 
  gr_make_constellation_decoder2_cb (gr_constellation_sptr constellation);
  
  gr_constellation_decoder2_cb (gr_constellation_sptr constellation);

 public:

  void forecast (int noutput_items,
		 gr_vector_int &ninput_items_required);
  
  int general_work (int noutput_items,
		    gr_vector_int &ninput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items);
};

#endif
