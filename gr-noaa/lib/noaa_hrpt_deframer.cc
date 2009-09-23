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
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <noaa_hrpt_deframer.h>
#include <gr_io_signature.h>
#include <cstring>

#define ST_IDLE   0
#define ST_SYNCED 1

#define SYNC1 0x0284
#define SYNC2 0x016F
#define SYNC3 0x035C
#define SYNC4 0x019D
#define SYNC5 0x020F
#define SYNC6 0x0095

#define HRPT_MINOR_FRAME_SYNC  0x0A116FD719D83C95LL

static int frames_seen = 0;

noaa_hrpt_deframer_sptr
noaa_make_hrpt_deframer()
{
  return gnuradio::get_initial_sptr(new noaa_hrpt_deframer());
}

noaa_hrpt_deframer::noaa_hrpt_deframer()
  : gr_block("noaa_hrpt_deframer",
	     gr_make_io_signature(1, 1, sizeof(char)),
	     gr_make_io_signature(1, 1, sizeof(short)))
{
  set_output_multiple(6); // room for writing full sync when received
  enter_idle();
}

void
noaa_hrpt_deframer::enter_idle()
{
  d_state = ST_IDLE;
}

void
noaa_hrpt_deframer::enter_synced()
{
  d_state = ST_SYNCED;
  d_bit_count = HRPT_BITS_PER_WORD;
  d_word_count = HRPT_MINOR_FRAME_WORDS-HRPT_SYNC_WORDS;
  d_word = 0;
}

int
noaa_hrpt_deframer::general_work(int noutput_items,
				 gr_vector_int &ninput_items,
				 gr_vector_const_void_star &input_items,
				 gr_vector_void_star &output_items)
{
  int ninputs = ninput_items[0];
  const char *in = (const char *)input_items[0];
  unsigned short *out = (unsigned short *)output_items[0];

  int i = 0, j = 0;
  while (i < ninputs && j < noutput_items) {
    char bit = in[i++];

    switch (d_state) {
    case ST_IDLE:
      d_shifter = (d_shifter << 1) | bit; // MSB transmitted first
      
      if ((d_shifter & 0x0FFFFFFFFFFFFFFF) == HRPT_MINOR_FRAME_SYNC) {
	fprintf(stderr, "SYNC #%i", frames_seen++);
	out[j++] = SYNC1;
	out[j++] = SYNC2;
	out[j++] = SYNC3;
	out[j++] = SYNC4;
	out[j++] = SYNC5;
	out[j++] = SYNC6;
	enter_synced();
      }
      break;

    case ST_SYNCED:
      d_word = (d_word << 1) | bit; // MSB transmitted first
      if (--d_bit_count == 0) {
	out[j++] = d_word;
	d_word = 0;
	d_bit_count = HRPT_BITS_PER_WORD;
	if (--d_word_count == 0) {
	  fprintf(stderr, "...done\n");
	  enter_idle();
	}
      }
      break;

    default:
      throw std::runtime_error("noaa_hrpt_deframer: bad state\n");
    }
  }

  consume_each(i);
  return j;
}
