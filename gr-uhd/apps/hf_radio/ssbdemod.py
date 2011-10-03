# This tries to push the hilbert transform for ssb demod back into the
# freq. xlating filter.
#
# The usual gnuradio copyright notice is hereby included by reference.
#
# The starting point for this was weaver_isb_am1_usrp3.py.
#
# The tap coefficients for freq_xlating_fir_filter_ccf were generated
# externally and are read from a file because I didn't want to learn how
# to make fir filters with arbitrary phase response using python numeric
# facilities.
#
# They were generated using Scilab which I am already familiar with.
# M. Revnell Jan 06

from gnuradio import gr

class ssb_demod( gr.hier_block2 ):
    def __init__( self, if_rate, af_rate ):
        gr.hier_block2.__init__(self, "ssb_demod",
                                gr.io_signature(1,1,gr.sizeof_gr_complex),
                                gr.io_signature(1,1,gr.sizeof_float))

        self.if_rate  = int(if_rate)
        self.af_rate  = int(af_rate)
        self.if_decim = int(if_rate / af_rate)
        self.sideband = 1

        self.xlate_taps = ([complex(v) for v in file('ssb_taps').readlines()])
        
        self.audio_taps = gr.firdes.low_pass(
            1.0,
            self.af_rate,
            3e3,
            600,
            gr.firdes.WIN_HAMMING )

        self.xlate = gr.freq_xlating_fir_filter_ccc(
            self.if_decim,
            self.xlate_taps,
            0,
            self.if_rate )

        self.split = gr.complex_to_float()

        self.lpf = gr.fir_filter_fff(
            1, self.audio_taps )

        self.sum   = gr.add_ff( )
        self.am_sel = gr.multiply_const_ff( 0 )
        self.sb_sel = gr.multiply_const_ff( 1 )
        self.mixer  = gr.add_ff()
        self.am_det = gr.complex_to_mag()
                
        self.connect(self,             self.xlate)
        self.connect(self.xlate,       self.split)
        self.connect((self.split, 0), (self.sum, 0))
        self.connect((self.split, 1), (self.sum, 1))
        self.connect(self.sum,         self.sb_sel)
        self.connect(self.xlate,       self.am_det)
        self.connect(self.sb_sel,     (self.mixer, 0))
        self.connect(self.am_det,      self.am_sel)
        self.connect(self.am_sel,     (self.mixer, 1))
        self.connect(self.mixer,       self.lpf)
        self.connect(self.lpf,         self)

    def upper_sb( self ):
        self.xlate.set_taps([v.conjugate() for v in self.xlate_taps])    
        self.sb_sel.set_k( 1.0 )
        self.am_sel.set_k( 0.0 )

    def lower_sb( self ):
        self.xlate.set_taps(self.xlate_taps)
        self.sb_sel.set_k( 1.0 )
        self.am_sel.set_k( 0.0 )
        
    def set_am( self ):
        taps = gr.firdes.low_pass( 1.0,
                                   self.if_rate,
                                   5e3,
                                   2e3,
                                   gr.firdes.WIN_HAMMING )
        self.xlate.set_taps( taps )
        self.sb_sel.set_k( 0.0 )
        self.am_sel.set_k( 1.0 )

    def set_bw( self, bw ):
        self.audio_taps = gr.firdes.low_pass(
            1.0,
            self.af_rate,
            bw,
            600,
            gr.firdes.WIN_HAMMING )
        self.lpf.set_taps( self.audio_taps )

    def tune( self, freq ):
        self.xlate.set_center_freq( freq )

