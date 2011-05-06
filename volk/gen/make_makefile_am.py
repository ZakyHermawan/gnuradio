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

from xml.dom import minidom

def make_makefile_am(dom, machines, archflags_dict):
    tempstring = r"""
# This file is automatically generated by make_makefile_am.py.
# Do not edit this file.
    
include $(top_srcdir)/Makefile.common

AM_CPPFLAGS = $(STD_DEFINES_AND_INCLUDES) \
	-I$(top_srcdir)/include \
	-I$(top_gendir)/include \
	-Dvolk_EXPORTS \
	-fvisibility=hidden \
	$(WITH_INCLUDES)

lib_LTLIBRARIES = \
	libvolk.la

EXTRA_DIST = \
	volk_rank_archs.h 	\
	gcc_x86_cpuid.h

# ----------------------------------------------------------------
#                      The main library
# ----------------------------------------------------------------

libvolk_la_SOURCES = 	\
	$(platform_CODE) 	\
	$(top_gendir)/lib/volk.c			\
	$(top_gendir)/lib/volk_cpu.c 		\
	volk_rank_archs.c	\
	$(top_gendir)/lib/volk_machines.c

if LV_HAVE_ORC
volk_orc_CFLAGS = -DLV_HAVE_ORC=1
volk_orc_LDFLAGS = $(ORC_LDFLAGS) -lorc-0.4
volk_orc_LIBADD = ../orc/libvolk_orc.la
else
volk_orc_CFLAGS = 
volk_orc_LDFLAGS =
volk_orc_LIBADD = 
endif

libvolk_la_CPPFLAGS = $(AM_CPPFLAGS) $(volk_orc_CFLAGS)
libvolk_la_LDFLAGS = $(NO_UNDEFINED) -version-info 0:0:0 $(volk_orc_LDFLAGS)
libvolk_la_LIBADD = $(volk_orc_LIBADD)

noinst_LTLIBRARIES = 
    
"""

    #here be dragons
    for machine_name in machines:
        tempstring += "if LV_MACHINE_" + machine_name.swapcase() + "\n"
        tempstring += "libvolk_" + machine_name + "_la_SOURCES = $(top_gendir)/lib/volk_machine_" + machine_name + ".c\n"
        tempstring += "libvolk_" + machine_name + "_la_CPPFLAGS = -I$(top_srcdir)/include -I$(top_gendir)/include $(volk_orc_CFLAGS) "
        for arch in machines[machine_name]:
            if archflags_dict[arch] != "none":
                tempstring += "-" + archflags_dict[arch] + " "
                
	tempstring += "\nnoinst_LTLIBRARIES += libvolk_" + machine_name + ".la "
        tempstring += "\nlibvolk_la_LIBADD += libvolk_" + machine_name + ".la\n"
	tempstring += "libvolk_la_CPPFLAGS += -DLV_MACHINE_" + machine_name.swapcase() + " \n"
        tempstring += "endif\n"


    tempstring += r"""

# ----------------------------------------------------------------
#        The QA library.  Note libvolk.la in LIBADD
# ----------------------------------------------------------------
#libvolk_qa_la_SOURCES = \
#	qa_utils.cc

#libvolk_qa_la_LDFLAGS = $(NO_UNDEFINED) -version-info 0:0:0 -lboost

#libvolk_qa_la_LIBADD = \
#	libvolk.la \
#	libvolk_runtime.la

# ----------------------------------------------------------------
# headers that don't get installed
# ----------------------------------------------------------------
noinst_HEADERS = \
	$(top_gendir)/lib/volk_init.h \
	qa_utils.h

# ----------------------------------------------------------------
# Our test program
# ----------------------------------------------------------------
noinst_PROGRAMS = \
	testqa

testqa_SOURCES = testqa.cc qa_utils.cc
testqa_CPPFLAGS = -DBOOST_TEST_DYN_LINK -DBOOST_TEST_MAIN $(AM_CPPFLAGS)
testqa_LDFLAGS = $(BOOST_UNIT_TEST_FRAMEWORK_LIB)
testqa_LDADD  = \
	libvolk.la
"""


    return tempstring
