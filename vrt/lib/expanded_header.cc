/* -*- c++ -*- */
/*
 * Copyright 2009 Free Software Foundation, Inc.
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
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif
#include <vrt/expanded_header.h>
#include <gruel/inet.h>
#include <boost/format.hpp>
#include "header_utils.h"

using boost::format;
using boost::io::group;


namespace vrt {

  using namespace detail;

  // lookup tables indexed by packet type
  unsigned char expanded_header::s_if_data[16] = {
    1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  };

  unsigned char expanded_header::s_ext_data[16] = {
    0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  };

  unsigned char expanded_header::s_data[16] = {
    1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  };

  unsigned char expanded_header::s_context[16] = {
    0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  };

  unsigned char expanded_header::s_stream_id[16] = {
    0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  };


  // dispatch codeword bits
  static const int HAS_STREAM_ID       = 1 << 0;
  static const int HAS_CLASS_ID        = 1 << 1;
  static const int HAS_INTEGER_SECS    = 1 << 2;
  static const int HAS_FRACTIONAL_SECS = 1 << 3;
  static const int HAS_TRAILER         = 1 << 4;

  static int
  compute_codeword(const expanded_header &h)
  {
    int cw = 0;
    if (h.stream_id_p())       cw |= HAS_STREAM_ID;
    if (h.class_id_p())        cw |= HAS_CLASS_ID;
    if (h.integer_secs_p())    cw |= HAS_INTEGER_SECS;
    if (h.fractional_secs_p()) cw |= HAS_FRACTIONAL_SECS;
    if (h.trailer_p())         cw |= HAS_TRAILER;
    return cw;
  }

  void expanded_header::pack(const expanded_header *h,      	// in
			     size_t n32_bit_words_payload,  	// in
			     uint32_t *header,              	// out
			     size_t *n32_bit_words_header,  	// out
			     uint32_t *trailer,             	// out
			     size_t *n32_bit_words_trailer)	// out
  {
    int cw = compute_codeword(*h);
    //fills in the header (except word0), header length, trailer, trailer length
    switch (cw & 0x1f){
#include "expanded_header_pack_switch_body.h"
    }
    //fill in the header word 0 with the calculated length
    size_t n32_bit_words_packet = *n32_bit_words_header + n32_bit_words_payload + *n32_bit_words_trailer;
    header[0] = htonl((h->header & ~VRTH_PKT_SIZE_MASK) | (n32_bit_words_packet & VRTH_PKT_SIZE_MASK));
  }

  bool 
  expanded_header::unpack(const uint32_t *packet,		// in
			  size_t n32_bit_words_packet,		// in
			  expanded_header *h,			// out
			  const uint32_t **payload,		// out
			  size_t *n32_bit_words_payload)	// out
  {
    size_t n32_bit_words_header = 0;
    size_t n32_bit_words_trailer = 0;
    size_t len = n32_bit_words_packet;
    const uint32_t *p = packet;

    *payload = 0;
    *n32_bit_words_payload = 0;

    // printf("unpack: n32_bit_words_packet = %zd\n", n32_bit_words_packet);

    if (len < 1){		// must have at least the header word
      h->header = 0;
      return false;
    }

    h->header = ntohl(p[0]);

    if (h->pkt_size() > len)
      return false;		// VRT header says packet is bigger than what we've got

    len = h->pkt_size();	// valid length of packet

    int cw = compute_codeword(*h);
    switch (cw & 0x1f){
#include "expanded_header_unpack_switch_body.h"
    }

    if (n32_bit_words_header + n32_bit_words_trailer > len)
      return false;		// negative payload len

    *payload = p + n32_bit_words_header;
    *n32_bit_words_payload = len - (n32_bit_words_header + n32_bit_words_trailer);

    // printf("unpack: hdr = 0x%08x, cw = 0x%02x, n32_bit_words_header = %d, n32_bit_words_trailer = %d\n",
    //   h->header, cw, n32_bit_words_header, n32_bit_words_trailer);

    return true;
  }

  std::string
  pkt_type_name(const vrt::expanded_header *hdr)
  {
    if (hdr->if_data_p())
      return "IF-Data";
    if (hdr->ext_data_p())
      return "Ext-Data";
    if (hdr->if_context_p())
      return "IF-Context";
    if (hdr->ext_context_p())
      return "Ext-Context";
    else
      return "<unknown pkt type>";
  }

  static void wr_name(std::ostream &os, const std::string &x)
  {
    os << format("  %-19s  ") % (x + ":");
  }

  static void wr_uint32(std::ostream &os, uint32_t x)
  {
    os << format("%#10x") % x;
    os << std::endl;
  }

  void
  expanded_header::write(std::ostream &port) const
  {
    port << format("%s:\n") % pkt_type_name(this);
    if (1){
      wr_name(port, "header");
      wr_uint32(port, header);
    }

    if (stream_id_p()){
      wr_name(port, "stream_id");
      wr_uint32(port, stream_id);
    }

    if (class_id_p()){
      wr_name(port, "class_id");
      port << format("0x%016llx\n") % class_id;
    }

    if (integer_secs_p()){
      wr_name(port, "int secs");
      //port << format("%10d\n") % integer_secs;
      wr_int_secs(port, integer_secs);
    }

    if (fractional_secs_p()){
      wr_name(port, "frac secs");
      port << format("%10d\n") % fractional_secs;
    }
  }

  std::ostream& operator<<(std::ostream &os, const expanded_header &obj)
  {
    obj.write(os);
    return os;
  }

}; // vrt
