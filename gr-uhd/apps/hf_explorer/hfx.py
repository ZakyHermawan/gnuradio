#!/usr/bin/python
#!/usr/bin/env python
# generated by wxGlade 0.4 on Tue Mar 14 10:16:06 2006
#
# Copyright 2006,2011 Free Software Foundation, Inc.
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
#-----------------------------------------------------------------
#
#                 +-->(fft)
#                 |
# (src)->(xlate)--+->(audio filter)--+-->(sel_am)-+--------------+
#                                    |            |              |
#                                    |          (pll)            |
#                                    |            |              |
#                                    |   (pll_carrier_scale)     |
#                                    |            |              |
#                                    |   (pll_carrier_filter)    |
#                                    |            |              |
#                                    |            +--(fft2)      |
#                                    |            |              |
#                                    |       +--(c2f3)--+        |
#                                    |       |          |        |
#                                    |   (phaser1)  (phaser2)    |
#                                    |       |          |        |
#                                    |       +--(f2c)---+        |
#                                    |            |              V
#                                    V            +---------->(am_det)
#                                  (c2f)                         |
#                                    |                         (c2f2)
#                                    |                           |
#                                    +-->(sel_sb)------------>(combine)
#                                                                |
#                                                                V
#                                  +--------------------------(scale)
#                                  |                             |
#                                  |                             |
#                                  |                            +++
#                                  V                            | |
#                                (agc)<--(offset)<--(intr)<---(sqr1)
#                                  |
#                                  V
#                                (dst)
#
#----------------------------------------------------------------------
#
# 3.0.1 - updated to support uhd correctly, old code for usrp had display negative, removed antenna tuner controls
#

# Web server control disabled by default. Do not enable
# until directory structure and scripts are in place.
WEB_CONTROL = False

import os, wx, sys, math
import wx.lib.evtmgr as em
from gnuradio.wxgui import powermate, fftsink2
from gnuradio import gr, audio, eng_notation
from gnuradio import analog
from gnuradio import filter
from gnuradio import blocks
from gnuradio.eng_option import eng_option
from gnuradio import uhd
from optparse import OptionParser

n2s = eng_notation.num_to_str

