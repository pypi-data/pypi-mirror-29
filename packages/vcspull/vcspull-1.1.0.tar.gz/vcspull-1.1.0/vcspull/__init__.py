#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manage multiple git, mercurial, svn repositories from a YAML / JSON file.

vcspull
~~~~~~~

:copyright: Copyright 2013-2018 Tony Narlock.
:license: MIT, see LICENSE for details

"""

from __future__ import absolute_import, print_function, unicode_literals

from . import cli  # NOQA

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
