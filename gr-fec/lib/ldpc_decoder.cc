/* -*- c++ -*- */
/*
 * Copyright 2015 Free Software Foundation, Inc.
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

#include <gnuradio/fec/ldpc_decoder.h>
#include <math.h>
#include <boost/assign/list_of.hpp>
#include <volk/volk.h>
#include <sstream>
#include <stdio.h>
#include <vector>
#include <gnuradio/fec/decoder.h>
#include <algorithm>            // for std::reverse
#include <string.h>             // for memcpy
#include <gnuradio/fec/maxstar.h>


namespace gr {
 namespace fec {

generic_decoder::sptr
ldpc_decoder::make(std::string alist_file, float sigma, int max_iterations)
{
    return generic_decoder::sptr(new ldpc_decoder(alist_file, sigma, max_iterations));
}

ldpc_decoder::ldpc_decoder (std::string alist_file, float sigma, int max_iterations)
    : generic_decoder("ldpc_decoder")
{
        d_list.read(alist_file.c_str());
        d_code.set_alist(d_list);
        d_spa.set_alist_sigma(d_list, sigma);
        inputSize = d_code.get_N();
        outputSize = d_code.dimension();
        d_spa.set_K(outputSize);
        d_spa.set_max_iterations(max_iterations);
}

int ldpc_decoder::get_output_size() {
    return outputSize;
}

int ldpc_decoder::get_input_size() {
    return inputSize;
}

void ldpc_decoder::generic_work(void *inBuffer, void *outBuffer) {
    const float *inPtr = (const float *) inBuffer;
    unsigned char *out = (unsigned char *) outBuffer;
 
    std::vector<float> rx(inputSize);
    for(int i=0; i<inputSize; i++){ rx[i] = inPtr[i] * (-1); }
    //memcpy(&rx[0], inPtr, inputSize*sizeof(float));
    int n_iterations = 0;
    std::vector<char> estimate( d_spa.decode(rx, &n_iterations) );   
    std::vector<char> data( d_code.get_systematic_bits(estimate) );
    memcpy(out, &data[0], outputSize);
}

int ldpc_decoder::get_input_item_size() {
    return sizeof(INPUT_DATATYPE);
}

int ldpc_decoder::get_output_item_size() {
    return sizeof(OUTPUT_DATATYPE);
}

int ldpc_decoder::get_history() {
    return 0;
}

float ldpc_decoder::get_shift() {
    return 0.0;
}

const char* ldpc_decoder::get_conversion() {
    return "none";
}

ldpc_decoder::~ldpc_decoder() {
}

}
}
