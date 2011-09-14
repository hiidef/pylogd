#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Twisted-enabled handlers for pylogd stats."""

from pylogd import stats
from pylogd.twisted import socket

class Timer(stats.Timer):
    pass

class Logd(stats.Logd):
    def __init__(self, host='localhost', port=8126, prefix=''):
        self.addr = (host, port)
        self.sock = socket.UDPSocket(host, port)
        self.prefix = prefix
        self.timer = Timer(self)

