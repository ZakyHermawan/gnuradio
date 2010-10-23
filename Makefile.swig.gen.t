# -*- Makefile -*-
#
# Copyright 2009 Free Software Foundation, Inc.
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

# Makefile.swig.gen for @NAME@.i

## Default install locations for these files:
##
## Default location for the Python directory is:
##  ${prefix}/lib/python${python_version}/site-packages/[category]/@NAME@
## Default location for the Python exec directory is:
##  ${exec_prefix}/lib/python${python_version}/site-packages/[category]/@NAME@
##
## The following can be overloaded to change the install location, but
## this has to be done in the including Makefile.am -before-
## Makefile.swig is included.

@NAME@_pythondir_category ?= gnuradio/@NAME@
@NAME@_pylibdir_category ?= $(@NAME@_pythondir_category)
@NAME@_pythondir = $(pythondir)/$(@NAME@_pythondir_category)
@NAME@_pylibdir = $(pyexecdir)/$(@NAME@_pylibdir_category)

# The .so libraries for the guile modules get installed whereever guile
# is installed, usually /usr/lib/guile/gnuradio/
# FIXME: determince whether these should be installed with gnuradio.
@NAME@_scmlibdir = @GUILE_PKLIBDIR@/gnuradio

# The scm files for the guile modules get installed where ever guile
# is installed, usually /usr/share/guile/site/@NAME@
# FIXME: determince whether these should be installed with gnuradio.
@NAME@_scmdir = @GUILE_PKDATADIR@/gnuradio

## SWIG headers are always installed into the same directory.

@NAME@_swigincludedir = $(swigincludedir)

## This is a template file for a "generated" Makefile addition (in
## this case, "Makefile.swig.gen").  By including the top-level
## Makefile.swig, this file will be used to generate the SWIG
## dependencies.  Assign the variable TOP_SWIG_FILES to be the list of
## SWIG .i files to generated wrappings for; there can be more than 1
## so long as the names are unique (no sorting is done on the
## TOP_SWIG_FILES list). This file explicitly assumes that a SWIG .i
## file will generate .cc, .py, and possibly .h files -- meaning that
## all of these files will have the same base name (that provided for
## the SWIG .i file).
##
## This code is setup to ensure parallel MAKE ("-j" or "-jN") does the
## right thing.  For more info, see <
## http://sources.redhat.com/automake/automake.html#Multiple-Outputs >

## Stamps used to ensure parallel make does the right thing.  These
## are removed by "make clean", but otherwise unused except during the
## parallel built.  These will not be included in a tarball, because
## the SWIG-generated files will be removed from the distribution.

STAMPS += $(DEPDIR)/@NAME@-generate-*

## Other cleaned files: dependency files generated by SWIG or this Makefile

MOSTLYCLEANFILES += $(DEPDIR)/*.S*

## Add the .py and .cc files to the list of SWIG built sources.  The
## .h file is sometimes built, but not always ... so that one has to
## be added manually by the including Makefile.am .

# generating the py or scm file also generates the .cc or .h files,
# but dependencies work better without the .cc ort .h files listed.
swig_built_sources += @NAME@.py
if GUILE
swig_built_sources += @NAME@.scm
endif

## Various SWIG variables.  These can be overloaded in the including
## Makefile.am by setting the variable value there, then including
## Makefile.swig .

@NAME@_swiginclude_HEADERS =		\
	@NAME@.i			\
	$(@NAME@_swiginclude_headers)

@NAME@_pylib_LTLIBRARIES =		\
	_@NAME@.la

_@NAME@_la_SOURCES = 			\
	python/@NAME@.cc		\
	$(@NAME@_la_swig_sources)

_@NAME@_la_LIBADD =			\
	$(STD_SWIG_LA_LIB_ADD)		\
	$(@NAME@_la_swig_libadd)

# _@NAME@_la_DEPENDENCIES = python/@NAME@.lo

_@NAME@_la_LDFLAGS =			\
	$(STD_SWIG_LA_LD_FLAGS)		\
	$(@NAME@_la_swig_ldflags)

_@NAME@_la_CXXFLAGS =			\
	$(STD_SWIG_CXX_FLAGS)		\
	-I$(top_builddir) 		\
	$(@NAME@_la_swig_cxxflags)

@NAME@_python_PYTHON =			\
	@NAME@.py			\
	$(@NAME@)

if GUILE
@NAME@_scmlib_LTLIBRARIES = @NAME@_guile.la
@NAME@_guile_la_SOURCES = 		\
	guile/@NAME@.cc			\
	$(@NAME@_la_swig_sources)
@NAME@_scm_DATA = @NAME@.scm

# Guile can use the same flags as python does
@NAME@_guile_la_LIBADD = $(_@NAME@_la_LIBADD)
@NAME@_guile_la_LDFLAGS = $(_@NAME@_la_LDFLAGS)
@NAME@_guile_la_CXXFLAGS = $(_@NAME@_la_CXXFLAGS)

guile/@NAME@.lo: @NAME@.lo
@NAME@.scm: @NAME@.i

endif				# end of GUILE

python/@NAME@.lo:
@NAME@.lo: @NAME@.py @NAME@.scm
@NAME@.py: @NAME@.i

-include python/@NAME@.d
