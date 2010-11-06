;;;
;;; Copyright 2010 Free Software Foundation, Inc.
;;;
;;; This file is part of GNU Radio
;;;
;;; GNU Radio is free software; you can redistribute it and/or modify
;;; it under the terms of the GNU General Public License as published by
;;; the Free Software Foundation; either version 3, or (at your option)
;;; any later version.
;;;
;;; GNU Radio is distributed in the hope that it will be useful,
;;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;; GNU General Public License for more details.
;;;
;;; You should have received a copy of the GNU General Public License
;;; along with this program.  If not, see <http://www.gnu.org/licenses/>.
;;;

(use-modules (gnuradio core))
(use-modules (oop goops))

(load-from-path "srfi/srfi-64")		; unit test library

;;; Add test code for all constructors in these files
;;;
;;; ./filter/gr_adaptive_fir_ccf.h
;;; ./filter/gr_cma_equalizer_cc.h
;;; ./filter/gr_fft_filter_ccc.h
;;; ./filter/gr_fft_filter_fff.h
;;; ./filter/gr_filter_delay_fc.h
;;; ./filter/gr_fir_ccc_generic.h
;;; ./filter/gr_fir_ccc_simd.h
;;; ./filter/gr_fir_ccc_x86.h
;;; ./filter/gr_fir_ccf_generic.h
;;; ./filter/gr_fir_ccf_simd.h
;;; ./filter/gr_fir_ccf_x86.h
;;; ./filter/gr_fir_fcc_generic.h
;;; ./filter/gr_fir_fcc_simd.h
;;; ./filter/gr_fir_fcc_x86.h
;;; ./filter/gr_fir_fff_altivec.h
;;; ./filter/gr_fir_fff_armv7_a.h
;;; ./filter/gr_fir_fff_generic.h
;;; ./filter/gr_fir_fff_simd.h
;;; ./filter/gr_fir_fff_x86.h
;;; ./filter/gr_fir_filter_ccc.h
;;; ./filter/gr_fir_filter_ccf.h
;;; ./filter/gr_fir_filter_fcc.h
;;; ./filter/gr_fir_filter_fff.h
;;; ./filter/gr_fir_filter_fsf.h
;;; ./filter/gr_fir_filter_scc.h
;;; ./filter/gr_fir_fsf_generic.h
;;; ./filter/gr_fir_fsf_simd.h
;;; ./filter/gr_fir_fsf_x86.h
;;; ./filter/gr_fir_scc_generic.h
;;; ./filter/gr_fir_scc_simd.h
;;; ./filter/gr_fir_scc_x86.h
;;; ./filter/gr_fir_sysconfig_armv7_a.h
;;; ./filter/gr_fir_sysconfig_generic.h
;;; ./filter/gr_fir_sysconfig_powerpc.h
;;; ./filter/gr_fir_sysconfig_x86.h
;;; ./filter/gr_fractional_interpolator_cc.h
;;; ./filter/gr_fractional_interpolator_ff.h
;;; ./filter/gr_freq_xlating_fir_filter_ccc.h
;;; ./filter/gr_freq_xlating_fir_filter_ccf.h
;;; ./filter/gr_freq_xlating_fir_filter_fcc.h
;;; ./filter/gr_freq_xlating_fir_filter_fcf.h
;;; ./filter/gr_freq_xlating_fir_filter_scc.h
;;; ./filter/gr_freq_xlating_fir_filter_scf.h
;;; ./filter/gr_goertzel_fc.h
;;; ./filter/gr_hilbert_fc.h
;;; ./filter/gr_iir_filter_ffd.h
;;; ./filter/gr_interp_fir_filter_ccc.h
;;; ./filter/gr_interp_fir_filter_ccf.h
;;; ./filter/gr_interp_fir_filter_fcc.h
;;; ./filter/gr_interp_fir_filter_fff.h
;;; ./filter/gr_interp_fir_filter_fsf.h
;;; ./filter/gr_interp_fir_filter_scc.h
;;; ./filter/gr_pfb_arb_resampler_ccf.h
;;; ./filter/gr_pfb_channelizer_ccf.h
;;; ./filter/gr_pfb_clock_sync_ccf.h
;;; ./filter/gr_pfb_clock_sync_fff.h
;;; ./filter/gr_pfb_decimator_ccf.h
;;; ./filter/gr_pfb_interpolator_ccf.h
;;; ./filter/gr_rational_resampler_base_ccc.h
;;; ./filter/gr_rational_resampler_base_ccf.h
;;; ./filter/gr_rational_resampler_base_fcc.h
;;; ./filter/gr_rational_resampler_base_fff.h
;;; ./filter/gr_rational_resampler_base_fsf.h
;;; ./filter/gr_rational_resampler_base_scc.h
;;; ./filter/gr_single_pole_iir_filter_cc.h
;;; ./filter/gr_single_pole_iir_filter_ff.h
