#!/usr/bin/env python
#
# Copyright 2006,2007 Free Software Foundation, Inc.
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
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

"""
Here is a bit of code that will receive SCA analog subcarriers of FM
Broadcast Stations using the USRP.  It is a modified version of
usrp_wfm_rcv.py.

Common SCA frequencies are 67 kHz and 92 kHz.  SCA is used for Reading
Services for the Blind, Background Music, Foreign Language Services, and
other services.  Remember you may hear static when tuned to a FM station
because this code only outputs SCA audio.

The USRP gain is critical for good decoding.  Adjust for minimum noise.
 I use the Post FM Demod FFT to check for SCA subcarriers and to adjust
the USRP gain for the lowest noise floor.  The stereo pilot at 19 KHz,
the stereo difference signal around 38 KHz, and RDS at 57 KHz are also
displayed on the Post FM Demod FFT if present.

The range below 67 kHz is used for SCA only when Stereo is not used.

The SCA recieve range is not as far as the main FM carrier receive range
so tune in strong local stations first.

I tried to comment the code with the various parameters.  There seems to
be several choices for a couple of them.  I coded the common ones I see
here.

In the local area there are a couple of stations using digital SCA.
These look similar to narrow DRM signals and I wonder if they are using
OFDM.
"""


from gnuradio import gr, gru, eng_notation, optfir
from gnuradio import audio
from gnuradio import usrp
from gnuradio import blks
from gnuradio.blksimpl.fm_emph import fm_deemph
from gnuradio.eng_option import eng_option
from gnuradio.wxgui import slider, powermate
from gnuradio.wxgui import stdgui, fftsink, form
from optparse import OptionParser
from usrpm import usrp_dbid
import sys
import math
import wx

def pick_subdevice(u):
    """
    The user didn't specify a subdevice on the command line.
    Try for one of these, in order: TV_RX, BASIC_RX, whatever is on side A.

    @return a subdev_spec
    """
    return usrp.pick_subdev(u, (usrp_dbid.TV_RX,
                                usrp_dbid.TV_RX_REV_2,
                                usrp_dbid.BASIC_RX))


