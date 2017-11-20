#!/usr/bin/python


class InvalidConfiguration(Exception):

    def __init__(self, message=None):
        if not message:
            message = "The configuration provided was invalid"
        super(InvalidConfiguration, self).__init__(message)
