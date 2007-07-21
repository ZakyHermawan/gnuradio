#!/bin/env python
# -*- python -*-
#
# Copyright 2003 Free Software Foundation, Inc.
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

from generate_utils import *


# ----------------------------------------------------------------

def make_gr_fir_sysconfig_generic_h ():
    out = open_and_log_name ('gr_fir_sysconfig_generic.h', 'w')
    out.write (copyright)

    out.write (
'''
/*
 * WARNING: This file is automatically generated by
 * generate_gr_fir_sysconfig_generic.py.
 *
 * Any changes made to this file will be overwritten.
 */

#ifndef _GR_FIR_SYSCONFIG_GENERIC_H_
#define _GR_FIR_SYSCONFIG_GENERIC_H_

#include <gr_fir_sysconfig.h>

''')

    out.write (
'''
class gr_fir_sysconfig_generic : public gr_fir_sysconfig {
public:
''')
    
    for sig in fir_signatures:
      out.write (('  virtual gr_fir_%s *create_gr_fir_%s (const std::vector<%s> &taps);\n' %
        (sig, sig, tap_type (sig))))

    out.write ('\n')

    for sig in fir_signatures:
      out.write (('  virtual void get_gr_fir_%s_info (std::vector<gr_fir_%s_info> *info);\n' %
        (sig, sig)))

    out.write (
'''
};


#endif /* _GR_FIR_SYSCONFIG_GENERIC_H_ */
''')
    out.close ()
    

# ----------------------------------------------------------------

def make_constructor (sig, out):
    out.write ('''
static gr_fir_%s *
make_gr_fir_%s (const std::vector<%s> &taps)
{
  return new gr_fir_%s_generic (taps);
}
''' % (sig, sig, tap_type (sig), sig))
  

def make_creator (sig, out):
    out.write ('''
gr_fir_%s *
gr_fir_sysconfig_generic::create_gr_fir_%s (const std::vector<%s> &taps)
{
  return make_gr_fir_%s (taps);
}
''' % (sig, sig, tap_type (sig), sig))
    

def make_info (sig, out):
    out.write ('''
void
gr_fir_sysconfig_generic::get_gr_fir_%s_info (std::vector<gr_fir_%s_info> *info)
{
  info->resize (1);
  (*info)[0].name = "generic";
  (*info)[0].create = make_gr_fir_%s;
}
''' % (sig, sig, sig))

    
# ----------------------------------------------------------------

def make_gr_fir_sysconfig_generic_cc ():
    out = open_and_log_name ('gr_fir_sysconfig_generic.cc', 'w')
    out.write (copyright)

    out.write (
'''
/*
 * WARNING: This file is automatically generated by
 * generate_gr_fir_sysconfig_generic.py.
 *
 * Any changes made to this file will be overwritten.
 */

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif
#include <gr_fir_sysconfig_generic.h>

''')
    
    for sig in fir_signatures:
        out.write ('#include <gr_fir_%s_generic.h>\n' % (sig))

    out.write (
'''
/*
 * ----------------------------------------------------------------
 * static functions that serve as constructors returned by info
 * ----------------------------------------------------------------
 */
''')

    for sig in fir_signatures:
        make_constructor (sig, out)

    out.write (
'''
/*
 * ----------------------------------------------------------------
 * return instances of the generic C++ versions of these classes.
 * ----------------------------------------------------------------
 */
''')

    for sig in fir_signatures:
        make_creator (sig, out)

    out.write (
'''
/*
 * Return info about available implementations.
 *
 * This is the bottom of the concrete hierarchy, so we set the
 * size of the vector to 1, and install our info.  Classes derived
 * from us invoke us first, then append their own info.
 */
''')

    for sig in fir_signatures:
        make_info (sig, out)


    out.close ()

# ----------------------------------------------------------------

def generate ():
    make_gr_fir_sysconfig_generic_h ()
    make_gr_fir_sysconfig_generic_cc ()

if __name__ == '__main__':
    generate ()
