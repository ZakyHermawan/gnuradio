#!/usr/bin/env python
#
# Copyright 2012 Free Software Foundation, Inc.
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

import os
import re
import sys
import volk_arch_defs
import volk_machine_defs
import volk_kernel_defs
from Cheetah import Template

def __escape_pre_processor(code):
    out = list()
    for line in code.splitlines():
        m = re.match('^(\s*)#(\s*)(\w+)(.*)$', line)
        if m:
            p0, p1, fcn, stuff = m.groups()
            conly = fcn in ('include', 'define', 'ifdef', 'ifndef', 'endif', 'elif')
            both = fcn in ('if', 'else')
            istmpl = '$' in stuff
            if conly or (both and not istmpl):
                line = '%s\\#%s%s%s'%(p0, p1, fcn, stuff)
        out.append(line)
    return '\n'.join(out)

def __parse_tmpl(_tmpl, **kwargs):
    defs = {
        'archs': volk_arch_defs.archs,
        'machines': volk_machine_defs.machines,
        'kernels': volk_kernel_defs.kernels,
    }
    defs.update(kwargs)
    _tmpl = __escape_pre_processor(_tmpl)
    _tmpl = """

/* this file was generated by volk template utils, do not edit! */

""" + _tmpl
    return str(Template.Template(_tmpl, defs))

if __name__ == '__main__':
    print __parse_tmpl(open(sys.argv[1]).read())
