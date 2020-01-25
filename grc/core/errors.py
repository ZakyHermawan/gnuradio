# Copyright 2016 Free Software Foundation, Inc.
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-2.0-or-later
# 

from __future__ import absolute_import, print_function


class GRCError(Exception):
    """Generic error class"""


class BlockLoadError(GRCError):
    """Error during block loading"""


class TemplateError(BlockLoadError):
    """Mako Template Error"""
