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
 * the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

#ifndef INCLUDED_GR_BINARY_SLICER_FB_H
#define INCLUDED_GR_BINARY_SLICER_FB_H

#include <gr_sync_block.h>

class gr_binary_slicer_fb;
typedef boost::shared_ptr<gr_binary_slicer_fb> gr_binary_slicer_fb_sptr;

gr_binary_slicer_fb_sptr gr_make_binary_slicer_fb ();

/*!
 * \brief slice float binary symbol outputting 1 bit output
 * \ingroup block
 *
 * x <  0 --> 0
 * x >= 0 --> 1
 */
class gr_binary_slicer_fb : public gr_sync_block
{
  friend gr_binary_slicer_fb_sptr gr_make_binary_slicer_fb ();
  gr_binary_slicer_fb ();

 public:
  int work (int noutput_items,
	    gr_vector_const_void_star &input_items,
	    gr_vector_void_star &output_items);
};

#endif
