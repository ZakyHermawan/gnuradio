/* -*- c++ -*- */
/*
 * Copyright 2006 Free Software Foundation, Inc.
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

#ifndef INCLUDED_N2BS_H
#define INCLUDED_N2BS_H

#include <string>
#include <algorithm>

std::string _n2bs_helper(unsigned long long v, size_t nbinary_digits);

template<class T>
std::string n2bs(T v, size_t nbinary_digits)
{
  return _n2bs_helper((unsigned long long)v, std::min(nbinary_digits, 8 * sizeof(T)));
}

#endif /* INCLUDED_N2BS_H */
