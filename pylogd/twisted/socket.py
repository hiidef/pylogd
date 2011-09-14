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
        reactor.callWhenRunning(self.connect)

    def connect(self):
        self.task = reactor.listenUDP(self)

    def startProtocol(self):
        self.transport.connect(host, port)

    def sendto(self, msg, addr):
        # ignore the addr, because we only send to one place
        try:
            self.transport.write(msg)
        except:
            traceback.print_exc()


    def close(self):
        return
