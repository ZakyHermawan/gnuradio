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

#ifndef INCLUDED_GR_BURST_TAGGER_H
#define INCLUDED_GR_BURST_TAGGER_H

#include <gr_sync_block.h>

class gr_burst_tagger;
typedef boost::shared_ptr<gr_burst_tagger> gr_burst_tagger_sptr;

gr_burst_tagger_sptr gr_make_burst_tagger(size_t itemsize);

/*!
 * \brief output[i] = input[i]
 * \ingroup misc_blk
 *
 */
class gr_burst_tagger : public gr_sync_block
{
  size_t		d_itemsize;
  bool                  d_state;
  pmt::pmt_t            d_key;
  pmt::pmt_t            d_id;

  friend gr_burst_tagger_sptr gr_make_burst_tagger(size_t itemsize);
  gr_burst_tagger(size_t itemsize);

 public:
  ~gr_burst_tagger();

  int work(int noutput_items,
	   gr_vector_const_void_star &input_items,
	   gr_vector_void_star &output_items);
};

#endif
