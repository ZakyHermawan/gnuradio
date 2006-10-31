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
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_PAGER_FLEX_SYNC_H
#define INCLUDED_PAGER_FLEX_SYNC_H

#include <gr_block.h>

class pager_flex_sync;
typedef boost::shared_ptr<pager_flex_sync> pager_flex_sync_sptr;
typedef std::vector<gr_int64> gr_int64_vector;

pager_flex_sync_sptr pager_make_flex_sync(int rate);

/*!
 * \brief flex sync description
 * \ingroup block
 */

class pager_flex_sync : public gr_block
{
private:
    // Constructors
    friend pager_flex_sync_sptr pager_make_flex_sync(int rate);
    pager_flex_sync(int rate);
   
    // State machine transitions
    void enter_idle();
    void enter_syncing();
    void enter_sync1();
    void enter_sync2();
    void enter_data();

    int index_avg(int start, int end);
    bool test_sync(unsigned char sym);
    void parse_fiw();
    int output_symbol(unsigned char sym);    
    
    // Simple state machine
    enum state_t { ST_IDLE, ST_SYNCING, ST_SYNC1, ST_SYNC2, ST_DATA };
    state_t d_state;     

    int d_rate;     // Incoming sample rate
    int d_index;    // Index into current baud
    int d_start;    // Start of good sync 
    int d_center;   // Center of bit
    int d_end;      // End of good sync
    int d_count;    // Bit counter

    int d_mode;     // Current packet mode
    int d_baudrate; // Current decoding baud rate
    int d_levels;   // Current decoding levels
    int d_spb;      // Current samples per baud
    bool d_hibit;   // Alternating bit indicator for 3200 bps
    
    gr_int32 d_fiw; // Frame information word
    int d_frame;    // Current FLEX frame
    int d_cycle;    // Current FLEX cycle
    int d_unknown1;
    int d_unknown2;

    unsigned char d_bit_a;
    unsigned char d_bit_b;
    unsigned char d_bit_c;
    unsigned char d_bit_d;
    
    unsigned char *d_phase_a;  
    unsigned char *d_phase_b;
    unsigned char *d_phase_c;
    unsigned char *d_phase_d;
    
    gr_int64_vector d_sync; // Trial synchronizers

public:
    void forecast(int noutput_items, gr_vector_int &inputs_required);

    int general_work(int noutput_items,
                     gr_vector_int &ninput_items,
                     gr_vector_const_void_star &input_items, 
                     gr_vector_void_star &output_items);
};

#endif /* INCLUDED_PAGER_FLEX_SYNC_H */
