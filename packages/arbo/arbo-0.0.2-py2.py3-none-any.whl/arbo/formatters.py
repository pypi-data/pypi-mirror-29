# -*- coding: utf-8 -*-

"""
This module implements various formatters for arbo

:copyright: (c) 2018 David Harrigan
"""

# stdlib
import logging
from datetime import datetime


class AnsiCodes(object):
    """
    http://en.wikipedia.org/wiki/ANSI_escape_code
    """
    RESET = 0
    BOLD = 1

    # Colors
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

    def __init__(self):
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                code = '\033[{}m'.format(value)
                setattr(self, name, code)


CODES = AnsiCodes()
COLORS = {
    'INFO': CODES.BLUE,
    'DEBUG': CODES.WHITE,
    'WARNING': CODES.YELLOW,
    'ERROR': CODES.RED,
    'CRITICAL': CODES.RED,
}
LEVEL_NAME = {
    'INFO': 'INFO ',
    'DEBUG': 'DEBUG',
    'WARNING': 'WARN ',
    'ERROR': 'ERROR',
    'CRITICAL': 'CRIT',
}


def color_format(color, message):
    """
    Returns a new string with the given color and the rest sequence
    """
    return color + message + CODES.RESET


class ColorFormatter(logging.Formatter):

    def __init__(self, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record):
        color = COLORS.get(record.levelname, CODES.WHITE)
        short_level = LEVEL_NAME[record.levelname]
        record.levelname = color_format(color, short_level)

        # Add datetime attribute
        record.datetime = datetime.fromtimestamp(record.created).strftime("%Y-%m-%dT%H:%M:%S.%f")

        # Formatt and colorize other attributes
        # Attributes: levelno, lineno, process, thread convert from int to str
        types = (str, int, float,)
        for attr_name in dir(record):
            if not(attr_name.startswith('__') and attr_name.endswith('__')):
                # Unchangeable Attributes
                if attr_name not in ['msg', 'args', 'exc_info', 'levelname', 'levelno']:
                    attr_val = getattr(record, attr_name)
                    if isinstance(attr_val, types):
                        val = '{}={}'.format(color_format(color, attr_name), attr_val)
                        setattr(record, attr_name, val)

        # Colorize the fields attribute
        fields = getattr(record, 'fields', {})
        colorized = []
        for k, v in fields.items():
            colorized.append('{}={}'.format(color_format(color, k), v))
        setattr(record, 'fields', ' '.join(colorized))

        message = logging.Formatter.format(self, record)
        return message
