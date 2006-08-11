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


#ifndef INCLUDED_TRELLIS_PERMUTATION_H
#define INCLUDED_TRELLIS_PERMUTATION_H

#include <vector>
#include <gr_sync_block.h>

class trellis_permutation;
typedef boost::shared_ptr<trellis_permutation> trellis_permutation_sptr;

trellis_permutation_sptr trellis_make_permutation (const int K, const std::vector<int> &TABLE, const size_t NBYTES);

/*!
 * \brief Permutation.
 * \ingroup block
 *
 * 
 */
class trellis_permutation : public gr_sync_block
{
private:
  friend trellis_permutation_sptr trellis_make_permutation (const int K, const std::vector<int> &TABLE, const size_t NBYTES);
  int d_K;
  std::vector<int> d_TABLE;
  size_t d_NBYTES;
  trellis_permutation (const int K, const std::vector<int> &TABLE, const size_t NBYTES); 

public:
  int K () const { return d_K; }
  const std::vector<int> & TABLE () const { return d_TABLE; }
  size_t NBYTES () const { return d_NBYTES; }

  int work (int noutput_items,
	    gr_vector_const_void_star &input_items,
	    gr_vector_void_star &output_items);
};

#endif
