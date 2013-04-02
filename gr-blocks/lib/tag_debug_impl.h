/* -*- c++ -*- */
/*
 * Copyright 2012-2013 Free Software Foundation, Inc.
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

#ifndef INCLUDED_GR_TAG_DEBUG_IMPL_H
#define INCLUDED_GR_TAG_DEBUG_IMPL_H

#include <blocks/tag_debug.h>
#include <thread/thread.h>
#include <stddef.h>

namespace gr {
  namespace blocks {

    class tag_debug_impl : public tag_debug
    {
    private:
      std::string d_name;
      std::vector<gr_tag_t> d_tags;
      std::vector<gr_tag_t>::iterator d_tags_itr;
      bool d_display;
      gr::thread::mutex d_mutex;

    public:
      tag_debug_impl(size_t sizeof_stream_item, const std::string &name);
      ~tag_debug_impl();

      std::vector<gr_tag_t> current_tags();

      void set_display(bool d);

      int work(int noutput_items,
               gr_vector_const_void_star &input_items,
               gr_vector_void_star &output_items);
    };

  } /* namespace blocks */
} /* namespace gr */

#endif /* INCLUDED_GR_TAG_DEBUG_IMPL_H */
