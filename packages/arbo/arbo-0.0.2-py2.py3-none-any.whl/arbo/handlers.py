# -*- coding: utf-8 -*-

"""
This module implements various handlers for arbo

:copyright: (c) 2018 David Harrigan
"""

import logging
import sys


class DefaultHandler(logging.StreamHandler):
    """
    This class is like a StreamHandler using sys.stderr, but always uses
    whatever sys.stderr is currently set to rather than the value of
    sys.stderr at handler construction time.
    """
    def __init__(self, level=logging.NOTSET):
        """
        Initialize the handler.
        """
        logging.Handler.__init__(self, level)

    @property
    def stream(self):
        return sys.stderr
