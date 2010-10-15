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

swig_built_sources += @NAME@.py @NAME@_python.cc

## Various SWIG variables.  These can be overloaded in the including
## Makefile.am by setting the variable value there, then including
## Makefile.swig .

@NAME@_swiginclude_HEADERS =		\
	@NAME@.i			\
	$(@NAME@_swiginclude_headers)

@NAME@_pylib_LTLIBRARIES =		\
	_@NAME@_python.la

_@NAME@_python_la_SOURCES = 		\
	@NAME@_python.cc		\
	$(@NAME@_la_swig_sources)

_@NAME@_python_la_LIBADD =		\
	$(STD_SWIG_LA_LIB_ADD)		\
	$(@NAME@_la_swig_libadd)

_@NAME@_python_la_LDFLAGS =		\
	$(STD_SWIG_LA_LD_FLAGS)		\
	$(@NAME@_la_swig_ldflags)

_@NAME@_python_la_CXXFLAGS =		\
	$(STD_SWIG_CXX_FLAGS)		\
	$(@NAME@_la_swig_cxxflags)

@NAME@_python_PYTHON =			\
	@NAME@.py			\
	$(@NAME@_python)

if GUILE
@NAME@_pylib_LTLIBRARIES += _@NAME@_guile.la

_@NAME@_guile_la_SOURCES = 		\
	@NAME@_guile.cc		\
	$(@NAME@_la_swig_sources)

# Guile can use the same flags as python does
_@NAME@_guile_la_LIBADD = $(_@NAME@_python_la_LIBADD)
_@NAME@_guile_la_LDFLAGS = $(_@NAME@_python_la_LDFLAGS)
_@NAME@_guile_la_CXXFLAGS = $(_@NAME@_python_la_CXXFLAGS)

endif				# end of GUILE

## Entry rule for running SWIG

@NAME@_python.h @NAME@.py @NAME@_python.cc @NAME@_guile.cc @NAME@_guile.h: @NAME@.i
## This rule will get called only when MAKE decides that one of the
## targets needs to be created or re-created, because:
##
## * The .i file is newer than any or all of the generated files;
##
## * Any or all of the .cc, .h, or .py files does not exist and is
##   needed (in the case this file is not needed, the rule for it is
##   ignored); or
##
## * Some SWIG-based dependecy of the .cc file isn't met and hence the
##   .cc file needs be be regenerated.  Explanation: Because MAKE
##   knows how to handle dependencies for .cc files (regardless of
##   their name or extension), then the .cc file is used as a target
##   instead of the .i file -- but with the dependencies of the .i
##   file.  It is this last reason why the line:
##
##     	if test -f $@; then :; else
##
##   cannot be used in this case: If a .i file dependecy is not met,
##   then the .cc file needs to be rebuilt.  But if the stamp is newer
##   than the .cc file, and the .cc file exists, then in the original
##   version (with the 'test' above) the internal MAKE call will not
##   be issued and hence the .cc file will not be rebuilt.
##
## Once execution gets to here, it should always proceed no matter the
## state of a stamp (as discussed in link above).  The
## $(DEPDIR)/@NAME@-generate stuff is used to allow for parallel
## builds to "do the right thing".  The stamp has no relationship with
## either the target files or dependency file; it is used solely for
## the protection of multiple builds during a given call to MAKE.
##
## Catch signals SIGHUP (1), SIGINT (2), SIGPIPE (13), and SIGTERM
## (15).  At a caught signal, the quoted command will be issued before
## exiting.  In this case, remove any stamp, whether temporary of not.
## The trap is valid until the process exits; the process includes all
## commands appended via "\"s.
##
	trap 'rm -rf $(DEPDIR)/@NAME@-generate-*' 1 2 13 15; \
##
## Create a temporary directory, which acts as a lock.  The first
## process to create the directory will succeed and issue the MAKE
## command to do the actual work, while all subsequent processes will
## fail -- leading them to wait for the first process to finish.
##
	if mkdir $(DEPDIR)/@NAME@-generate-lock 2>/dev/null; then \
##
## This code is being executed by the first process to succeed in
## creating the directory lock.
##
## Remove the stamp associated with this filename.
##
		rm -f $(DEPDIR)/@NAME@-generate-*stamp; \
##
## Tell MAKE to run the rule for creating this stamp.
##
		$(MAKE) $(AM_MAKEFLAGS) $(DEPDIR)/@NAME@-generate-python-stamp WHAT=$<; \
		$(MAKE) $(AM_MAKEFLAGS) $(DEPDIR)/@NAME@-generate-guile-stamp WHAT=$<; \
##
## Now that the .cc, .h, and .py files have been (re)created from the
## .i file, future checking of this rule during the same MAKE
## execution will come back that the rule doesn't need to be executed
## because none of the conditions mentioned at the start of this rule
## will be positive.  Remove the the directory lock, which frees up
## any waiting process(es) to continue.
##
		rmdir $(DEPDIR)/@NAME@-generate-lock; \
	else \
##
## This code is being executed by any follower processes while the
## directory lock is in place.
##
## Wait until the first process is done, testing once per second.
##
		while test -d $(DEPDIR)/@NAME@-generate-lock; do \
			sleep 1; \
		done; \
