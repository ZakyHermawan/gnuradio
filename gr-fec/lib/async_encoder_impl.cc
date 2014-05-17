/* -*- c++ -*- */
/*
 * Copyright 2014 Free Software Foundation, Inc.
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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "async_encoder_impl.h"
#include <gnuradio/io_signature.h>
#include <volk/volk.h>
#include <stdio.h>

namespace gr {
  namespace fec {

    async_encoder::sptr
    async_encoder::make(generic_encoder::sptr my_encoder,
                        bool rev_unpack, bool rev_pack)
    {
      return gnuradio::get_initial_sptr
        (new async_encoder_impl(my_encoder, rev_unpack, rev_pack));
    }

    async_encoder_impl::async_encoder_impl(generic_encoder::sptr my_encoder,
                                           bool rev_unpack, bool rev_pack)
      : block("async_encoder",
              io_signature::make(0,0,0),
              io_signature::make(0,0,0)),
        d_input_item_size(sizeof(char)), d_output_item_size(sizeof(char))
    {
      d_in_port = pmt::mp("in");
      d_out_port = pmt::mp("out");

      d_encoder = my_encoder;
      d_unpack = new blocks::kernel::unpack_k_bits(8);
      d_pack   = new blocks::kernel::pack_k_bits(8);

      d_rev_unpack = rev_unpack;
      d_rev_pack = rev_pack;

      message_port_register_in(d_in_port);
      message_port_register_out(d_out_port);
      set_msg_handler(d_in_port, boost::bind(&async_encoder_impl::encode, this ,_1) );
    }

    async_encoder_impl::~async_encoder_impl()
    {
      delete d_unpack;
      delete d_pack;
    }

    void
    async_encoder_impl::encode(pmt::pmt_t msg)
    {
      // extract input pdu
      pmt::pmt_t meta(pmt::car(msg));
      pmt::pmt_t bytes(pmt::cdr(msg));

      int nbytes = pmt::length(bytes);
      int nbits = 8*nbytes;
      size_t o0 = 0;
      const uint8_t* bytes_in = pmt::u8vector_elements(bytes, o0);
      uint8_t* bits_in = (uint8_t*)volk_malloc(nbits*sizeof(uint8_t),
                                               volk_get_alignment());

      // Encoder takes a stream of bits, but PDU's are received as
      // bytes, so we unpack them here.
      if(d_rev_unpack)
        d_unpack->unpack_rev(bits_in, bytes_in, nbytes);
      else
        d_unpack->unpack(bits_in, bytes_in, nbytes);

      d_encoder->set_frame_size(nbits);

      int nbits_out = d_encoder->get_output_size();
      int nbytes_out = nbits_out/8;

      // buffers for bits/bytes to go to
      uint8_t* bits_out = (uint8_t*)volk_malloc(nbits_out*sizeof(uint8_t),
                                                volk_get_alignment());

      pmt::pmt_t outvec = pmt::make_u8vector(nbytes_out, 0x00);
      uint8_t* bytes_out = pmt::u8vector_writable_elements(outvec, o0);

      // ENCODE!
      d_encoder->generic_work((void*)bits_in, (void*)bits_out);

      // Encoder produces bits, so repack them here to bytes.
      if(d_rev_pack)
        d_pack->pack_rev(bytes_out, bits_out, nbytes_out);
      else
        d_pack->pack(bytes_out, bits_out, nbytes_out);

      pmt::pmt_t msg_pair = pmt::cons(meta, outvec);
      message_port_pub(d_out_port, msg_pair);

      volk_free(bits_in);
      volk_free(bits_out);
    }

    int
    async_encoder_impl::general_work(int noutput_items,
                                     gr_vector_int& ninput_items,
                                     gr_vector_const_void_star &input_items,
                                     gr_vector_void_star &output_items)
    {
      return noutput_items;
    }

  } /* namespace fec */
} /* namespace gr */
