#
# Copyright 2010-2011 Free Software Foundation, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from volk_regexp import *

def make_machines_h(functions, machines, archs):
    tempstring = r"""
// This file is automatically generated by make_machines_h.py.
// Do not edit this file.

#ifndef INCLUDED_LIBVOLK_MACHINES_H
#define INCLUDED_LIBVOLK_MACHINES_H

#include <volk/volk_common.h>
#include <volk/volk_typedefs.h>

__VOLK_DECL_BEGIN

struct volk_machine {
   const unsigned int caps; //capabilities (i.e., archs compiled into this machine, in the volk_get_lvarch format)
   const char *name;
   const unsigned int alignment; //the maximum byte alignment required for functions in this library
"""
    for function in functions:
        tempstring += "    const char *%s_name;\n"%function
        tempstring += "    const char *%s_indices[%d];\n"%(function, len(archs))
        tempstring += "    const int %s_arch_defs[%d];\n"%(function, len(archs))
        tempstring += "    const %s %s_archs[%d];\n"%(replace_volk.sub("p", function), function, len(archs))
        tempstring += "    const int %s_n_archs;\n"%function
    
    tempstring += r"""};
    
"""
    for machine in machines:
        tempstring += """#if LV_MACHINE_""" + machine.swapcase() + "\n"
        tempstring += "extern struct volk_machine volk_machine_" + machine + ";\n"
        tempstring += """#endif\n"""
    
    tempstring += r"""

__VOLK_DECL_END

#endif //INCLUDED_LIBVOLK_MACHINES_H"""

    return tempstring