##
## Succeed if and only if the first process succeeded; exit this
## process returning the status of the generated stamp.
##
		test -f $(DEPDIR)/@NAME@-generate-python-stamp; \
		exit $$?; \
	fi;

$(DEPDIR)/@NAME@-generate-guile-stamp:
if GUILE
	if $(SWIG) $(STD_SWIG_GUILE_ARGS) $(@NAME@_swig_args) \
		-MD -MF $(DEPDIR)/@NAME@_guile.Std \
		-module @NAME@ -o @NAME@_guile.cc $(WHAT); then \
	    if test $(host_os) = mingw32; then \
		$(RM) $(DEPDIR)/@NAME@_guile.Sd; \
		$(SED) 's,\\\\,/,g' < $(DEPDIR)/@NAME@_guile.Std \
			> $(DEPDIR)/@NAME@_guile.Sd; \
		$(RM) $(DEPDIR)/@NAME@_guile.Std; \
		$(MV) $(DEPDIR)/@NAME@_guile.Sd $(DEPDIR)/@NAME@_guile.Std; \
	    fi; \
	else \
	    $(RM) $(DEPDIR)/@NAME@_guile.S*; exit 1; \
	fi;
	touch $(DEPDIR)/@NAME@-generate-guile-stamp
	$(RM) $(DEPDIR)/@NAME@_guile.d
	cp $(DEPDIR)/@NAME@_guile.Std $(DEPDIR)/@NAME@_guile.d
	echo "" >> $(DEPDIR)/@NAME@_guile.d
	$(SED) -e '1d;s, \\,,g;s, ,,g' < $(DEPDIR)/@NAME@_guile.Std | \
		awk '{ printf "%s:\n\n", $$0 }' >> $(DEPDIR)/@NAME@_guile.d
	$(RM) $(DEPDIR)/@NAME@_guile.Std
	touch $(DEPDIR)/@NAME@-generate-guile-stamp

@am__include@ @am__quote@./$(DEPDIR)/@NAME@_guile.d@am__quote@
endif

$(DEPDIR)/@NAME@-generate-python-stamp:
## This rule will be called only by the first process issuing the
## above rule to succeed in creating the lock directory, after
## removing the actual stamp file in order to guarantee that MAKE will
## execute this rule.
##
## Call SWIG to generate the various output files; special
## post-processing on 'mingw32' host OS for the dependency file.
##
	if $(SWIG) $(STD_SWIG_PYTHON_ARGS) $(@NAME@_swig_args) \
		-MD -MF $(DEPDIR)/@NAME@_python.Std \
		-module @NAME@ -o @NAME@_python.cc $(WHAT); then \
	    if test $(host_os) = mingw32; then \
		$(RM) $(DEPDIR)/@NAME@_python.Sd; \
		$(SED) 's,\\\\,/,g' < $(DEPDIR)/@NAME@_python.Std \
			> $(DEPDIR)/@NAME@_python.Sd; \
		$(RM) $(DEPDIR)/@NAME@_python.Std; \
		$(MV) $(DEPDIR)/@NAME@_python.Sd $(DEPDIR)/@NAME@_python.Std; \
	    fi; \
	else \
	    $(RM) $(DEPDIR)/@NAME@_python.S*; exit 1; \
	fi;
##
## Mess with the SWIG output .Std dependency file, to create a
## dependecy file valid for the input .i file: Basically, simulate the
## dependency file created for libraries by GNU's libtool for C++,
## where all of the dependencies for the target are first listed, then
## each individual dependency is listed as a target with no further
## dependencies.
##
## (1) remove the current dependency file
##
	$(RM) $(DEPDIR)/@NAME@_python.d
##
## (2) Copy the whole SWIG file:
##
	cp $(DEPDIR)/@NAME@_python.Std $(DEPDIR)/@NAME@_python.d
##
## (3) all a carriage return to the end of the dependency file.
##
	echo "" >> $(DEPDIR)/@NAME@_python.d
##
## (4) from the SWIG file, remove the first line (the target); remove
##     trailing " \" and " " from each line.  Append ":" to each line,
##     followed by 2 carriage returns, then append this to the end of
##     the dependency file.
##
	$(SED) -e '1d;s, \\,,g;s, ,,g' < $(DEPDIR)/@NAME@_python.Std | \
		awk '{ printf "%s:\n\n", $$0 }' >> $(DEPDIR)/@NAME@_python.d
##
## (5) remove the SWIG-generated file
##
	$(RM) $(DEPDIR)/@NAME@_python.Std
##
## Create the stamp for this filename generation, to signal success in
## executing this rule; allows other threads waiting on this process
## to continue.
##
	touch $(DEPDIR)/@NAME@-generate-python-stamp

# KLUDGE: Force runtime include of a SWIG dependency file.  This is
# not guaranteed to be portable, but will probably work.  If it works,
# we have accurate dependencies for our swig stuff, which is good.

@am__include@ @am__quote@./$(DEPDIR)/@NAME@_python.d@am__quote@
