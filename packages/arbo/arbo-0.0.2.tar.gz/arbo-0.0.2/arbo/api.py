# -*- coding: utf-8 -*-

"""
This module implements the arbo API

:copyright: (c) 2018 David Harrigan
"""

import logging
import sys
from datetime import datetime

from .formatters import ColorFormatter
from .handlers import DefaultHandler


DEFAULT_FORMAT = "%(levelname)s %(message)-20s %(fields)s %(threadName)s %(processName)s %(datetime)s"
_defaultLastResort = DefaultHandler(logging.INFO)
_defaultLastResort.setFormatter(ColorFormatter(fmt=DEFAULT_FORMAT))
lastResort = _defaultLastResort


class FieldsRecord(logging.LogRecord):
    def __init__(self, fields, name, level, fn, lno, msg, args, exc_info, func, sinfo):
        logging.LogRecord.__init__(self, name, level, fn, lno, msg, args, exc_info, func, sinfo)
        self.fields = fields


class Logger(logging.Logger):
    """
    Logger is an arbo implementation of the python logger.
    """

    def __init__(self, name, fields=None, level=logging.NOTSET):
        """
        Initialize the logger with a name and an optional level.
        """
        self.fields = fields or {}
        logging.Logger.__init__(self, name, level)

    def with_fields(self, **kwargs):
        """
        with_fields adds custom fields to the logging call and returns a new instance of logger which when called will
        adds the kwargs as log fields along with the fields currently set in the logger.
        """
        fields = {}
        fields.update(kwargs)
        fields.update(self.fields)
        logger = Logger(self.name, fields, self.level)
        logger.handlers = self.handlers
        return logger

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
        func=None, extra=None, sinfo=None):
        """
        A factory method which can be overridden in subclasses to create
        specialized LogRecords.
        """
        rv = FieldsRecord(self.fields, name, level, fn, lno, msg, args, exc_info, func, sinfo)
        if extra is not None:
            for key in extra:
                if (key in ["message", "asctime"]) or (key in rv.__dict__):
                    raise KeyError("Attempt to overwrite %r in LogRecord" % key)
                rv.__dict__[key] = extra[key]
        return rv

    def callHandlers(self, record):
        """
        """
        c = self
        found = 0
        while c:
            for hdlr in c.handlers:
                found = found + 1
                if record.levelno >= hdlr.level:
                    hdlr.handle(record)
            if not c.propagate:
                c = None    #break out
            else:
                c = c.parent
        if (found == 0):
            if lastResort:
                if record.levelno >= lastResort.level:
                    lastResort.handle(record)
            elif raiseExceptions and not self.manager.emittedNoHandlerWarning:
                sys.stderr.write("No handlers could be found for logger"
                                 " \"%s\"\n" % self.name)
                self.manager.emittedNoHandlerWarning = True


class RootLogger(Logger):
    """
    RootLogger is a arbo implmentation of the python RootLogger.
    """
    def __init__(self, level): 
        """
        Initialize the logger with the name "root".
        """
        Logger.__init__(self, "root", level=level)

    def __reduce__(self):
        return getLogger, ()


# arbo uses its own Manager so that it can be used independently from the built-in logger and "out of the box".  arbo
# can still replace the built-in logger by calling logging.SetLoggerClass.
root = RootLogger(logging.WARNING)
Logger.root = root
Logger.manager = logging.Manager(Logger.root)
Logger.manager.setLoggerClass(Logger)


def getLogger(name=None):
    """
    getLogger returns an arbo logger with the sepcified name, creating it if necessary.  If no name is specified,
    return the root logger.
    """
    if name:
        return Logger.manager.getLogger(name)
    else:
        return root

