#!/usr/bin/env python
#
# Copyright 2011 Free Software Foundation, Inc.
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

from gnuradio import gr, blks2, gr_unittest
import digital_swig
import random, cmath

class test_digital(gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test01 (self):
        # test basic functionality by setting all gains to 0
        damp = 0.4
        natfreq = 0.25
        order = 2
        self.test = digital_swig.costas_loop_cc(damp, natfreq, order)

        data = 100*[complex(1,0),]
        self.src = gr.vector_source_c(data, False)
        self.snk = gr.vector_sink_c()

        self.tb.connect(self.src, self.test, self.snk)
        self.tb.run()
        
        expected_result = data
        dst_data = self.snk.data()
        self.assertComplexTuplesAlmostEqual (expected_result, dst_data, 5)

    def test02 (self):
        # Make sure it doesn't diverge given perfect data
        damp = 0.4
        natfreq = 0.25
        order = 2
        self.test = digital_swig.costas_loop_cc(damp, natfreq, order)

        data = [complex(2*random.randint(0,1)-1, 0) for i in xrange(100)]
        self.src = gr.vector_source_c(data, False)
        self.snk = gr.vector_sink_c()

        self.tb.connect(self.src, self.test, self.snk)
        self.tb.run()

        expected_result = data
        dst_data = self.snk.data()

        self.assertComplexTuplesAlmostEqual (expected_result, dst_data, 5)

    def test03 (self):
        # BPSK Convergence test with static rotation
        damp = 0.4
        natfreq = 0.25
        order = 2
        self.test = digital_swig.costas_loop_cc(damp, natfreq, order)

        rot = cmath.exp(0.2j) # some small rotation
        data = [complex(2*random.randint(0,1)-1, 0) for i in xrange(100)]
        
        N = 40 # settling time
        expected_result = data[N:]
        data = [rot*d for d in data]

        self.src = gr.vector_source_c(data, False)
        self.snk = gr.vector_sink_c()

        self.tb.connect(self.src, self.test, self.snk)
        self.tb.run()

        dst_data = self.snk.data()[N:]
        
        # generously compare results; the loop will converge near to, but
        # not exactly on, the target data
        self.assertComplexTuplesAlmostEqual (expected_result, dst_data, 2)

    def test04 (self):
        # QPSK Convergence test with static rotation
        damp = 0.4
        natfreq = 0.25
        order = 4
        self.test = digital_swig.costas_loop_cc(damp, natfreq, order)

        rot = cmath.exp(0.2j) # some small rotation
        data = [complex(2*random.randint(0,1)-1, 2*random.randint(0,1)-1)
                for i in xrange(100)]
        
        N = 40 # settling time
        expected_result = data[N:]
        data = [rot*d for d in data]

        self.src = gr.vector_source_c(data, False)
        self.snk = gr.vector_sink_c()

        self.tb.connect(self.src, self.test, self.snk)
        self.tb.run()

        dst_data = self.snk.data()[N:]

        # generously compare results; the loop will converge near to, but
        # not exactly on, the target data
        self.assertComplexTuplesAlmostEqual (expected_result, dst_data, 2)

    def test05 (self):
        # 8PSK Convergence test with static rotation
        damp = 0.5
        natfreq = 0.5
        order = 8
        self.test = digital_swig.costas_loop_cc(damp, natfreq, order)

        rot = cmath.exp(-cmath.pi/8.0j) # rotate to match Costas rotation
        const = blks2.psk.make_constellation(order)
        data = [random.randint(0,7) for i in xrange(100)]
        data = [2*rot*const[d] for d in data]
        
        N = 40 # settling time
        expected_result = data[N:]

        rot = cmath.exp(0.1j) # some small rotation
        data = [rot*d for d in data]

        self.src = gr.vector_source_c(data, False)
        self.snk = gr.vector_sink_c()

        self.tb.connect(self.src, self.test, self.snk)
        self.tb.run()

        dst_data = self.snk.data()[N:]
        
        # generously compare results; the loop will converge near to, but
        # not exactly on, the target data
        self.assertComplexTuplesAlmostEqual (expected_result, dst_data, 2)

if __name__ == '__main__':
    gr_unittest.run(test_digital, "test_digital.xml")
