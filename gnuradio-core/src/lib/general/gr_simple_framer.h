/* -*- c++ -*- */
/*
 * Copyright 2004 Free Software Foundation, Inc.
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

#ifndef INCLUDED_GR_SIMPLE_FRAMER_H
#define INCLUDED_GR_SIMPLE_FRAMER_H

#include <gr_block.h>

class gr_simple_framer;
typedef boost::shared_ptr<gr_simple_framer> gr_simple_framer_sptr;

gr_simple_framer_sptr gr_make_simple_framer (int payload_bytesize);

/*!
 * \brief add sync field, seq number and command field to payload
 * \ingroup block
 */
class gr_simple_framer : public gr_block
{
  int	d_seqno;
  int	d_payload_bytesize;
  int	d_input_block_size;	// bytes
  int	d_output_block_size;	// bytes

  friend gr_simple_framer_sptr gr_make_simple_framer (int payload_bytesize);
  gr_simple_framer (int payload_bytesize);

 public:
  void forecast (int noutput_items,
		 gr_vector_int &ninput_items_required);

  int general_work (int noutput_items,
		    gr_vector_int &ninput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items);
};


#endif /* INCLUDED_GR_SIMPLE_FRAMER_H */
