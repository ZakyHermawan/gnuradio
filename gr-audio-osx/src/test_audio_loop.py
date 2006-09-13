#!/usr/bin/env python
#
# Copyright 2006 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio.
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
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

from gnuradio import gr
from gnuradio import audio
from gnuradio.eng_option import eng_option
from optparse import OptionParser

class my_graph(gr.flow_graph):

    def __init__(self):
        gr.flow_graph.__init__(self)

        parser = OptionParser(option_class=eng_option)
        parser.add_option("-O", "--audio-output",
			  type="string",
			  default="",
                          help="audio output device name. E.g., hw:0,0 or /dev/dsp")
        parser.add_option("-I", "--audio-input",
			  type="string",
			  default="",
                          help="audio input device name.  E.g., hw:0,0 or /dev/dsp")
        parser.add_option("-r", "--sample-rate",
			  type="eng_float",
			  default=48000,
                          help="set sample rate to RATE (48000)")
        (options, args) = parser.parse_args ()
        if len(args) != 0:
            parser.print_help()
            raise SystemExit, 1

        sample_rate = int(options.sample_rate)
        src = audio.source (sample_rate, options.audio_output)
        dst = audio.sink (sample_rate, options.audio_output)

        max_chan = max (src.output_signature().max_streams(),
			dst.output_signature().max_streams())

	for i in range (max_chan):
		self.connect ((src, i), (dst, i))

if __name__ == '__main__':
    try:
        my_graph().run()
    except KeyboardInterrupt:
        pass
