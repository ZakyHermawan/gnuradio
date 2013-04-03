/* -*- c++ -*- */
/*
 * Copyright 2012-2013 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#define BLOCKS_API

%include "runtime_swig.i"
%include "blocks/pdu.h"

//load generated python docstrings
%include "blocks_swig_doc.i"

%include <gr_endianness.h>

// For vector_map.
%template() std::vector< std::vector< std::vector<size_t> > >;

%{
#include "blocks/add_ff.h"
#include "blocks/add_ss.h"
#include "blocks/add_ii.h"
#include "blocks/add_cc.h"
#include "blocks/add_const_ff.h"
#include "blocks/add_const_bb.h"
#include "blocks/add_const_ss.h"
#include "blocks/add_const_ii.h"
#include "blocks/add_const_cc.h"
#include "blocks/add_const_vff.h"
#include "blocks/add_const_vbb.h"
#include "blocks/add_const_vss.h"
#include "blocks/add_const_vii.h"
#include "blocks/add_const_vcc.h"
#include "blocks/and_bb.h"
#include "blocks/and_ss.h"
#include "blocks/and_ii.h"
#include "blocks/and_const_bb.h"
#include "blocks/and_const_ss.h"
#include "blocks/and_const_ii.h"
#include "blocks/annotator_1to1.h"
#include "blocks/annotator_alltoall.h"
#include "blocks/annotator_raw.h"
#include "blocks/argmax_fs.h"
#include "blocks/argmax_is.h"
#include "blocks/argmax_ss.h"
#include "blocks/bin_statistics_f.h"
#include "blocks/burst_tagger.h"
#include "blocks/char_to_float.h"
#include "blocks/char_to_short.h"
#include "blocks/check_lfsr_32k_s.h"
#include "blocks/complex_to_interleaved_short.h"
#include "blocks/complex_to_float.h"
#include "blocks/complex_to_real.h"
#include "blocks/complex_to_imag.h"
#include "blocks/complex_to_mag.h"
#include "blocks/complex_to_mag_squared.h"
#include "blocks/complex_to_arg.h"
#include "blocks/conjugate_cc.h"
#include "blocks/control_loop.h"
#include "blocks/copy.h"
#include "blocks/deinterleave.h"
#include "blocks/delay.h"
#include "blocks/divide_ff.h"
#include "blocks/divide_ss.h"
#include "blocks/divide_ii.h"
#include "blocks/divide_cc.h"
#include "blocks/endian_swap.h"
#include "blocks/file_descriptor_sink.h"
#include "blocks/file_descriptor_source.h"
#include "blocks/file_sink_base.h"
#include "blocks/file_sink.h"
#include "blocks/file_source.h"
#include "blocks/file_meta_sink.h"
#include "blocks/file_meta_source.h"
#include "blocks/float_to_char.h"
#include "blocks/float_to_complex.h"
#include "blocks/float_to_int.h"
#include "blocks/float_to_short.h"
#include "blocks/float_to_uchar.h"
#include "blocks/head.h"
#include "blocks/int_to_float.h"
#include "blocks/integrate_ss.h"
#include "blocks/integrate_ii.h"
#include "blocks/integrate_ff.h"
#include "blocks/integrate_cc.h"
#include "blocks/interleave.h"
#include "blocks/interleaved_short_to_complex.h"
#include "blocks/keep_m_in_n.h"
#include "blocks/keep_one_in_n.h"
#include "blocks/lfsr_32k_source_s.h"
#include "blocks/max_ff.h"
#include "blocks/max_ii.h"
#include "blocks/max_ss.h"
#include "blocks/message_debug.h"
#include "blocks/message_sink.h"
#include "blocks/message_source.h"
#include "blocks/message_strobe.h"
#include "blocks/message_burst_source.h"
#include "blocks/moving_average_cc.h"
#include "blocks/moving_average_ff.h"
#include "blocks/moving_average_ii.h"
#include "blocks/moving_average_ss.h"
#include "blocks/multiply_ss.h"
#include "blocks/multiply_ii.h"
#include "blocks/multiply_ff.h"
#include "blocks/multiply_cc.h"
#include "blocks/multiply_conjugate_cc.h"
#include "blocks/multiply_const_ss.h"
#include "blocks/multiply_const_ii.h"
#include "blocks/multiply_const_ff.h"
#include "blocks/multiply_const_cc.h"
#include "blocks/multiply_const_vss.h"
#include "blocks/multiply_const_vii.h"
#include "blocks/multiply_const_vff.h"
#include "blocks/multiply_const_vcc.h"
#include "blocks/mute_ss.h"
#include "blocks/mute_ii.h"
#include "blocks/mute_ff.h"
#include "blocks/mute_cc.h"
#include "blocks/nlog10_ff.h"
#include "blocks/nop.h"
#include "blocks/not_bb.h"
#include "blocks/not_ss.h"
#include "blocks/not_ii.h"
#include "blocks/null_sink.h"
#include "blocks/null_source.h"
#include "blocks/patterned_interleaver.h"
#include "blocks/pack_k_bits_bb.h"
#include "blocks/packed_to_unpacked_bb.h"
#include "blocks/packed_to_unpacked_ss.h"
#include "blocks/packed_to_unpacked_ii.h"
#include "blocks/pdu_to_tagged_stream.h"
#include "blocks/peak_detector_fb.h"
#include "blocks/peak_detector_ib.h"
#include "blocks/peak_detector_sb.h"
#include "blocks/peak_detector2_fb.h"
#include "blocks/plateau_detector_fb.h"
#include "blocks/probe_rate.h"
#include "blocks/probe_signal_b.h"
#include "blocks/probe_signal_s.h"
#include "blocks/probe_signal_i.h"
#include "blocks/probe_signal_f.h"
#include "blocks/probe_signal_c.h"
#include "blocks/probe_signal_vb.h"
#include "blocks/probe_signal_vs.h"
#include "blocks/probe_signal_vi.h"
#include "blocks/probe_signal_vf.h"
#include "blocks/probe_signal_vc.h"
#include "blocks/or_bb.h"
#include "blocks/or_ss.h"
#include "blocks/or_ii.h"
#include "blocks/random_pdu.h"
#include "blocks/regenerate_bb.h"
#include "blocks/repack_bits_bb.h"
#include "blocks/repeat.h"
#include "blocks/rms_cf.h"
#include "blocks/rms_ff.h"
#include "blocks/sample_and_hold_bb.h"
#include "blocks/sample_and_hold_ss.h"
#include "blocks/sample_and_hold_ii.h"
#include "blocks/sample_and_hold_ff.h"
#include "blocks/short_to_char.h"
#include "blocks/short_to_float.h"
#include "blocks/skiphead.h"
#include "blocks/socket_pdu.h"
#include "blocks/stream_mux.h"
#include "blocks/stream_to_streams.h"
#include "blocks/stream_to_vector.h"
#include "blocks/streams_to_stream.h"
#include "blocks/streams_to_vector.h"
#include "blocks/stretch_ff.h"
#include "blocks/sub_ff.h"
#include "blocks/sub_ss.h"
#include "blocks/sub_ii.h"
#include "blocks/sub_cc.h"
#include "blocks/tag_debug.h"
#include "blocks/tagged_file_sink.h"
#include "blocks/tagged_stream_mux.h"
#include "blocks/tagged_stream_to_pdu.h"
#include "blocks/threshold_ff.h"
#include "blocks/throttle.h"
#include "blocks/transcendental.h"
#include "blocks/tuntap_pdu.h"
#include "blocks/uchar_to_float.h"
#include "blocks/udp_sink.h"
#include "blocks/udp_source.h"
#include "blocks/unpack_k_bits_bb.h"
#include "blocks/unpacked_to_packed_bb.h"
#include "blocks/unpacked_to_packed_ss.h"
#include "blocks/unpacked_to_packed_ii.h"
#include "blocks/vco_f.h"
#include "blocks/vector_map.h"
#include "blocks/vector_to_stream.h"
#include "blocks/vector_to_streams.h"
#include "blocks/vector_insert_b.h"
#include "blocks/vector_insert_s.h"
#include "blocks/vector_insert_i.h"
#include "blocks/vector_insert_f.h"
#include "blocks/vector_insert_c.h"
#include "blocks/vector_sink_b.h"
#include "blocks/vector_sink_s.h"
#include "blocks/vector_sink_i.h"
#include "blocks/vector_sink_f.h"
#include "blocks/vector_sink_c.h"
#include "blocks/vector_source_b.h"
#include "blocks/vector_source_s.h"
#include "blocks/vector_source_i.h"
#include "blocks/vector_source_f.h"
#include "blocks/vector_source_c.h"
#include "blocks/wavfile_sink.h"
#include "blocks/wavfile_source.h"
#include "blocks/xor_bb.h"
#include "blocks/xor_ss.h"
#include "blocks/xor_ii.h"
%}

%include "blocks/add_ff.h"
%include "blocks/add_ss.h"
%include "blocks/add_ii.h"
%include "blocks/add_cc.h"
%include "blocks/add_const_ff.h"
%include "blocks/add_const_bb.h"
%include "blocks/add_const_ss.h"
%include "blocks/add_const_ii.h"
%include "blocks/add_const_cc.h"
%include "blocks/add_const_vff.h"
%include "blocks/add_const_vbb.h"
%include "blocks/add_const_vss.h"
%include "blocks/add_const_vii.h"
%include "blocks/add_const_vcc.h"
%include "blocks/and_bb.h"
%include "blocks/and_ss.h"
%include "blocks/and_ii.h"
%include "blocks/and_const_bb.h"
%include "blocks/and_const_ss.h"
%include "blocks/and_const_ii.h"
%include "blocks/annotator_1to1.h"
%include "blocks/annotator_alltoall.h"
%include "blocks/annotator_raw.h"
%include "blocks/argmax_fs.h"
%include "blocks/argmax_is.h"
%include "blocks/argmax_ss.h"
%include "blocks/char_to_float.h"
%include "blocks/bin_statistics_f.h"
%include "blocks/burst_tagger.h"
%include "blocks/char_to_short.h"
%include "blocks/check_lfsr_32k_s.h"
%include "blocks/complex_to_interleaved_short.h"
%include "blocks/complex_to_float.h"
%include "blocks/complex_to_real.h"
%include "blocks/complex_to_imag.h"
%include "blocks/complex_to_mag.h"
%include "blocks/complex_to_mag_squared.h"
%include "blocks/complex_to_arg.h"
%include "blocks/conjugate_cc.h"
%include "blocks/control_loop.h"
%include "blocks/copy.h"
%include "blocks/deinterleave.h"
%include "blocks/delay.h"
%include "blocks/file_descriptor_sink.h"
%include "blocks/file_descriptor_source.h"
%include "blocks/file_sink_base.h"
%include "blocks/file_sink.h"
%include "blocks/file_source.h"
%include "blocks/file_meta_sink.h"
%include "blocks/file_meta_source.h"
%include "blocks/divide_ff.h"
%include "blocks/divide_ss.h"
%include "blocks/divide_ii.h"
%include "blocks/divide_cc.h"
%include "blocks/endian_swap.h"
%include "blocks/float_to_char.h"
%include "blocks/float_to_complex.h"
%include "blocks/float_to_int.h"
%include "blocks/float_to_short.h"
%include "blocks/float_to_uchar.h"
%include "blocks/head.h"
%include "blocks/int_to_float.h"
%include "blocks/integrate_ss.h"
%include "blocks/integrate_ii.h"
%include "blocks/integrate_ff.h"
%include "blocks/integrate_cc.h"
%include "blocks/interleave.h"
%include "blocks/interleaved_short_to_complex.h"
%include "blocks/keep_m_in_n.h"
%include "blocks/keep_one_in_n.h"
%include "blocks/lfsr_32k_source_s.h"
%include "blocks/max_ff.h"
%include "blocks/max_ii.h"
%include "blocks/max_ss.h"
%include "blocks/message_debug.h"
%include "blocks/message_sink.h"
%include "blocks/message_source.h"
%include "blocks/message_strobe.h"
%include "blocks/message_burst_source.h"
%include "blocks/moving_average_cc.h"
%include "blocks/moving_average_ff.h"
%include "blocks/moving_average_ii.h"
%include "blocks/moving_average_ss.h"
%include "blocks/multiply_ss.h"
%include "blocks/multiply_ii.h"
%include "blocks/multiply_ff.h"
%include "blocks/multiply_cc.h"
%include "blocks/multiply_conjugate_cc.h"
%include "blocks/multiply_const_ss.h"
%include "blocks/multiply_const_ii.h"
%include "blocks/multiply_const_ff.h"
%include "blocks/multiply_const_cc.h"
%include "blocks/multiply_const_vss.h"
%include "blocks/multiply_const_vii.h"
%include "blocks/multiply_const_vff.h"
%include "blocks/multiply_const_vcc.h"
%include "blocks/mute_ss.h"
%include "blocks/mute_ii.h"
%include "blocks/mute_ff.h"
%include "blocks/mute_cc.h"
%include "blocks/nlog10_ff.h"
%include "blocks/nop.h"
%include "blocks/not_bb.h"
%include "blocks/not_ss.h"
%include "blocks/not_ii.h"
%include "blocks/null_sink.h"
%include "blocks/null_source.h"
%include "blocks/probe_signal_b.h"
%include "blocks/probe_signal_s.h"
%include "blocks/probe_signal_i.h"
%include "blocks/probe_signal_f.h"
%include "blocks/probe_signal_c.h"
%include "blocks/probe_signal_vb.h"
%include "blocks/probe_signal_vs.h"
%include "blocks/probe_signal_vi.h"
%include "blocks/probe_signal_vf.h"
%include "blocks/probe_signal_vc.h"
%include "blocks/or_bb.h"
%include "blocks/or_ss.h"
%include "blocks/or_ii.h"
%include "blocks/pack_k_bits_bb.h"
%include "blocks/packed_to_unpacked_bb.h"
%include "blocks/packed_to_unpacked_ss.h"
%include "blocks/packed_to_unpacked_ii.h"
%include "blocks/patterned_interleaver.h"
%include "blocks/tag_debug.h"
%include "blocks/pdu_to_tagged_stream.h"
%include "blocks/peak_detector_fb.h"
%include "blocks/peak_detector_ib.h"
%include "blocks/peak_detector_sb.h"
%include "blocks/peak_detector2_fb.h"
%include "blocks/random_pdu.h"
%include "blocks/plateau_detector_fb.h"
%include "blocks/probe_rate.h"
%include "blocks/regenerate_bb.h"
%include "blocks/repack_bits_bb.h"
%include "blocks/repeat.h"
%include "blocks/rms_cf.h"
%include "blocks/rms_ff.h"
%include "blocks/sample_and_hold_bb.h"
%include "blocks/sample_and_hold_ss.h"
%include "blocks/sample_and_hold_ii.h"
%include "blocks/sample_and_hold_ff.h"
%include "blocks/short_to_char.h"
%include "blocks/short_to_float.h"
%include "blocks/skiphead.h"
%include "blocks/socket_pdu.h"
%include "blocks/stream_mux.h"
%include "blocks/stream_to_streams.h"
%include "blocks/stream_to_vector.h"
%include "blocks/streams_to_stream.h"
%include "blocks/streams_to_vector.h"
%include "blocks/stretch_ff.h"
%include "blocks/sub_ff.h"
%include "blocks/sub_ss.h"
%include "blocks/sub_ii.h"
%include "blocks/sub_cc.h"
%include "blocks/tagged_file_sink.h"
%include "blocks/tagged_stream_mux.h"
%include "blocks/tagged_stream_to_pdu.h"
%include "blocks/threshold_ff.h"
%include "blocks/throttle.h"
%include "blocks/transcendental.h"
%include "blocks/tuntap_pdu.h"
%include "blocks/uchar_to_float.h"
%include "blocks/udp_sink.h"
%include "blocks/udp_source.h"
%include "blocks/unpack_k_bits_bb.h"
%include "blocks/unpacked_to_packed_bb.h"
%include "blocks/unpacked_to_packed_ss.h"
%include "blocks/unpacked_to_packed_ii.h"
%include "blocks/vco_f.h"
%include "blocks/vector_map.h"
%include "blocks/vector_to_stream.h"
%include "blocks/vector_to_streams.h"
%include "blocks/vector_insert_b.h"
%include "blocks/vector_insert_s.h"
%include "blocks/vector_insert_i.h"
%include "blocks/vector_insert_f.h"
%include "blocks/vector_insert_c.h"
%include "blocks/vector_sink_b.h"
%include "blocks/vector_sink_s.h"
%include "blocks/vector_sink_i.h"
%include "blocks/vector_sink_f.h"
%include "blocks/vector_sink_c.h"
%include "blocks/vector_source_b.h"
%include "blocks/vector_source_s.h"
%include "blocks/vector_source_i.h"
%include "blocks/vector_source_f.h"
%include "blocks/vector_source_c.h"
%include "blocks/wavfile_sink.h"
%include "blocks/wavfile_source.h"
%include "blocks/xor_bb.h"
%include "blocks/xor_ss.h"
%include "blocks/xor_ii.h"

GR_SWIG_BLOCK_MAGIC2(blocks, add_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, add_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, add_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, add_cc);
GR_SWIG_BLOCK_MAGIC2(blocks, add_const_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, add_const_bb);
GR_SWIG_BLOCK_MAGIC2(blocks, add_const_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, add_const_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, add_const_cc);
GR_SWIG_BLOCK_MAGIC2(blocks, add_const_vff);
GR_SWIG_BLOCK_MAGIC2(blocks, add_const_vbb);
GR_SWIG_BLOCK_MAGIC2(blocks, add_const_vss);
GR_SWIG_BLOCK_MAGIC2(blocks, add_const_vii);
GR_SWIG_BLOCK_MAGIC2(blocks, add_const_vcc);
GR_SWIG_BLOCK_MAGIC2(blocks, and_bb);
GR_SWIG_BLOCK_MAGIC2(blocks, and_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, and_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, and_const_bb);
GR_SWIG_BLOCK_MAGIC2(blocks, and_const_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, and_const_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, annotator_1to1);
GR_SWIG_BLOCK_MAGIC2(blocks, annotator_alltoall);
GR_SWIG_BLOCK_MAGIC2(blocks, annotator_raw);
GR_SWIG_BLOCK_MAGIC2(blocks, argmax_fs);
GR_SWIG_BLOCK_MAGIC2(blocks, argmax_is);
GR_SWIG_BLOCK_MAGIC2(blocks, argmax_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, bin_statistics_f);
GR_SWIG_BLOCK_MAGIC2(blocks, burst_tagger);
GR_SWIG_BLOCK_MAGIC2(blocks, char_to_float);
GR_SWIG_BLOCK_MAGIC2(blocks, char_to_short);
GR_SWIG_BLOCK_MAGIC2(blocks, check_lfsr_32k_s);
GR_SWIG_BLOCK_MAGIC2(blocks, complex_to_interleaved_short);
GR_SWIG_BLOCK_MAGIC2(blocks, complex_to_float);
GR_SWIG_BLOCK_MAGIC2(blocks, complex_to_real);
GR_SWIG_BLOCK_MAGIC2(blocks, complex_to_imag);
GR_SWIG_BLOCK_MAGIC2(blocks, complex_to_mag);
GR_SWIG_BLOCK_MAGIC2(blocks, complex_to_mag_squared);
GR_SWIG_BLOCK_MAGIC2(blocks, complex_to_arg);
GR_SWIG_BLOCK_MAGIC2(blocks, conjugate_cc);
GR_SWIG_BLOCK_MAGIC2(blocks, copy);
GR_SWIG_BLOCK_MAGIC2(blocks, deinterleave);
GR_SWIG_BLOCK_MAGIC2(blocks, delay);
GR_SWIG_BLOCK_MAGIC2(blocks, endian_swap);
GR_SWIG_BLOCK_MAGIC2(blocks, divide_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, divide_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, divide_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, divide_cc);
GR_SWIG_BLOCK_MAGIC2(blocks, file_descriptor_sink);
GR_SWIG_BLOCK_MAGIC2(blocks, file_descriptor_source);
GR_SWIG_BLOCK_MAGIC2(blocks, file_sink);
GR_SWIG_BLOCK_MAGIC2(blocks, file_source);
GR_SWIG_BLOCK_MAGIC2(blocks, file_meta_sink);
GR_SWIG_BLOCK_MAGIC2(blocks, file_meta_source);
GR_SWIG_BLOCK_MAGIC2(blocks, float_to_char);
GR_SWIG_BLOCK_MAGIC2(blocks, float_to_complex);
GR_SWIG_BLOCK_MAGIC2(blocks, float_to_int);
GR_SWIG_BLOCK_MAGIC2(blocks, float_to_short);
GR_SWIG_BLOCK_MAGIC2(blocks, float_to_uchar);
GR_SWIG_BLOCK_MAGIC2(blocks, head);
GR_SWIG_BLOCK_MAGIC2(blocks, int_to_float);
GR_SWIG_BLOCK_MAGIC2(blocks, integrate_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, integrate_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, integrate_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, integrate_cc);
GR_SWIG_BLOCK_MAGIC2(blocks, interleave);
GR_SWIG_BLOCK_MAGIC2(blocks, interleaved_short_to_complex);
GR_SWIG_BLOCK_MAGIC2(blocks, keep_m_in_n);
GR_SWIG_BLOCK_MAGIC2(blocks, keep_one_in_n);
GR_SWIG_BLOCK_MAGIC2(blocks, lfsr_32k_source_s);
GR_SWIG_BLOCK_MAGIC2(blocks, max_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, max_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, max_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, message_debug);
GR_SWIG_BLOCK_MAGIC2(blocks, message_sink);
GR_SWIG_BLOCK_MAGIC2(blocks, message_source);
GR_SWIG_BLOCK_MAGIC2(blocks, message_strobe);
GR_SWIG_BLOCK_MAGIC2(blocks, message_burst_source);
GR_SWIG_BLOCK_MAGIC2(blocks, moving_average_cc);
GR_SWIG_BLOCK_MAGIC2(blocks, moving_average_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, moving_average_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, moving_average_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, multiply_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, multiply_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, multiply_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, multiply_cc);
GR_SWIG_BLOCK_MAGIC2(blocks, multiply_conjugate_cc);
GR_SWIG_BLOCK_MAGIC2(blocks, multiply_const_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, multiply_const_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, multiply_const_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, multiply_const_cc);
GR_SWIG_BLOCK_MAGIC2(blocks, multiply_const_vss);
GR_SWIG_BLOCK_MAGIC2(blocks, multiply_const_vii);
GR_SWIG_BLOCK_MAGIC2(blocks, multiply_const_vff);
GR_SWIG_BLOCK_MAGIC2(blocks, multiply_const_vcc);
GR_SWIG_BLOCK_MAGIC2(blocks, mute_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, mute_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, mute_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, mute_cc);
GR_SWIG_BLOCK_MAGIC2(blocks, nlog10_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, nop);
GR_SWIG_BLOCK_MAGIC2(blocks, not_bb);
GR_SWIG_BLOCK_MAGIC2(blocks, not_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, not_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, null_sink);
GR_SWIG_BLOCK_MAGIC2(blocks, null_source);
GR_SWIG_BLOCK_MAGIC2(blocks, patterned_interleaver);
GR_SWIG_BLOCK_MAGIC2(blocks, pack_k_bits_bb);
GR_SWIG_BLOCK_MAGIC2(blocks, packed_to_unpacked_bb);
GR_SWIG_BLOCK_MAGIC2(blocks, packed_to_unpacked_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, packed_to_unpacked_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, peak_detector_fb);
GR_SWIG_BLOCK_MAGIC2(blocks, peak_detector_ib);
GR_SWIG_BLOCK_MAGIC2(blocks, peak_detector_sb);
GR_SWIG_BLOCK_MAGIC2(blocks, peak_detector2_fb);
GR_SWIG_BLOCK_MAGIC2(blocks, plateau_detector_fb);
GR_SWIG_BLOCK_MAGIC2(blocks, pdu_to_tagged_stream);
GR_SWIG_BLOCK_MAGIC2(blocks, probe_rate);
GR_SWIG_BLOCK_MAGIC2(blocks, or_bb);
GR_SWIG_BLOCK_MAGIC2(blocks, or_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, or_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, random_pdu);
GR_SWIG_BLOCK_MAGIC2(blocks, probe_signal_b);
GR_SWIG_BLOCK_MAGIC2(blocks, probe_signal_s);
GR_SWIG_BLOCK_MAGIC2(blocks, probe_signal_i);
GR_SWIG_BLOCK_MAGIC2(blocks, probe_signal_f);
GR_SWIG_BLOCK_MAGIC2(blocks, probe_signal_c);
GR_SWIG_BLOCK_MAGIC2(blocks, probe_signal_vb);
GR_SWIG_BLOCK_MAGIC2(blocks, probe_signal_vs);
GR_SWIG_BLOCK_MAGIC2(blocks, probe_signal_vi);
GR_SWIG_BLOCK_MAGIC2(blocks, probe_signal_vf);
GR_SWIG_BLOCK_MAGIC2(blocks, probe_signal_vc);
GR_SWIG_BLOCK_MAGIC2(blocks, regenerate_bb);
GR_SWIG_BLOCK_MAGIC2(blocks, repack_bits_bb);
GR_SWIG_BLOCK_MAGIC2(blocks, repeat);
GR_SWIG_BLOCK_MAGIC2(blocks, rms_cf);
GR_SWIG_BLOCK_MAGIC2(blocks, rms_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, sample_and_hold_bb);
GR_SWIG_BLOCK_MAGIC2(blocks, sample_and_hold_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, sample_and_hold_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, sample_and_hold_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, short_to_char);
GR_SWIG_BLOCK_MAGIC2(blocks, short_to_float);
GR_SWIG_BLOCK_MAGIC2(blocks, skiphead);
GR_SWIG_BLOCK_MAGIC2(blocks, socket_pdu);
GR_SWIG_BLOCK_MAGIC2(blocks, stream_mux);
GR_SWIG_BLOCK_MAGIC2(blocks, stream_to_streams);
GR_SWIG_BLOCK_MAGIC2(blocks, stream_to_vector);
GR_SWIG_BLOCK_MAGIC2(blocks, streams_to_stream);
GR_SWIG_BLOCK_MAGIC2(blocks, streams_to_vector);
GR_SWIG_BLOCK_MAGIC2(blocks, stretch_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, sub_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, sub_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, sub_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, sub_cc);
GR_SWIG_BLOCK_MAGIC2(blocks, tag_debug);
GR_SWIG_BLOCK_MAGIC2(blocks, tagged_file_sink);
GR_SWIG_BLOCK_MAGIC2(blocks, tagged_stream_mux);
GR_SWIG_BLOCK_MAGIC2(blocks, tagged_stream_to_pdu);
GR_SWIG_BLOCK_MAGIC2(blocks, threshold_ff);
GR_SWIG_BLOCK_MAGIC2(blocks, throttle);
GR_SWIG_BLOCK_MAGIC2(blocks, transcendental);
GR_SWIG_BLOCK_MAGIC2(blocks, tuntap_pdu);
GR_SWIG_BLOCK_MAGIC2(blocks, uchar_to_float);
GR_SWIG_BLOCK_MAGIC2(blocks, udp_sink);
GR_SWIG_BLOCK_MAGIC2(blocks, udp_source);
GR_SWIG_BLOCK_MAGIC2(blocks, unpack_k_bits_bb);
GR_SWIG_BLOCK_MAGIC2(blocks, unpacked_to_packed_bb);
GR_SWIG_BLOCK_MAGIC2(blocks, unpacked_to_packed_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, unpacked_to_packed_ii);
GR_SWIG_BLOCK_MAGIC2(blocks, vco_f);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_map);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_to_stream);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_to_streams);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_insert_b);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_insert_s);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_insert_i);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_insert_f);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_insert_c);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_sink_b);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_sink_s);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_sink_i);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_sink_f);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_sink_c);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_source_b);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_source_s);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_source_i);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_source_f);
GR_SWIG_BLOCK_MAGIC2(blocks, vector_source_c);
GR_SWIG_BLOCK_MAGIC2(blocks, wavfile_sink);
GR_SWIG_BLOCK_MAGIC2(blocks, wavfile_source);
GR_SWIG_BLOCK_MAGIC2(blocks, xor_bb);
GR_SWIG_BLOCK_MAGIC2(blocks, xor_ss);
GR_SWIG_BLOCK_MAGIC2(blocks, xor_ii);


#ifdef GR_CTRLPORT

%{
#include "blocks/ctrlport_probe_c.h"
#include "blocks/ctrlport_probe2_c.h"
%}

%include "blocks/ctrlport_probe_c.h"
%include "blocks/ctrlport_probe2_c.h"

GR_SWIG_BLOCK_MAGIC2(blocks, ctrlport_probe_c);
GR_SWIG_BLOCK_MAGIC2(blocks, ctrlport_probe2_c);

#endif /* GR_CTRLPORT */
