/* -*- c++ -*- */
/*
 * Copyright 2007 Free Software Foundation, Inc.
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
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */
#ifndef INCLUDED_MB_MSG_ACCEPTER_SMP_H
#define INCLUDED_MB_MSG_ACCEPTER_SMP_H

#include <mblock/msg_accepter.h>

/*!
 * \brief Concrete message acceptor that does an mb_msg_queue insertion
 */
class mb_msg_accepter_smp : public mb_msg_accepter
{
  mb_mblock_sptr	d_mb;
  pmt_t			d_port_name;
  
public:
  mb_msg_accepter_smp(mb_mblock_sptr mblock, pmt_t port_name);
  ~mb_msg_accepter_smp();

  void operator()(pmt_t signal, pmt_t data, pmt_t metadata, mb_pri_t priority);
};


#endif /* INCLUDED_MB_MSG_ACCEPTER_SMP_H */