class wfm_rx_sca_graph (stdgui.gui_flow_graph):
    def __init__(self,frame,panel,vbox,argv):
        stdgui.gui_flow_graph.__init__ (self,frame,panel,vbox,argv)

        parser=OptionParser(option_class=eng_option)
        parser.add_option("-R", "--rx-subdev-spec", type="subdev", default=None,
                          help="select USRP Rx side A or B (default=A)")
        parser.add_option("-f", "--freq", type="eng_float", default=100.1e6,
                          help="set frequency to FREQ", metavar="FREQ")
        parser.add_option("-g", "--gain", type="eng_float", default=40,
                          help="set gain in dB (default is midpoint)")
        parser.add_option("-V", "--volume", type="eng_float", default=None,
                          help="set volume (default is midpoint)")
        parser.add_option("-O", "--audio-output", type="string", default="",
                          help="pcm device name.  E.g., hw:0,0 or surround51 or /dev/dsp")

        (options, args) = parser.parse_args()
        if len(args) != 0:
            parser.print_help()
            sys.exit(1)

        self.frame = frame
        self.panel = panel

        self.vol = 0
        self.state = "FREQ"
        self.freq = 0

        # build graph

        self.u = usrp.source_c()                    # usrp is data source

        adc_rate = self.u.adc_rate()                # 64 MS/s
        usrp_decim = 200
        self.u.set_decim_rate(usrp_decim)
        usrp_rate = adc_rate / usrp_decim           # 320 kS/s
        chanfilt_decim = 1
        demod_rate = usrp_rate / chanfilt_decim
        sca_chanfilt_decim = 5
        sca_demod_rate = demod_rate / sca_chanfilt_decim  #64 kHz
        audio_decimation = 2
        audio_rate = sca_demod_rate / audio_decimation  # 32 kHz

        if options.rx_subdev_spec is None:
            options.rx_subdev_spec = pick_subdevice(self.u)

        self.u.set_mux(usrp.determine_rx_mux_value(self.u, options.rx_subdev_spec))
        self.subdev = usrp.selected_subdev(self.u, options.rx_subdev_spec)
        print "Using RX d'board %s" % (self.subdev.side_and_name(),)

        #Create filter to get main FM Channel we want
        chan_filt_coeffs = optfir.low_pass (1,           # gain
                                            usrp_rate,   # sampling rate
                                            100e3,        # passband cutoff
                                            140e3,       # stopband cutoff
                                            0.1,         # passband ripple
                                            60)          # stopband attenuation
        #print len(chan_filt_coeffs)
        chan_filt = gr.fir_filter_ccf (chanfilt_decim, chan_filt_coeffs)

        #Create demodulator block for Main FM Channel
	max_dev = 75e3
        fm_demod_gain = demod_rate/(2*math.pi*max_dev)
        self.fm_demod = gr.quadrature_demod_cf (fm_demod_gain)

        # Note - deemphasis is not applied to the Main FM Channel as main audio is not decoded

        # SCA Devation is 10% of carrier but some references say 20% if mono with one SCA (6 KHz seems typical)
        max_sca_dev = 6e3

	# Create filter to get SCA channel we want
        sca_chan_coeffs = gr.firdes.low_pass (1.0,                # gain
                                          demod_rate,       # sampling rate
                                          max_sca_dev,      # low pass cutoff freq
                                          max_sca_dev/3,    # width of trans. band
                                          gr.firdes.WIN_HANN) # filter type

        self.ddc = gr.freq_xlating_fir_filter_fcf(sca_chanfilt_decim,       # decimation rate
                                                  sca_chan_coeffs,    # taps
                                                  0,              # frequency translation amount (Gets set by the UI)
                                                  demod_rate)   # input sample rate

        #Create demodulator block for SCA Channel
        sca_demod_gain = sca_demod_rate/(2*math.pi*max_sca_dev)
        self.fm_demod_sca = gr.quadrature_demod_cf (sca_demod_gain)


        # SCA analog audio is bandwidth limited to 5 KHz
        max_sca_audio_freq = 5.0e3
        # SCA analog deephasis is 150 uS (75 uS may be used)
        sca_tau = 150e-6

        # compute FIR filter taps for SCA audio filter
        audio_coeffs = gr.firdes.low_pass (1.0,         # gain
                                           sca_demod_rate,      # sampling rate
                                           max_sca_audio_freq, # low pass cutoff freq
                                           max_sca_audio_freq/2.5,             # width of trans. band
                                           gr.firdes.WIN_HAMMING)

        # input: float; output: float
        self.audio_filter = gr.fir_filter_fff (audio_decimation, audio_coeffs)

	# Create deemphasis block that is applied after SCA demodulation
        self.deemph = fm_deemph (self, audio_rate, sca_tau)

        self.volume_control = gr.multiply_const_ff(self.vol)

        # sound card as final sink
        audio_sink = audio.sink (int (audio_rate),
                                 options.audio_output,
                                 False)  # ok_to_block

        # now wire it all together
        self.connect (self.u, chan_filt, self.fm_demod, self.ddc, self.fm_demod_sca)
        self.connect (self.fm_demod_sca, self.audio_filter, self.deemph, self.volume_control, audio_sink)

        self._build_gui(vbox, usrp_rate, demod_rate, sca_demod_rate, audio_rate)

        if options.gain is None:
            # if no gain was specified, use the mid-point in dB
            g = self.subdev.gain_range()
            options.gain = float(g[0]+g[1])/2

        if options.volume is None:
            g = self.volume_range()
            options.volume = float(g[0]+g[1])/2

        if abs(options.freq) < 1e6:
            options.freq *= 1e6

        # set initial values

        self.set_gain(options.gain)
        self.set_vol(options.volume)
        if not(self.set_freq(options.freq)):
            self._set_status_msg("Failed to set initial frequency")
        self.set_sca_freq(67000)  # A common SCA Frequency


    def _set_status_msg(self, msg, which=0):
        self.frame.GetStatusBar().SetStatusText(msg, which)


    def _build_gui(self, vbox, usrp_rate, demod_rate, sca_demod_rate, audio_rate):

        def _form_set_freq(kv):
            return self.set_freq(kv['freq'])

        def _form_set_sca_freq(kv):
            return self.set_sca_freq(kv['sca_freq'])

        if 1:
            self.src_fft = fftsink.fft_sink_c (self, self.panel, title="Data from USRP",
                                               fft_size=512, sample_rate=usrp_rate)
            self.connect (self.u, self.src_fft)
            vbox.Add (self.src_fft.win, 4, wx.EXPAND)

        if 1:
            post_demod_fft = fftsink.fft_sink_f (self, self.panel, title="Post FM Demod",
                                                fft_size=2048, sample_rate=demod_rate,
                                                y_per_div=10, ref_level=0)
            self.connect (self.fm_demod, post_demod_fft)
            vbox.Add (post_demod_fft.win, 4, wx.EXPAND)

        if 0:
            post_demod_sca_fft = fftsink.fft_sink_f (self, self.panel, title="Post SCA Demod",
                                                fft_size=1024, sample_rate=sca_demod_rate,
                                                y_per_div=10, ref_level=0)
            self.connect (self.fm_demod_sca, post_demod_sca_fft)
            vbox.Add (post_demod_sca_fft.win, 4, wx.EXPAND)

        if 0:
            post_deemph_fft = fftsink.fft_sink_f (self, self.panel, title="Post SCA Deemph",
                                                  fft_size=512, sample_rate=audio_rate,
                                                  y_per_div=10, ref_level=-20)
            self.connect (self.deemph, post_deemph_fft)
            vbox.Add (post_deemph_fft.win, 4, wx.EXPAND)


        # control area form at bottom
        self.myform = myform = form.form()

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add((5,0), 0)
        myform['freq'] = form.float_field(
            parent=self.panel, sizer=hbox, label="Freq", weight=1,
            callback=myform.check_input_and_call(_form_set_freq, self._set_status_msg))

        hbox.Add((5,0), 0)
        myform['freq_slider'] = \
            form.quantized_slider_field(parent=self.panel, sizer=hbox, weight=3,
                                        range=(87.9e6, 108.1e6, 0.1e6),
                                        callback=self.set_freq)
        hbox.Add((5,0), 0)
        vbox.Add(hbox, 0, wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add((5,0), 0)
        myform['sca_freq'] = form.float_field(
            parent=self.panel, sizer=hbox, label="SCA", weight=1,
            callback=myform.check_input_and_call(_form_set_sca_freq, self._set_status_msg))

        hbox.Add((5,0), 0)
        myform['sca_freq_slider'] = \
            form.quantized_slider_field(parent=self.panel, sizer=hbox, weight=3,
                                        range=(38e3, 100e3, 1.0e3),
                                        callback=self.set_sca_freq)
        hbox.Add((5,0), 0)
        vbox.Add(hbox, 0, wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add((5,0), 0)

        myform['volume'] = \
            form.quantized_slider_field(parent=self.panel, sizer=hbox, label="Volume",
                                        weight=3, range=self.volume_range(),
                                        callback=self.set_vol)
        hbox.Add((5,0), 1)

        myform['gain'] = \
            form.quantized_slider_field(parent=self.panel, sizer=hbox, label="Gain",
                                        weight=3, range=self.subdev.gain_range(),
                                        callback=self.set_gain)
        hbox.Add((5,0), 0)
        vbox.Add(hbox, 0, wx.EXPAND)

        try:
            self.knob = powermate.powermate(self.frame)
            self.rot = 0
            powermate.EVT_POWERMATE_ROTATE (self.frame, self.on_rotate)
            powermate.EVT_POWERMATE_BUTTON (self.frame, self.on_button)
        except:
            print "FYI: No Powermate or Contour Knob found"


    def on_rotate (self, event):
        self.rot += event.delta
        if (self.state == "FREQ"):
            if self.rot >= 3:
                self.set_freq(self.freq + .1e6)
                self.rot -= 3
            elif self.rot <=-3:
                self.set_freq(self.freq - .1e6)
                self.rot += 3
        else:
            step = self.volume_range()[2]
            if self.rot >= 3:
                self.set_vol(self.vol + step)
                self.rot -= 3
            elif self.rot <=-3:
                self.set_vol(self.vol - step)
                self.rot += 3

    def on_button (self, event):
        if event.value == 0:        # button up
            return
        self.rot = 0
        if self.state == "FREQ":
            self.state = "VOL"
        else:
            self.state = "FREQ"
        self.update_status_bar ()


    def set_vol (self, vol):
        g = self.volume_range()
        self.vol = max(g[0], min(g[1], vol))
        self.volume_control.set_k(10**(self.vol/10))
        self.myform['volume'].set_value(self.vol)
        self.update_status_bar ()

    def set_freq(self, target_freq):
        """
        Set the center frequency we're interested in.

        @param target_freq: frequency in Hz
        @rypte: bool

        Tuning is a two step process.  First we ask the front-end to
        tune as close to the desired frequency as it can.  Then we use
        the result of that operation and our target_frequency to
        determine the value for the digital down converter.
        """
        r = usrp.tune(self.u, 0, self.subdev, target_freq)

        if r:
            self.freq = target_freq
            self.myform['freq'].set_value(target_freq)         # update displayed value
            self.myform['freq_slider'].set_value(target_freq)  # update displayed value
            self.update_status_bar()
            self._set_status_msg("OK", 0)
            return True

        self._set_status_msg("Failed", 0)
        return False

    def set_sca_freq(self, target_sca_freq):

        self.ddc.set_center_freq(-target_sca_freq)
        self.myform['sca_freq'].set_value(target_sca_freq)         # update displayed value
        self.myform['sca_freq_slider'].set_value(target_sca_freq)  # update displayed value
        self.update_status_bar()
        self._set_status_msg("OK", 0)
        return True

    def set_gain(self, gain):
        self.myform['gain'].set_value(gain)     # update displayed value
        self.subdev.set_gain(gain)

    def update_status_bar (self):
        msg = "Volume:%r  Setting:%s" % (self.vol, self.state)
        self._set_status_msg(msg, 1)
        self.src_fft.set_baseband_freq(self.freq)

    def volume_range(self):
        return (-20.0, 0.0, 0.5)


if __name__ == '__main__':
    app = stdgui.stdapp (wfm_rx_sca_graph, "USRP WFM SCA RX")
    app.MainLoop ()
