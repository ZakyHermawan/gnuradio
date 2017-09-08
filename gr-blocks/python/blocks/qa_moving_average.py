#!/usr/bin/env python
#
# Copyright 2013,2017 Free Software Foundation, Inc.
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

    def test_03(self):
        tb = self.tb

        print "setting up"
        vlen = 5
        N = 10*vlen
        seed = 0
        data = make_random_float_tuple(N, 2**10)
        data = [int(d*1000) for d in data]
        print "making blocks"
        src = blocks.vector_source_i(data, False)
        one_to_many = blocks.stream_to_streams(gr.sizeof_int, vlen)
        one_to_vector = blocks.stream_to_vector(gr.sizeof_int, vlen)
        many_to_vector = blocks.streams_to_vector(gr.sizeof_int, vlen)
        isolated  = [ blocks.moving_average_ii(100, 1) for i in range(vlen)]
        dut = blocks.moving_average_ii(100, 1, vlen=vlen)
        dut_dst = blocks.vector_sink_i(vlen=vlen)
        ref_dst = blocks.vector_sink_i(vlen=vlen)

        print "connecting"
        tb.connect(src, one_to_many)
        tb.connect(src, one_to_vector, dut, dut_dst)
        tb.connect(many_to_vector, ref_dst)
        for idx, single in enumerate(isolated):
            tb.connect((one_to_many,idx), single, (many_to_vector,idx))


        print "running"
        tb.run()

        print "comparing"
        dut_data = dut_dst.data()
        ref_data = ref_dst.data()

        # make sure result is close to zero
        self.assertTupleEqual(dut_data, ref_data)
if __name__ == '__main__':
    gr_unittest.run(test_moving_average, "test_moving_average.xml")
