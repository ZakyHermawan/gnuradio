/* -*- c++ -*- */
/*
 * Copyright 2004 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

%{

#include <gr_file_sink.h>
#include <gr_file_source.h>
#include <gr_file_descriptor_sink.h>
#include <gr_file_descriptor_source.h>
#include <microtune_4702_eval_board.h>
#include <microtune_4937_eval_board.h>
#include <sdr_1000.h>
#include <gr_oscope_sink_x.h>
#include <gr_oscope_sink_f.h>
#include <ppio.h>
#include <gr_message_source.h>
#include <gr_message_sink.h>

%}

%include "gr_file_sink.i"
%include "gr_file_source.i"
%include "gr_file_descriptor_sink.i"
%include "gr_file_descriptor_source.i"
%include "microtune_xxxx_eval_board.i"
%include "microtune_4702_eval_board.i"
%include "microtune_4937_eval_board.i"
%include "sdr_1000.i"
%include "gr_oscope_sink.i"
%include "ppio.i"
%include "gr_message_source.i"
%include "gr_message_sink.i"

