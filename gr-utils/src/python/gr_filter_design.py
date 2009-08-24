#!/usr/bin/env python

try:
    import scipy
    from scipy import fftpack
except ImportError:
    print "Please install SciPy to run this script (http://www.scipy.org/)"
    raise SystemExit, 1

import sys, os
from PyQt4 import Qt, QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from optparse import OptionParser
from gnuradio import gr, blks2, eng_notation
from scipy import fftpack

from pyqt_filter import Ui_MainWindow
from pyqt_filter_firlpf import Ui_firlpfForm
from pyqt_filter_firhpf import Ui_firhpfForm

class gr_plot_filter(QtGui.QMainWindow):
    def __init__(self, qapp, options):
        QtGui.QWidget.__init__(self, None)
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        self.connect(self.gui.filterTypeComboBox,
                     Qt.SIGNAL("currentIndexChanged(const QString&)"),
                     self.changed_filter_type)
        self.connect(self.gui.filterDesignTypeComboBox,
                     Qt.SIGNAL("currentIndexChanged(const QString&)"),
                     self.changed_filter_design_type)

        self.connect(self.gui.designButton,
                     Qt.SIGNAL("released()"),
                     self.design)

        self.connect(self.gui.tabGroup,
                     Qt.SIGNAL("currentChanged(int)"),
                     self.tab_changed)

        self.connect(self.gui.nfftEdit,
                     Qt.SIGNAL("textEdited(QString)"),
                     self.nfft_edit_changed)

        self.gui.designButton.setShortcut("Return")

        self.taps = []
        self.nfftpts = int(10000)
        self.gui.nfftEdit.setText(Qt.QString("%1").arg(self.nfftpts))

        self.gui.lpfPassBandRippleLabel.setVisible(False)
        self.gui.lpfPassBandRippleEdit.setVisible(False)
        self.gui.bpfPassBandRippleLabel.setVisible(False)
        self.gui.bpfPassBandRippleEdit.setVisible(False)
        self.gui.hpfPassBandRippleLabel.setVisible(False)
        self.gui.hpfPassBandRippleEdit.setVisible(False)
                
        # Initialize to LPF
        self.gui.filterTypeWidget.setCurrentWidget(self.gui.firlpfPage)

        # Set up plot curves
        self.rcurve = Qwt.QwtPlotCurve("Real")
        self.rcurve.attach(self.gui.timePlot)

        self.freqcurve = Qwt.QwtPlotCurve("PSD")
        self.freqcurve.attach(self.gui.freqPlot)

        # Create zoom functionality for the plots
        self.timeZoomer = Qwt.QwtPlotZoomer(self.gui.timePlot.xBottom,
                                            self.gui.timePlot.yLeft,
                                            Qwt.QwtPicker.PointSelection,
                                            Qwt.QwtPicker.AlwaysOn,
                                            self.gui.timePlot.canvas())

        self.freqZoomer = Qwt.QwtPlotZoomer(self.gui.freqPlot.xBottom,
                                            self.gui.freqPlot.yLeft,
                                            Qwt.QwtPicker.PointSelection,
                                            Qwt.QwtPicker.AlwaysOn,
                                            self.gui.freqPlot.canvas())

        self.phaseZoomer = Qwt.QwtPlotZoomer(self.gui.phasePlot.xBottom,
                                             self.gui.phasePlot.yLeft,
                                             Qwt.QwtPicker.PointSelection,
                                             Qwt.QwtPicker.AlwaysOn,
                                             self.gui.phasePlot.canvas())

        self.groupZoomer = Qwt.QwtPlotZoomer(self.gui.groupPlot.xBottom,
                                             self.gui.groupPlot.yLeft,
                                             Qwt.QwtPicker.PointSelection,
                                             Qwt.QwtPicker.AlwaysOn,
                                             self.gui.groupPlot.canvas())

        # Set up pen for colors and line width
        blue = QtGui.qRgb(0x00, 0x00, 0xFF)
        blueBrush = Qt.QBrush(Qt.QColor(blue))
        self.freqcurve.setPen(Qt.QPen(blueBrush, 2))
        self.rcurve.setPen(Qt.QPen(blueBrush, 2))

        self.filterWindows = {"Hamming Window" : gr.firdes.WIN_HAMMING,
                              "Hann Window" : gr.firdes.WIN_HANN,
                              "Blackman Window" : gr.firdes.WIN_BLACKMAN,
                              "Rectangular Window" : gr.firdes.WIN_RECTANGULAR,
                              "Kaiser Window" : gr.firdes.WIN_KAISER,
                              "Blackman-harris Window" : gr.firdes.WIN_BLACKMAN_hARRIS}

        self.show()

    def changed_filter_type(self, ftype):
        strftype = str(ftype.toAscii())
        if(ftype == "Low Pass"):
            self.gui.filterTypeWidget.setCurrentWidget(self.gui.firlpfPage)
        elif(ftype == "Band Pass"):
            self.gui.filterTypeWidget.setCurrentWidget(self.gui.firbpfPage)
        elif(ftype == "High Pass"):
            self.gui.filterTypeWidget.setCurrentWidget(self.gui.firhpfPage)

        self.design()
        
    def changed_filter_design_type(self, design):
        if(design == "Equiripple"):
            self.set_equiripple()
        else:
            self.set_windowed()
            
        self.design()

    def set_equiripple(self):
        self.equiripple = True
        self.gui.lpfPassBandRippleLabel.setVisible(True)
        self.gui.lpfPassBandRippleEdit.setVisible(True)
        self.gui.bpfPassBandRippleLabel.setVisible(True)
        self.gui.bpfPassBandRippleEdit.setVisible(True)
        self.gui.hpfPassBandRippleLabel.setVisible(True)
        self.gui.hpfPassBandRippleEdit.setVisible(True)
        
    def set_windowed(self):
        self.equiripple = False
        self.gui.lpfPassBandRippleLabel.setVisible(False)
        self.gui.lpfPassBandRippleEdit.setVisible(False)
        self.gui.bpfPassBandRippleLabel.setVisible(False)
        self.gui.bpfPassBandRippleEdit.setVisible(False)
        self.gui.hpfPassBandRippleLabel.setVisible(False)
        self.gui.hpfPassBandRippleEdit.setVisible(False)
        
    def design(self):
        ret = True
        fs,r = self.gui.sampleRateEdit.text().toDouble()
        ret = r and ret
        gain,r = self.gui.filterGainEdit.text().toDouble()
        ret = r and ret

        if(ret):
            winstr = str(self.gui.filterDesignTypeComboBox.currentText().toAscii())
            ftype = str(self.gui.filterTypeComboBox.currentText().toAscii())

            if(winstr == "Equiripple"):
                designer = {"Low Pass" : self.design_opt_lpf,
                            "Band Pass" : self.design_opt_bpf,
                            "High Pass" :  self.design_opt_hpf}        
                taps,r = designer[ftype](fs, gain)

            else:
                designer = {"Low Pass" : self.design_win_lpf,
                            "Band Pass" : self.design_win_bpf,
                            "High Pass" :  self.design_win_hpf}        
                wintype = self.filterWindows[winstr]
                taps,r = designer[ftype](fs, gain, wintype)

            if(r):
                self.update_time_curves(taps)
                self.update_freq_curves(taps, self.nfftpts)
        

    # Filter design functions using a window
    def design_win_lpf(self, fs, gain, wintype):
        ret = True
        pb,r = self.gui.endofLpfPassBandEdit.text().toDouble()
        ret = r and ret
        sb,r = self.gui.startofLpfStopBandEdit.text().toDouble()
        ret = r and ret
        atten,r = self.gui.lpfStopBandAttenEdit.text().toDouble()
        ret = r and ret

        if(ret):
            tb = sb - pb
            
            taps = gr.firdes.low_pass_2(gain, fs, pb, tb,
                                        atten, wintype)
            return (taps, ret)
        else:
            return ([], ret)
    
    def design_win_bpf(self, fs, gain, wintype):
        ret = True
        pb1,r = self.gui.startofBpfPassBandEdit.text().toDouble()
        ret = r and ret
        pb2,r = self.gui.endofBpfPassBandEdit.text().toDouble()
        ret = r and ret
        tb,r  = self.gui.bpfTransitionEdit.text().toDouble()
        ret = r and ret
        atten,r = self.gui.bpfStopBandAttenEdit.text().toDouble()
        ret = r and ret

        if(r):
            taps = gr.firdes.band_pass_2(gain, fs, pb1, pb2, tb,
                                         atten, wintype)
            return (taps,r)
        else:
            return ([],r)

    def design_win_hpf(self, fs, gain, wintype):
        ret = True
        sb,r = self.gui.endofHpfStopBandEdit.text().toDouble()
        ret = r and ret
        pb,r = self.gui.startofHpfPassBandEdit.text().toDouble()
        ret = r and ret
        atten,r = self.gui.hpfStopBandAttenEdit.text().toDouble()
        ret = r and ret

        if(r):
            tb = pb - sb
            taps = gr.firdes.high_pass_2(gain, fs, pb, tb,
                                         atten, wintype)            
            return (taps,r)
        else:
            return ([],r)



    # Design Functions for Equiripple Filters
    def design_opt_lpf(self, fs, gain, wintype=None):
        ret = True
        pb,r = self.gui.endofLpfPassBandEdit.text().toDouble()
        ret = r and ret
        sb,r = self.gui.startofLpfStopBandEdit.text().toDouble()
        ret = r and ret
        atten,r = self.gui.lpfStopBandAttenEdit.text().toDouble()
        ret = r and ret
        ripple,r = self.gui.lpfPassBandRippleEdit.text().toDouble()
        ret = r and ret

        if(ret):
            taps = blks2.optfir.low_pass(gain, fs, pb, sb,
                                         ripple, atten)
            return (taps, ret)
        else:
            return ([], ret)
    
    def design_opt_bpf(self, fs, gain, wintype=None):
        ret = True
        pb1,r = self.gui.startofBpfPassBandEdit.text().toDouble()
        ret = r and ret
        pb2,r = self.gui.endofBpfPassBandEdit.text().toDouble()
        ret = r and ret
        tb,r  = self.gui.bpfTransitionEdit.text().toDouble()
        ret = r and ret
        atten,r = self.gui.bpfStopBandAttenEdit.text().toDouble()
        ret = r and ret
        ripple,r = self.gui.bpfPassBandRippleEdit.text().toDouble()
        ret = r and ret

        if(r):
            sb1 = pb1 - tb
            sb2 = pb2 + tb
            taps = blks2.optfir.band_pass(gain, fs, sb1, pb1, pb2, sb2,
                                          ripple, atten)
            return (taps,r)
        else:
            return ([],r)

    def design_opt_hpf(self, fs, gain, wintype=None):
        ret = True
        sb,r = self.gui.endofHpfStopBandEdit.text().toDouble()
        ret = r and ret
        pb,r = self.gui.startofHpfPassBandEdit.text().toDouble()
        ret = r and ret
        atten,r = self.gui.hpfStopBandAttenEdit.text().toDouble()
        ret = r and ret
        ripple,r = self.gui.hpfPassBandRippleEdit.text().toDouble()
        ret = r and ret

        if(r):
            taps = blks2.optfir.high_pass(gain, fs, sb, pb,
                                          atten, ripple)
            return (taps,r)
        else:
            return ([],r)

    def nfft_edit_changed(self, nfft):
        infft,r = nfft.toInt()
        if(r and (infft != self.nfftpts)):
            self.nfftpts = infft
            self.update_freq_curves(self.taps, self.nfftpts)

    def tab_changed(self, tab):
        if(tab == 0):
            self.update_freq_curves(self.taps, self.nfftpts)
        if(tab == 1):
            self.update_time_curves(self.taps)
        
    def update_time_curves(self, taps):
        self.taps = taps
        ntaps = len(taps)
        if(ntaps > 0):
            self.rcurve.setData(scipy.arange(ntaps), taps)
            
            # Reset the x-axis to the new time scale
            ymax = 1.5 * max(taps)
            ymin = 1.5 * min(taps)
            self.gui.timePlot.setAxisScale(self.gui.timePlot.xBottom,
                                           0, ntaps)
            self.gui.timePlot.setAxisScale(self.gui.timePlot.yLeft,
                                           ymin, ymax)
            
            # Set the zoomer base to unzoom to the new axis
            self.timeZoomer.setZoomBase()
            
            self.gui.timePlot.replot()
        
    def update_freq_curves(self, taps, Npts=1000):
        if(len(taps) > 0):
            fftpts = fftpack.fft(taps, Npts)
            freq = scipy.arange(0, Npts)
            
            fftdB = 20.0*scipy.log10(abs(fftpts))
            
            self.freqcurve.setData(freq, fftdB)
            
            # Reset the x-axis to the new time scale
            ymax = 1.5 * max(fftdB)
            ymin = 1.5 * min(fftdB)
            self.gui.freqPlot.setAxisScale(self.gui.freqPlot.xBottom,
                                           0, Npts/2)
            self.gui.timePlot.setAxisScale(self.gui.timePlot.yLeft,
                                           ymin, ymax)
            
            # Set the zoomer base to unzoom to the new axis
            self.freqZoomer.setZoomBase()
            
            self.gui.freqPlot.replot()


def setup_options():
    usage="%prog: [options] (input_filename)"
    description = ""

    parser = OptionParser(conflict_handler="resolve",
                          usage=usage, description=description)
    return parser

def main(args):
    parser = setup_options()
    (options, args) = parser.parse_args ()

    app = Qt.QApplication(args)
    gplt = gr_plot_filter(app, options)
    app.exec_()

if __name__ == '__main__':
    main(sys.argv)

