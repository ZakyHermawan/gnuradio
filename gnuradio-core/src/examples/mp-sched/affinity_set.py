#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Affinity Set Test
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import blocks
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from optparse import OptionParser
import sys

class affinity_set(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Affinity Set Test")

        ##################################################
	# Variables
	##################################################
	self.samp_rate = samp_rate = 32000

	##################################################
	# Blocks
	##################################################
        vec_len = 1
	self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*vec_len, samp_rate)
	self.gr_null_source_0 = gr.null_source(gr.sizeof_gr_complex*vec_len)
	self.gr_null_sink_0 = gr.null_sink(gr.sizeof_gr_complex*vec_len)
	self.gr_filt_0 = gr.fir_filter_ccc(1, 40000*[0.2+0.3j,])
	self.gr_filt_1 = gr.fir_filter_ccc(1, 40000*[0.2+0.3j,])

	self.gr_filt_0.set_processor_affinity([0,])
	self.gr_filt_1.set_processor_affinity([0,1])
		
	##################################################
	# Connections
	##################################################
	self.connect((self.gr_null_source_0, 0), (self.blocks_throttle_0, 0))
	self.connect((self.blocks_throttle_0, 0), (self.gr_filt_0, 0))
	self.connect((self.gr_filt_0, 0), (self.gr_filt_1, 0))
	self.connect((self.gr_filt_1, 0), (self.gr_null_sink_0, 0))


	# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = affinity_set()
    tb.start()
	
    while(1):
        ret = raw_input('Press Enter to quit: ')
	if(len(ret) == 0):
            tb.stop()
	    sys.exit(0)
        elif(ret.lower() == "none"):
            tb.gr_filt_0.unset_processor_affinity()
	else:
            try:
                n = int(ret)
	    except ValueError:
                print "Invalid number"
	    else:
                tb.gr_filt_0.set_processor_affinity([n,])
