/* -*- c++ -*- */
/*
 * Copyright 2013,2014 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "pub_sink_impl.h"

namespace gr {
  namespace zeromq {

    pub_sink::sptr
    pub_sink::make(size_t itemsize, size_t vlen, char *address, bool blocking)
    {
      return gnuradio::get_initial_sptr
	(new pub_sink_impl(itemsize, vlen, address, blocking));
    }

    pub_sink_impl::pub_sink_impl(size_t itemsize, size_t vlen, char *address, bool blocking)
      : gr::sync_block("pub_sink",
                       gr::io_signature::make(1, 1, itemsize * vlen),
                       gr::io_signature::make(0, 0, 0)),
        d_itemsize(itemsize), d_vlen(vlen), d_blocking(blocking)
    {
      d_context = new zmq::context_t(1);
      d_socket = new zmq::socket_t(*d_context, ZMQ_PUB);
      int time = 0;
      d_socket->setsockopt(ZMQ_LINGER, &time, sizeof(time));
      d_socket->bind(address);
    }

    pub_sink_impl::~pub_sink_impl()
    {
      delete d_socket;
      delete d_context;
    }

    int
    pub_sink_impl::work(int noutput_items,
                        gr_vector_const_void_star &input_items,
                        gr_vector_void_star &output_items)
    {
      const char *in = (const char *)input_items[0];

      // create message copy and send
      zmq::message_t msg(d_itemsize*d_vlen*noutput_items);
      memcpy((void *)msg.data(), in, d_itemsize*d_vlen*noutput_items);
      d_socket->send(msg, d_blocking ? 0 : ZMQ_NOBLOCK);

      return noutput_items;
    }

  } /* namespace zeromq */
} /* namespace gr */
