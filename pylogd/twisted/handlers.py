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
        handlers.PylogdHandler.__init__(self, host, port)

    def makeSocket(self):
        return socket.UDPSocket(self.host, self.path)

    def createSocket(self):
        if not self.sock:
            self.sock = makeSocket()

    def send(self, msg):
        pass
