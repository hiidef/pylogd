#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Twisted-enabled handlers for logd."""

from pylogd.twisted import socket
from pylogd import handlers

class PylogdHandler(handlers.PylogdHandler):
    def __init__(self, path, host='localhost', port=8126):
        port = int(port)
        self.path = path
        # the eventual base of handlers.PylogdHandler is not new-style
        handlers.PylogdHandler.__init__(self, path, host=host, port=port)

    def makeSocket(self):
        """Re-implement makeSocket to use twisted UDPSocket."""
        return socket.UDPSocket(self.host, self.port)
