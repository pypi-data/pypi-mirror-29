#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import sys
import traceback
from marshmallow import Schema, fields


class Error(Exception):
    """Error"""
    msgid = "Err-00000"

    def __init__(self, code=1, message=None, extra=None):
        self.message = message if message else self.__doc__
        Exception.__init__(self, code, self.message)
        self.code = code
        self.extra = extra or dict()
        self.stack = None

        exc_t, exc_v, exc_tb = sys.exc_info()
        if exc_t and exc_v and exc_tb:
            self.stack = "\n".join([
                x.rstrip() for x in traceback.format_exception(
                    exc_t, exc_v, exc_tb
                )
            ])

    def to_json(self):
        return ErrorSchema().dumps(self)

    @classmethod
    def from_json(cls, data):
        return ErrorSchema().load(data)

    def __repr__(self):
        return "%s<code=%s, message=%s>" % (
            self.__class__.__name__,
            self.code,
            self.message
        )

    def __str__(self):
        return "{}: {}".format(self.code, self.message)


class ErrorSchema(Schema):
    code = fields.Integer(required=True)
    message = fields.String(required=True)
    msgid = fields.String()
    extra = fields.Dict()
    stack = fields.String()


class ConfigurationError(Error):
    """Configuration error"""
    msgid = "ERR-19036"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=500, message=message, extra=extra)


# noinspection PyShadowingBuiltins
class IOError(Error):
    """I/O Error"""
    msgid = "ERR-27582"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=500, message=message, extra=extra)


# noinspection PyShadowingBuiltins
class NotImplemented(Error):
    """Not Implemented"""
    msgid = "ERR-04766"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=501, message=message, extra=extra)


class ValidationError(Error):
    """Validation error"""
    msgid = "ERR-04413"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=400, message=message, extra=extra)


class NotFound(Error):
    """Not Found"""
    msgid = "ERR-08414"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=404, message=message, extra=extra)


class InternalError(Error):
    """Internal Error"""
    msgid = "ERR-29885"

    def __init__(self, message=None, extra=None):
        Error.__init__(self, code=500, message=message, extra=extra)
