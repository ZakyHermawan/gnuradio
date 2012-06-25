#
# Copyright 2005,2006,2011 Free Software Foundation, Inc.
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

"""
BPSK modulation and demodulation.
"""

from math import pi, log
from cmath import exp

from gnuradio import gr
from gnuradio.digital.generic_mod_demod import generic_mod, generic_demod
import digital_swig
import modulation_utils

# /////////////////////////////////////////////////////////////////////////////
#                           BPSK constellation
# /////////////////////////////////////////////////////////////////////////////

def bpsk_constellation():
    return digital_swig.constellation_bpsk()

# /////////////////////////////////////////////////////////////////////////////
#                           BPSK modulator
# /////////////////////////////////////////////////////////////////////////////

class bpsk_mod(generic_mod):

    def __init__(self, mod_code=None, differential=False, *args, **kwargs):

        """
	Hierarchical block for RRC-filtered BPSK modulation.

	The input is a byte stream (unsigned char) and the
	output is the complex modulated signal at baseband.

        See generic_mod block for list of parameters.

        'mod_code' argument is not used.
        It exists purely to simplify generation of the block in grc.
	"""

        constellation = digital_swig.constellation_bpsk()
        super(bpsk_mod, self).__init__(constellation=constellation,
                                       differential=differential, *args, **kwargs)
        
# /////////////////////////////////////////////////////////////////////////////
#                           BPSK demodulator
#
# /////////////////////////////////////////////////////////////////////////////

class bpsk_demod(generic_demod):

    def __init__(self, mod_code=None, differential=False, *args, **kwargs):

        """
	Hierarchical block for RRC-filtered BPSK modulation.

	The input is a byte stream (unsigned char) and the
	output is the complex modulated signal at baseband.

        See generic_demod block for list of parameters.

        'mod_code' argument is not used.
        It exists purely to simplify generation of the block in grc.
        """

        constellation = digital_swig.constellation_bpsk()
        super(bpsk_demod, self).__init__(constellation=constellation,
                                         differential=differential, *args, **kwargs)



# /////////////////////////////////////////////////////////////////////////////
#                           DBPSK constellation
# /////////////////////////////////////////////////////////////////////////////

def dbpsk_constellation():
    return digital_swig.constellation_dbpsk()

# /////////////////////////////////////////////////////////////////////////////
#                           DBPSK modulator
# /////////////////////////////////////////////////////////////////////////////

class dbpsk_mod(bpsk_mod):

    def __init__(self, mod_code=None, *args, **kwargs):

        """
	Hierarchical block for RRC-filtered DBPSK modulation.

	The input is a byte stream (unsigned char) and the
	output is the complex modulated signal at baseband.

        See generic_mod block for list of parameters.

        'mod_code' argument is not used.
        It exists purely to simplify generation of the block in grc.
	"""

        super(dbpsk_mod, self).__init__(differential=True,
                                        *args, **kwargs)

# /////////////////////////////////////////////////////////////////////////////
#                           DBPSK demodulator
#
# /////////////////////////////////////////////////////////////////////////////

class dbpsk_demod(bpsk_demod):

    def __init__(self, mod_code=None, *args, **kwargs):

        """
	Hierarchical block for RRC-filtered DBPSK modulation.

	The input is a byte stream (unsigned char) and the
	output is the complex modulated signal at baseband.

        See generic_demod block for list of parameters.

        'mod_code' argument is not used.
        It exists purely to simplify generation of the block in grc.
        """

        super(dbpsk_demod, self).__init__(differential=True,
                                          *args, **kwargs)

#
# Add these to the mod/demod registry
#
modulation_utils.add_type_1_mod('bpsk', bpsk_mod)
modulation_utils.add_type_1_demod('bpsk', bpsk_demod)
modulation_utils.add_type_1_constellation('bpsk', bpsk_constellation)
modulation_utils.add_type_1_mod('dbpsk', dbpsk_mod)
modulation_utils.add_type_1_demod('dbpsk', dbpsk_demod)
modulation_utils.add_type_1_constellation('dbpsk', dbpsk_constellation)