ID_BUTTON_1 = wx.NewId()	# LSB button
ID_BUTTON_2 = wx.NewId()	# USB
ID_BUTTON_3 = wx.NewId()	# AM
ID_BUTTON_4 = wx.NewId()	# CW
ID_BUTTON_5 = wx.NewId()	# Powermate controls: Upper audio freq cutoff
ID_BUTTON_6 = wx.NewId()	#  "                  Lower audio freq cutoff
ID_BUTTON_7 = wx.NewId()	#  "                  Frequency
ID_BUTTON_8 = wx.NewId()	#  "                  Volume
ID_BUTTON_9 = wx.NewId()	#  "                  Time
ID_BUTTON_10 = wx.NewId()	# Time Seek Forwards
ID_BUTTON_11 = wx.NewId()	# Time Seek Backwards
ID_TEXT_1 = wx.NewId()		# Band Center, USRP ddc Freq
ID_SPIN_1 = wx.NewId()		# Frequency display and control
ID_SLIDER_1 = wx.NewId()	# Upper audio freq cutoff
ID_SLIDER_2 = wx.NewId()	# Lower audio freq cutoff
ID_SLIDER_3 = wx.NewId()	# Frequency
ID_SLIDER_4 = wx.NewId()	# Volume
ID_SLIDER_5 = wx.NewId()	# Programmable Gain Amp, PGA, RF gain
ID_SLIDER_7 = wx.NewId()	# AT control voltage output
ID_EXIT	= wx.NewId()		# Menu Exit


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        # Menu Bar
        self.frame_1_menubar = wx.MenuBar()
        self.SetMenuBar(self.frame_1_menubar)
        wxglade_tmp_menu = wx.Menu()
        self.Exit = wx.MenuItem(wxglade_tmp_menu, ID_EXIT, "Exit",
                                "Exit", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.Exit)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "File")
        # Menu Bar end
        self.panel_1 = wx.Panel(self, -1)
        self.button_1 = wx.Button(self, ID_BUTTON_1, "LSB")
        self.button_2 = wx.Button(self, ID_BUTTON_2, "USB")
        self.button_3 = wx.Button(self, ID_BUTTON_3, "AM")
        self.button_4 = wx.Button(self, ID_BUTTON_4, "CW")
        self.button_5 = wx.ToggleButton(self, ID_BUTTON_5, "Upper")
        self.slider_fcutoff_hi = wx.Slider(self, ID_SLIDER_1, 0, -15798, 15799,
                                  style=wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.button_6 = wx.ToggleButton(self, ID_BUTTON_6, "Lower")
        self.slider_fcutoff_lo = wx.Slider(self, ID_SLIDER_2, 0, -15799, 15798,
                                  style=wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.panel_5 = wx.Panel(self, -1)
        self.label_1 = wx.StaticText(self, -1, " Band\nCenter")
        self.text_ctrl_1 = wx.TextCtrl(self, ID_TEXT_1, "")
        self.panel_6 = wx.Panel(self, -1)
        self.panel_7 = wx.Panel(self, -1)
        self.panel_2 = wx.Panel(self, -1)
        self.button_7 = wx.ToggleButton(self, ID_BUTTON_7, "Freq")
        self.slider_3 = wx.Slider(self, ID_SLIDER_3, 3000, 0, 6000)
        self.spin_ctrl_1 = wx.SpinCtrl(self, ID_SPIN_1, "", min=0, max=100)
        self.button_8 = wx.ToggleButton(self, ID_BUTTON_8, "Vol")
        self.slider_4 = wx.Slider(self, ID_SLIDER_4, 0, 0, 500)
        self.slider_5 = wx.Slider(self, ID_SLIDER_5, 0, 0, 20)
        self.button_9 = wx.ToggleButton(self, ID_BUTTON_9, "Time")
        self.button_11 = wx.Button(self, ID_BUTTON_11, "Rew")
        self.button_10 = wx.Button(self, ID_BUTTON_10, "Fwd")
        self.panel_3 = wx.Panel(self, -1)
        self.label_2 = wx.StaticText(self, -1, "PGA               ")
        self.panel_4 = wx.Panel(self, -1)
        self.panel_8 = wx.Panel(self, -1)
        self.panel_9 = wx.Panel(self, -1)
        self.panel_10 = wx.Panel(self, -1)
        self.panel_11 = wx.Panel(self, -1)
        self.panel_12 = wx.Panel(self, -1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

        parser = OptionParser (option_class=eng_option)
        parser.add_option("", "--address", type="string", default="addr=''",
                          help="Address of UHD device, [default=%default]")
        parser.add_option("", "--spec", type="string", default="A:A",
                          help="UHD device subdev spec, [default=%default]")
        parser.add_option ("-c", "--ddc-freq", type="eng_float", default=3.9e6,
                           help="set Rx DDC frequency to FREQ", metavar="FREQ")
        parser.add_option ("-s", "--samp-rate", type="eng_float", default=256000,
                           help="set sample rate (bandwidth) [default=%default]")
        parser.add_option ("-a", "--audio_file", default="",
                           help="audio output file", metavar="FILE")
        parser.add_option ("-r", "--radio_file", default="",
                           help="radio output file", metavar="FILE")
        parser.add_option ("-i", "--input_file", default="",
                           help="radio input file", metavar="FILE")
        parser.add_option ("-O", "--audio-output", type="string", default="",
                           help="audio output device name. E.g., hw:0,0, /dev/dsp, or pulse")

        (options, args) = parser.parse_args ()

        self.usrp_center = options.ddc_freq
        input_rate = options.samp_rate
        self.slider_range = input_rate * 0.9375
        self.f_lo = self.usrp_center - (self.slider_range/2)
        self.f_hi = self.usrp_center + (self.slider_range/2)
	self.af_sample_rate = 32000
	fir_decim = long (input_rate / self.af_sample_rate)

	self.tb = gr.top_block()

        # radio variables, initial conditions
        self.frequency = self.usrp_center
        # these map the frequency slider (0-6000) to the actual range
        self.f_slider_offset = self.f_lo
        self.f_slider_scale = 10000/250
        self.spin_ctrl_1.SetRange(self.f_lo,self.f_hi)
        self.text_ctrl_1.SetValue(str(int(self.usrp_center)))
        self.slider_5.SetValue(0)
	self.AM_mode = False

        self.slider_3.SetValue((self.frequency-self.f_slider_offset)/self.f_slider_scale)
        self.spin_ctrl_1.SetValue(int(self.frequency))

        POWERMATE = True
        try:
            self.pm = powermate.powermate(self)
        except:
            sys.stderr.write("Unable to find PowerMate or Contour Shuttle\n")
            POWERMATE = False

        if POWERMATE:
          powermate.EVT_POWERMATE_ROTATE(self, self.on_rotate)
          powermate.EVT_POWERMATE_BUTTON(self, self.on_pmButton)
	self.active_button = 7

        # command line options
        if options.audio_file == "": SAVE_AUDIO_TO_FILE = False
        else: SAVE_AUDIO_TO_FILE = True
        if options.radio_file == "": SAVE_RADIO_TO_FILE = False
        else: SAVE_RADIO_TO_FILE = True
        if options.input_file == "": self.PLAY_FROM_USRP = True
        else: self.PLAY_FROM_USRP = False

        if self.PLAY_FROM_USRP:
            self.src = uhd.usrp_source("",stream_args=uhd.stream_args('fc32'))
            self.src.set_samp_rate(input_rate)
            self.src.set_subdev_spec(options.spec)
            input_rate = self.src.get_samp_rate()

            self.src.set_center_freq(self.usrp_center, 0)	
            self.tune_offset = 0

        else:
           self.src = blocks.file_source (gr.sizeof_short,options.input_file)
           self.tune_offset = 2200 # 2200 works for 3.5-4Mhz band

           # convert rf data in interleaved short int form to complex
           s2ss = blocks.stream_to_streams(gr.sizeof_short,2)
           s2f1 = blocks.short_to_float()
           s2f2 = blocks.short_to_float()
           src_f2c = blocks.float_to_complex()
           self.tb.connect(self.src,s2ss)
           self.tb.connect((s2ss,0),s2f1)
           self.tb.connect((s2ss,1),s2f2)
           self.tb.connect(s2f1,(src_f2c,0))
           self.tb.connect(s2f2,(src_f2c,1))

        # save radio data to a file
        if SAVE_RADIO_TO_FILE:
           radio_file = blocks.file_sink(gr.sizeof_short, options.radio_file)
           self.tb.connect (self.src, radio_file)

	# 2nd DDC
        xlate_taps = filter.firdes.low_pass ( \
           1.0, input_rate, 16e3, 4e3, filter.firdes.WIN_HAMMING )
        self.xlate = filter.freq_xlating_fir_filter_ccf ( \
           fir_decim, xlate_taps, self.tune_offset, input_rate )

	# Complex Audio filter
        audio_coeffs = filter.firdes.complex_band_pass (
                1.0,    # gain
                self.af_sample_rate, # sample rate
                -3000,    # low cutoff
                0,   # high cutoff
                100,    # transition
                filter.firdes.WIN_HAMMING)  # window
	self.slider_fcutoff_hi.SetValue(0)
	self.slider_fcutoff_lo.SetValue(-3000)

        self.audio_filter = filter.fir_filter_ccc(1, audio_coeffs)

	# Main +/- 16Khz spectrum display
        self.fft = fftsink2.fft_sink_c(self.panel_2, fft_size=512,
                                       sample_rate=self.af_sample_rate,
                                       average=True, size=(640,240),
				       baseband_freq=self.usrp_center)
        c2f = blocks.complex_to_float()


	# AM branch
	self.sel_am = blocks.multiply_const_cc(0)
	# the following frequencies turn out to be in radians/sample
	# analog.pll_refout_cc(alpha,beta,min_freq,max_freq)
	# suggested alpha = X, beta = .25 * X * X
	pll = analog.pll_refout_cc(.05,(2.*math.pi*7.5e3/self.af_sample_rate),
                                    (2.*math.pi*6.5e3/self.af_sample_rate))
	self.pll_carrier_scale = blocks.multiply_const_cc(complex(10,0))
	am_det = blocks.multiply_cc()
	# these are for converting +7.5kHz to -7.5kHz
	# for some reason blocks.conjugate_cc() adds noise ??
	c2f2 = blocks.complex_to_float()
	c2f3 = blocks.complex_to_float()
	f2c = blocks.float_to_complex()
	phaser1 = blocks.multiply_const_ff(1)
	phaser2 = blocks.multiply_const_ff(-1)

	# filter for pll generated carrier
        pll_carrier_coeffs = filter.firdes.complex_band_pass (
                2.0,    # gain
                self.af_sample_rate, # sample rate
                7400,    # low cutoff
                7600,   # high cutoff
                100,    # transition
                filter.firdes.WIN_HAMMING)  # window

        self.pll_carrier_filter = filter.fir_filter_ccc (1, pll_carrier_coeffs)

	self.sel_sb = blocks.multiply_const_ff(1)
	combine = blocks.add_ff()

	#AGC
	sqr1 = blocks.multiply_ff()
	intr = filter.iir_filter_ffd( [.004, 0], [0, .999] )
	offset = blocks.add_const_ff(1)
	agc = blocks.divide_ff()

        self.scale = blocks.multiply_const_ff(0.00001)
        dst = audio.sink(long(self.af_sample_rate),
                         options.audio_output)


        if self.PLAY_FROM_USRP:
            self.tb.connect(self.src, self.xlate, self.fft)
        else:
            self.tb.connect(src_f2c, self.xlate, self.fft)

        self.tb.connect(self.xlate,self.audio_filter,self.sel_am,(am_det,0))
	self.tb.connect(self.sel_am,pll,self.pll_carrier_scale,
                        self.pll_carrier_filter,c2f3)
	self.tb.connect((c2f3,0),phaser1,(f2c,0))
	self.tb.connect((c2f3,1),phaser2,(f2c,1))
	self.tb.connect(f2c,(am_det,1))
	self.tb.connect(am_det,c2f2,(combine,0))
	self.tb.connect(self.audio_filter,c2f,
                        self.sel_sb,(combine,1))


	self.tb.connect(combine,self.scale)
	self.tb.connect(self.scale,(sqr1,0))
	self.tb.connect(self.scale,(sqr1,1))
	self.tb.connect(sqr1, intr, offset, (agc, 1))
	self.tb.connect(self.scale,(agc, 0))
	self.tb.connect(agc,dst)

	if SAVE_AUDIO_TO_FILE:
	  f_out = blocks.file_sink(gr.sizeof_short,options.audio_file)
	  sc1 = blocks.multiply_const_ff(64000)
	  f2s1 = blocks.float_to_short()
	  self.tb.connect(agc,sc1,f2s1,f_out)

        self.tb.start()

        # left click to re-tune
        self.fft.win.plotter.Bind(wx.EVT_LEFT_DOWN, self.Click)

        # start a timer to check for web commands
        if WEB_CONTROL:
	   self.timer = UpdateTimer(self, 1000) # every 1000 mSec, 1 Sec


	wx.EVT_BUTTON(self,ID_BUTTON_1,self.set_lsb)
	wx.EVT_BUTTON(self,ID_BUTTON_2,self.set_usb)
	wx.EVT_BUTTON(self,ID_BUTTON_3,self.set_am)
	wx.EVT_BUTTON(self,ID_BUTTON_4,self.set_cw)
	wx.EVT_BUTTON(self,ID_BUTTON_10,self.fwd)
	wx.EVT_BUTTON(self,ID_BUTTON_11,self.rew)
	wx.EVT_TOGGLEBUTTON(self,ID_BUTTON_5,self.on_button)
	wx.EVT_TOGGLEBUTTON(self,ID_BUTTON_6,self.on_button)
	wx.EVT_TOGGLEBUTTON(self,ID_BUTTON_7,self.on_button)
	wx.EVT_TOGGLEBUTTON(self,ID_BUTTON_8,self.on_button)
	wx.EVT_TOGGLEBUTTON(self,ID_BUTTON_9,self.on_button)
        wx.EVT_SLIDER(self,ID_SLIDER_1,self.set_filter)
        wx.EVT_SLIDER(self,ID_SLIDER_2,self.set_filter)
        wx.EVT_SLIDER(self,ID_SLIDER_3,self.slide_tune)
        wx.EVT_SLIDER(self,ID_SLIDER_4,self.set_volume)
	wx.EVT_SLIDER(self,ID_SLIDER_5,self.set_pga)
        wx.EVT_SPINCTRL(self,ID_SPIN_1,self.spin_tune)

        wx.EVT_MENU(self, ID_EXIT,  self.TimeToQuit)

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("HF Explorer")
        self.slider_fcutoff_hi.SetMinSize((650, 38))
        self.slider_fcutoff_lo.SetMinSize((650, 38))
        self.panel_2.SetMinSize((800, 400))
        self.button_7.SetValue(1)
        self.slider_3.SetMinSize((650, 19))
        self.slider_4.SetMinSize((275, 19))
        self.slider_5.SetMinSize((275, 19))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(11, 2, 0, 0)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        sizer_2.Add(self.button_1, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.button_2, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.button_3, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.button_4, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_5, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.slider_fcutoff_hi, 0,
                         wx.ALIGN_LEFT|wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.button_6, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.slider_fcutoff_lo, 0,
                         wx.ALIGN_LEFT|wx.ADJUST_MINSIZE, 0)
        sizer_6.Add(self.panel_5, 1, wx.EXPAND, 0)
        sizer_6.Add(self.label_1, 0,
                    wx.ALIGN_CENTER_HORIZONTAL|wx.ADJUST_MINSIZE, 0)
        sizer_6.Add(self.text_ctrl_1, 0, wx.ADJUST_MINSIZE, 0)
        sizer_6.Add(self.panel_6, 1, wx.EXPAND, 0)
        sizer_6.Add(self.panel_7, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_6, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.panel_2, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_7, 0, wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.slider_3, 0, wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.spin_ctrl_1, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_8, 0, wx.ADJUST_MINSIZE, 0)
        sizer_4.Add(self.slider_4, 0, wx.ADJUST_MINSIZE, 0)
        sizer_4.Add(self.slider_5, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_9, 0, wx.ADJUST_MINSIZE, 0)
        sizer_5.Add(self.button_11, 0, wx.ADJUST_MINSIZE, 0)
        sizer_5.Add(self.button_10, 0, wx.ADJUST_MINSIZE, 0)
        sizer_5.Add(self.panel_3, 1, wx.EXPAND, 0)
        sizer_5.Add(self.label_2, 0, wx.ADJUST_MINSIZE, 0)
        sizer_5.Add(self.panel_4, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.panel_8, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.panel_9, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.panel_10, 1, wx.EXPAND, 0)
        sizer_7.Add(self.panel_11, 1, wx.EXPAND, 0)
        sizer_7.Add(self.panel_12, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()
        # end wxGlade

    # Menu exit
    def TimeToQuit(self, event):
        self.tb.stop()
        self.Close(True)

    # Powermate being turned
    def on_rotate(self, event):
	if self.active_button == 5:
	   self.slider_fcutoff_hi.SetValue(self.slider_fcutoff_hi.GetValue()+event.delta)
           if self.slider_fcutoff_lo.GetValue() > (self.slider_fcutoff_hi.GetValue() - 200) :
              self.slider_fcutoff_lo.SetValue(self.slider_fcutoff_hi.GetValue() - 200)
	   self.filter()
	if self.active_button == 6:
	   self.slider_fcutoff_lo.SetValue(self.slider_fcutoff_lo.GetValue()+event.delta)
	   if self.slider_fcutoff_hi.GetValue() < (self.slider_fcutoff_lo.GetValue() + 200) :
	      self.slider_fcutoff_hi.SetValue(self.slider_fcutoff_lo.GetValue() + 200)
	   self.filter()
	if self.active_button == 7:
           new = max(0, min(6000, self.slider_3.GetValue() + event.delta))
           self.slider_3.SetValue(new)
           self.frequency = (self.f_slider_scale * new) + self.f_slider_offset
           self.spin_ctrl_1.SetValue(self.frequency)
	   if self.AM_mode == False:
             self.xlate.set_center_freq( (self.frequency - self.tune_offset) - self.usrp_center)
             self.fft.set_baseband_freq( self.frequency - self.tune_offset )
	   else:
	     self.xlate.set_center_freq( (self.frequency - self.tune_offset - 7.5e3) - self.usrp_center)
             self.fft.set_baseband_freq( self.frequency - self.tune_offset - 7.5e3 )
	if self.active_button == 8:
           new = max(0, min(500, self.slider_4.GetValue() + event.delta))
           self.slider_4.SetValue(new)
           self.scale.set_k(math.pow(10.,((self.slider_4.GetValue()-500.)/100.)))
	if self.active_button == 9:
           if self.PLAY_FROM_USRP == False:
              if event.delta == -1:
                 self.src.seek(-1000000,gr.SEEK_CUR)
              elif event.delta == 1:
                 self.src.seek(1000000,gr.SEEK_CUR)


    # Powermate pressed to switch controlled function
    def on_pmButton(self, event):
	if event.value == 0:
	   if self.active_button == 5:
	      self.active_button = 6
	      self.button_5.SetValue(False)
	      self.button_6.SetValue(True)
	   elif self.active_button == 6:
	      self.active_button = 7
	      self.button_6.SetValue(False)
	      self.button_7.SetValue(True)
	   elif self.active_button == 7:
	      self.active_button = 8
	      self.button_7.SetValue(False)
	      self.button_8.SetValue(True)
	   elif self.active_button == 8:
	      self.active_button = 9
	      self.button_8.SetValue(False)
	      self.button_9.SetValue(True)
	   elif self.active_button == 9:
	      self.active_button = 5
	      self.button_9.SetValue(False)
	      self.button_5.SetValue(True)

    # Clicking one PM control button turns the rest off
    def on_button(self, event):
	id = event.GetId()
	if id == ID_BUTTON_5:
	   self.active_button = 5
	   self.button_6.SetValue(False)
	   self.button_7.SetValue(False)
	   self.button_8.SetValue(False)
	   self.button_9.SetValue(False)
	if id == ID_BUTTON_6:
	   self.active_button = 6
           self.button_5.SetValue(False)
           self.button_7.SetValue(False)
           self.button_8.SetValue(False)
           self.button_9.SetValue(False)
        if id == ID_BUTTON_7:
           self.active_button = 7
           self.button_5.SetValue(False)
           self.button_6.SetValue(False)
           self.button_8.SetValue(False)
           self.button_9.SetValue(False)
        if id == ID_BUTTON_8:
           self.active_button = 8
           self.button_5.SetValue(False)
           self.button_6.SetValue(False)
           self.button_7.SetValue(False)
           self.button_9.SetValue(False)
        if id == ID_BUTTON_9:
           self.active_button = 9
           self.button_5.SetValue(False)
           self.button_6.SetValue(False)
           self.button_7.SetValue(False)
           self.button_8.SetValue(False)

    # Make sure filter settings are legal
    def set_filter(self, event):
        slider = event.GetId()
        slider1 = self.slider_fcutoff_hi.GetValue()
        slider2 = self.slider_fcutoff_lo.GetValue()
        if slider == ID_SLIDER_1:
           if slider2 > (self.slider_fcutoff_hi.GetValue() - 200) :
              self.slider_fcutoff_lo.SetValue(slider1 - 200)
        elif slider == ID_SLIDER_2:
           if slider1 < (self.slider_fcutoff_lo.GetValue() + 200) :
              self.slider_fcutoff_hi.SetValue(slider2 + 200)
	self.filter()

    # Calculate taps and apply
    def filter(self):
        audio_coeffs = filter.firdes.complex_band_pass (
                1.0,    # gain
                self.af_sample_rate, # sample rate
                self.slider_fcutoff_lo.GetValue(),   # low cutoff
                self.slider_fcutoff_hi.GetValue(),   # high cutoff
                100,    # transition
                filter.firdes.WIN_HAMMING)  # window
        self.audio_filter.set_taps(audio_coeffs)

    def set_lsb(self, event):
	self.AM_mode = False
	self.xlate.set_center_freq( (self.frequency - self.tune_offset) - self.usrp_center)
	self.fft.set_baseband_freq( self.frequency - self.tune_offset )
	self.sel_sb.set_k(1)
	self.sel_am.set_k(0)
	self.slider_fcutoff_hi.SetValue(0)
	self.slider_fcutoff_lo.SetValue(-3000)
	self.filter()

    def set_usb(self, event):
	self.AM_mode = False
	self.xlate.set_center_freq( (self.frequency - self.tune_offset) - self.usrp_center)
        self.fft.set_baseband_freq( self.frequency - self.tune_offset )
	self.sel_sb.set_k(1)
	self.sel_am.set_k(0)
	self.slider_fcutoff_hi.SetValue(3000)
	self.slider_fcutoff_lo.SetValue(0)
	self.filter()

    def set_am(self, event):
	self.AM_mode = True
	self.xlate.set_center_freq( (self.frequency - self.tune_offset - 7.5e3) - self.usrp_center)
        self.fft.set_baseband_freq( self.frequency - self.tune_offset - 7.5e3 )
	self.sel_sb.set_k(0)
	self.sel_am.set_k(1)
	self.slider_fcutoff_hi.SetValue(12500)
	self.slider_fcutoff_lo.SetValue(2500)
	self.filter()

    def set_cw(self, event):
	self.AM_mode = False
	self.xlate.set_center_freq( (self.frequency - self.tune_offset) - self.usrp_center)
        self.fft.set_baseband_freq( self.frequency - self.tune_offset )
	self.AM_mode = False
	self.sel_sb.set_k(1)
	self.sel_am.set_k(0)
	self.slider_fcutoff_hi.SetValue(-400)
	self.slider_fcutoff_lo.SetValue(-800)
	self.filter()

    def set_volume(self, event):
        self.scale.set_k(math.pow(10.,((self.slider_4.GetValue()-500.)/100.)))

    def set_pga(self,event):
	if self.PLAY_FROM_USRP:
	   self.src.set_gain(self.slider_5.GetValue())

    def slide_tune(self, event):
        self.frequency = (self.f_slider_scale * self.slider_3.GetValue()) + self.f_slider_offset
	if self.AM_mode == False:
          self.xlate.set_center_freq( (self.frequency - self.tune_offset) - self.usrp_center)
          self.fft.set_baseband_freq( self.frequency - self.tune_offset )
	else:
	  self.xlate.set_center_freq( (self.frequency - self.tune_offset - 7.5e3) - self.usrp_center)
          self.fft.set_baseband_freq( self.frequency - self.tune_offset - 7.5e3 )
        self.spin_ctrl_1.SetValue(self.frequency)

    def spin_tune(self, event):
	self.frequency = self.spin_ctrl_1.GetValue()
	if self.AM_mode == False:
           self.xlate.set_center_freq( (self.frequency - self.tune_offset) - self.usrp_center)
           self.fft.set_baseband_freq( self.frequency - self.tune_offset )
	else:
	   self.xlate.set_center_freq( (self.frequency - self.tune_offset - 7.5e3) - self.usrp_center)
           self.fft.set_baseband_freq( self.frequency - self.tune_offset - 7.5e3 )
        self.slider_3.SetValue(int((self.frequency-self.f_slider_offset)/self.f_slider_scale))

    # Seek forwards in file
    def fwd(self, event):
	if self.PLAY_FROM_USRP == False:
	   self.src.seek(10000000,gr.SEEK_CUR)

    # Seek backwards in file
    def rew(self, event):
	if self.PLAY_FROM_USRP == False:
	   self.src.seek(-10000000,gr.SEEK_CUR)

    # Mouse clicked on fft display - change frequency
    def Click(self,event):
        fRel = ( event.GetX() - 340. ) / 18.125
	if self.AM_mode == False:
           self.frequency = self.frequency + (fRel*1e3)
	else:
	   self.frequency = self.frequency + (fRel*1e3) - 7.5e3
        self.spin_ctrl_1.SetValue(int(self.frequency))
        self.slider_3.SetValue(int((self.frequency-self.f_slider_offset)/self.f_slider_scale))
        if self.AM_mode == False:
	   self.xlate.set_center_freq ( ( self.frequency - self.tune_offset ) - self.usrp_center)
           self.fft.set_baseband_freq( self.frequency - self.tune_offset )
	else:
	   self.xlate.set_center_freq( (self.frequency - self.tune_offset - 7.5e3) - self.usrp_center)
           self.fft.set_baseband_freq( self.frequency - self.tune_offset - 7.5e3 )


    # Timer events - check for web commands
    def OnUpdate(self):
      cmds = os.listdir("/var/www/cgi-bin/commands/")
      if cmds!=[]:
        if cmds[0]=='chfreq':
          fd=open("/var/www/cgi-bin/commands/chfreq","r")
          new=fd.readline()
          fd.close()
          if new!='':
            os.unlink("/var/www/cgi-bin/commands/chfreq")
            if ( int(new) >= self.f_lo ) & ( int(new) <= self.f_hi ):
               self.frequency = int(new)
               self.slider_3.SetValue(( self.frequency - self.f_slider_offset) / self.f_slider_scale )
               self.spin_ctrl_1.SetValue(self.frequency)
               if self.AM_mode:
                 self.xlate.set_center_freq ( ( self.frequency - self.tune_offset - 7.5e3 ) - self.usrp_center)
                 self.fft.set_baseband_freq( self.frequency - self.tune_offset )
               else:
                 self.xlate.set_center_freq ( ( self.frequency - self.tune_offset ) - self.usrp_center)
                 self.fft.set_baseband_freq( self.frequency - self.tune_offset - 7.5e3 )

        if cmds[0]=='chvolume':
          fd=open("/var/www/cgi-bin/commands/chvolume","r")
          new=fd.readline()
          fd.close()
          if new!='':
            os.unlink("/var/www/cgi-bin/commands/chvolume")
            if ( int(new) >= 0 ) & ( int(new) <= 500 ):
               self.volume = int(new)
               self.slider_4.SetValue(self.volume)
               self.scale.set_k(math.pow(10.,((self.slider_4.GetValue()-500.)/100.)))

      else: # no new web commands, update state
        fh = open("/var/www/cgi-bin/state/freq","w")
        fh.write(str(int(self.frequency))+'\n')
        fh.close()
        fh = open("/var/www/cgi-bin/state/volume","w")
        fh.write(str(self.slider_4.GetValue())+'\n')
        fh.close()


# end of class MyFrame

# wx.Timer to check for web updates
class UpdateTimer(wx.Timer):
    def __init__(self, target, dur=1000):
        wx.Timer.__init__(self)
        self.target = target
        self.Start(dur)

    def Notify(self):
        """Called every timer interval"""
        if self.target:
            self.target.OnUpdate()


class MyApp(wx.App):
  def OnInit(self):
    frame = MyFrame(None, -1, "HF Explorer")
    frame.Show(True)
    self.SetTopWindow(frame)
    return True


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

