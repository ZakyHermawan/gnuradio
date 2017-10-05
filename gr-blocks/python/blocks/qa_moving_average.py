#!/usr/bin/env python
#
# Copyright 2013 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

from gnuradio import gr, gr_unittest, blocks

import math, random

def make_random_complex_tuple(L, scale=1):
    result = []
    for x in range(L):
        result.append(scale*complex(2*random.random()-1,
                                    2*random.random()-1))
    return tuple(result)

def make_random_float_tuple(L, scale=1):
    result = []
    for x in range(L):
        result.append(scale*(2*random.random()-1))
    return tuple(result)

class test_moving_average(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    # These tests will always pass and are therefore useless. 100 random numbers [-1,1) are
    # getting summed up and scaled with 0.001. Then, an assertion verifies a result near 0,
    # which is the case even if the block is malfunctioning.

    def test_01(self):
        tb = self.tb

        N = 10000
        seed = 0
        data = make_random_float_tuple(N, 1)
        expected_result = N*[0,]

        src = blocks.vector_source_f(data, False)
        op  = blocks.moving_average_ff(100, 0.001)
        dst = blocks.vector_sink_f()

        tb.connect(src, op)
        tb.connect(op, dst)
        tb.run()

        dst_data = dst.data()

        # make sure result is close to zero
        self.assertFloatTuplesAlmostEqual(expected_result, dst_data, 1)

    def test_02(self):
        tb = self.tb

        N = 10000
        seed = 0
        data = make_random_complex_tuple(N, 1)
        expected_result = N*[0,]

        src = blocks.vector_source_c(data, False)
        op  = blocks.moving_average_cc(100, 0.001)
        dst = blocks.vector_sink_c()

        tb.connect(src, op)
        tb.connect(op, dst)
        tb.run()

        dst_data = dst.data()

        # make sure result is close to zero
        self.assertComplexTuplesAlmostEqual(expected_result, dst_data, 1)

    # This tests implement own moving average to verify correct behaviour of the block

    def test_03(self):
        tb = self.tb

        N = 10000  # number of samples
        history = 100  # num of samples to average
        data = make_random_float_tuple(N, 1)  # generate random data

        #  pythonic MA filter
        data_padded = (history-1)*[0.0]+list(data)  # history  
        expected_result = []
        moving_sum = sum(data_padded[:history-1])
        for i in range(N):
            moving_sum += data_padded[i+history-1]
            expected_result.append(moving_sum)
            moving_sum -= data_padded[i]

        src = blocks.vector_source_f(data, False)
        op  = blocks.moving_average_ff(history, 1)
        dst = blocks.vector_sink_f()
        
        tb.connect(src, op)
        tb.connect(op, dst)
        tb.run()
    
        dst_data = dst.data()

        # make sure result is close to zero
        self.assertFloatTuplesAlmostEqual(expected_result, dst_data, 4)

    def test_04(self):
        tb = self.tb

        N = 10000  # number of samples
        history = 100  # num of samples to average
        data = make_random_complex_tuple(N, 1)  # generate random data

        #  pythonic MA filter
        data_padded = (history-1)*[0.0+1j*0.0]+list(data)  # history  
        expected_result = []
        moving_sum = sum(data_padded[:history-1])
        for i in range(N):
            moving_sum += data_padded[i+history-1]
            expected_result.append(moving_sum)
            moving_sum -= data_padded[i]

        src = blocks.vector_source_c(data, False)
        op  = blocks.moving_average_cc(history, 1)
        dst = blocks.vector_sink_c()
        
        tb.connect(src, op)
        tb.connect(op, dst)
        tb.run()
    
        dst_data = dst.data()

        # make sure result is close to zero
        self.assertComplexTuplesAlmostEqual(expected_result, dst_data, 4)


if __name__ == '__main__':
    gr_unittest.run(test_moving_average, "test_moving_average.xml")
