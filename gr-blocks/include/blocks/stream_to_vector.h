/* -*- c++ -*- */
/*
 * Copyright 2012 Free Software Foundation, Inc.
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

#ifndef INCLUDED_BLOCKS_STREAM_TO_VECTOR_H
#define INCLUDED_BLOCKS_STREAM_TO_VECTOR_H

#include <blocks/api.h>
#include <gr_sync_decimator.h>

namespace gr {
  namespace blocks {

    /*!
     * \brief convert a stream of items into a stream of blocks containing nitems_per_block
     * \ingroup slicedice_blk
     */
    class BLOCKS_API stream_to_vector : virtual public gr_sync_decimator
    {
    public:
      
      // gr::blocks::stream_to_vector::sptr
      typedef boost::shared_ptr<stream_to_vector> sptr;

      static sptr make(size_t itemsize, size_t nitems_per_block);
    };

  } /* namespace blocks */
} /* namespace gr */

#endif /* INCLUDED_BLOCKS_STREAM_TO_VECTOR_H */
