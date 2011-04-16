#
# Copyright 2010 Free Software Foundation, Inc.
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

def make_machines_c(machines):
    tempstring = r"""
// This file is automatically generated by make_machines_c.py.
// Do not edit this file.

#include <volk/volk_common.h>
#include <volk/volk_typedefs.h>
#include <volk/volk_machines.h>

struct volk_machine volk_machines[] = {    
"""
    for machine in machines:
        tempstring += """#if LV_MACHINE_""" + machine.swapcase() + "\n"
        tempstring += "volk_machine_" + machine
        tempstring += ","
        tempstring += "\n#endif\n"
    
    tempstring += r"""
};

"""

    for machine in machines:
        tempstring += "#if LV_MACHINE_" + machine.swapcase() + "\n"
        tempstring += "#define LV_MACHINE_" + machine.swapcase() + "_CNT 1\n"
        tempstring += "#else\n"
        tempstring += "#define LV_MACHINE_" + machine.swapcase() + "_CNT 0\n"
        tempstring += "#endif\n"
        
    tempstring += """unsigned int n_volk_machines = 
"""
    for machine in machines:
        tempstring += "(LV_MACHINE_" + machine.swapcase() + "_CNT) "
        tempstring += "+ "
    tempstring = tempstring[:-2]
    tempstring += ";\n"

    return tempstring
