#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A twisted UDP interface that is similar to the built-in socket interface."""

import traceback

from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol

class UDPSocket(DatagramProtocol):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.task = None
        reactor.callWhenRunning(self.connect)

    def connect(self):
        self.task = reactor.listenUDP(0, self)

    def connectTransport(self, ip):
        self.transport.connect(ip, self.port)

    def startProtocol(self):
        """Start the protocol.  Resolve the host in case it is a hostname,
        then call connect on the resulting ip and configured port."""
        reactor.resolve(self.host).addCallback(self.connectTransport)

    def sendto(self, msg, addr):
        # ignore the addr, because we only send to one place
        try:
            self.transport.write(msg)
        except AttributeError:
            # trying to log before twisted is running, nothing we can really do
            pass
        except AssertionError:
            # trying to log before connection yields an assertion error
            pass

    def close(self):
        return
