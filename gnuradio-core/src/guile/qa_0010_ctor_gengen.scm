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
;;; ./gengen/gr_add_cc.h
;;; ./gengen/gr_add_const_cc.h
;;; ./gengen/gr_add_const_ff.h
;;; ./gengen/gr_add_const_ii.h
;;; ./gengen/gr_add_const_sf.h
;;; ./gengen/gr_add_const_ss.h
;;; ./gengen/gr_add_const_vcc.h
;;; ./gengen/gr_add_const_vff.h
;;; ./gengen/gr_add_const_vii.h
;;; ./gengen/gr_add_const_vss.h
;;; ./gengen/gr_add_ff.h
;;; ./gengen/gr_add_ii.h
;;; ./gengen/gr_add_ss.h
;;; ./gengen/gr_and_bb.h
;;; ./gengen/gr_and_const_bb.h
;;; ./gengen/gr_and_const_ii.h
;;; ./gengen/gr_and_const_ss.h
;;; ./gengen/gr_and_ii.h
;;; ./gengen/gr_and_ss.h
;;; ./gengen/gr_argmax_fs.h
;;; ./gengen/gr_argmax_is.h
;;; ./gengen/gr_argmax_ss.h
;;; ./gengen/gr_chunks_to_symbols_bc.h
;;; ./gengen/gr_chunks_to_symbols_bf.h
;;; ./gengen/gr_chunks_to_symbols_ic.h
;;; ./gengen/gr_chunks_to_symbols_if.h
;;; ./gengen/gr_chunks_to_symbols_sc.h
;;; ./gengen/gr_chunks_to_symbols_sf.h
;;; ./gengen/gr_divide_cc.h
;;; ./gengen/gr_divide_ff.h
;;; ./gengen/gr_divide_ii.h
;;; ./gengen/gr_divide_ss.h
;;; ./gengen/gr_integrate_cc.h
;;; ./gengen/gr_integrate_ff.h
;;; ./gengen/gr_integrate_ii.h
;;; ./gengen/gr_integrate_ss.h
;;; ./gengen/gr_max_ff.h
;;; ./gengen/gr_max_ii.h
;;; ./gengen/gr_max_ss.h
;;; ./gengen/gr_moving_average_cc.h
;;; ./gengen/gr_moving_average_ff.h
;;; ./gengen/gr_moving_average_ii.h
;;; ./gengen/gr_moving_average_ss.h
;;; ./gengen/gr_multiply_cc.h
;;; ./gengen/gr_multiply_const_cc.h
;;; ./gengen/gr_multiply_const_ff.h
;;; ./gengen/gr_multiply_const_ii.h
;;; ./gengen/gr_multiply_const_ss.h
;;; ./gengen/gr_multiply_const_vcc.h
;;; ./gengen/gr_multiply_const_vff.h
;;; ./gengen/gr_multiply_const_vii.h
;;; ./gengen/gr_multiply_const_vss.h
;;; ./gengen/gr_multiply_ff.h
;;; ./gengen/gr_multiply_ii.h
;;; ./gengen/gr_multiply_ss.h
;;; ./gengen/gr_mute_cc.h
;;; ./gengen/gr_mute_ff.h
;;; ./gengen/gr_mute_ii.h
;;; ./gengen/gr_mute_ss.h
;;; ./gengen/gr_noise_source_c.h
;;; ./gengen/gr_noise_source_f.h
;;; ./gengen/gr_noise_source_i.h
;;; ./gengen/gr_noise_source_s.h
;;; ./gengen/gr_not_bb.h
;;; ./gengen/gr_not_ii.h
;;; ./gengen/gr_not_ss.h
;;; ./gengen/gr_or_bb.h
;;; ./gengen/gr_or_ii.h
;;; ./gengen/gr_or_ss.h
;;; ./gengen/gr_packed_to_unpacked_bb.h
;;; ./gengen/gr_packed_to_unpacked_ii.h
;;; ./gengen/gr_packed_to_unpacked_ss.h
;;; ./gengen/gr_peak_detector_fb.h
;;; ./gengen/gr_peak_detector_ib.h
;;; ./gengen/gr_peak_detector_sb.h
;;; ./gengen/gr_sample_and_hold_bb.h
;;; ./gengen/gr_sample_and_hold_ff.h
;;; ./gengen/gr_sample_and_hold_ii.h
;;; ./gengen/gr_sample_and_hold_ss.h
;;; ./gengen/gr_sig_source_c.h
;;; ./gengen/gr_sig_source_f.h
;;; ./gengen/gr_sig_source_i.h
;;; ./gengen/gr_sig_source_s.h
;;; ./gengen/gr_sub_cc.h
;;; ./gengen/gr_sub_ff.h
;;; ./gengen/gr_sub_ii.h
;;; ./gengen/gr_sub_ss.h
;;; ./gengen/gr_unpacked_to_packed_bb.h
;;; ./gengen/gr_unpacked_to_packed_ii.h
;;; ./gengen/gr_unpacked_to_packed_ss.h
;;; ./gengen/gr_vector_sink_b.h
;;; ./gengen/gr_vector_sink_c.h
;;; ./gengen/gr_vector_sink_f.h
;;; ./gengen/gr_vector_sink_i.h
;;; ./gengen/gr_vector_sink_s.h
;;; ./gengen/gr_vector_source_b.h
;;; ./gengen/gr_vector_source_c.h
;;; ./gengen/gr_vector_source_f.h
;;; ./gengen/gr_vector_source_i.h
;;; ./gengen/gr_vector_source_s.h
;;; ./gengen/gr_xor_bb.h
;;; ./gengen/gr_xor_ii.h
;;; ./gengen/gr_xor_ss.h
