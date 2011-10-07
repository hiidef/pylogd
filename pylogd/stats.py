#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Logd's stats implementation.  Similar to the python_example in statsd's
repository."""

import time
import msgpack
import random
import socket
import traceback
import logging
import functools

logger = logging.getLogger(__name__)

# these are taken from logd.js

COUNTER = 2
TIMER = 3
METER = 4

class Timer(object):
    def __init__(self, logd):
        self.logd = logd
        self.timers = {}
        self.accs = {}

    def start(self, name, sample_rate=1):
        """Start a simple timer.  If a timer is started twice in a row, the
        old timing information is never sent."""
        self.timers[name] = (time.time(), sample_rate)

    def end(self, name):
        """End a timer and send a delta to logd."""
        if name not in self.timers:
            return
        t0, sample_rate = self.timers.pop(name)
        dt = time.time() - t0
        self.logd.time(name, dt, sample_rate)

    stop = end

    def start_accumulator(self, name, sample_rate=1):
        """Start an accumulator.  This is a timer that can take multiple
        readings before being sent out so you can measure aggregate time
        spent on certain tasks (network wait, etc)."""
        if name in self.accs:
            self.accs[name][0] = time.time()
        else:
            self.accs[name] = (time.time(), sample_rate, 0)

    def end_accumulator(self, name):
        """End an accumulator section."""
        if name not in self.accs:
            return
        t0, sample_rate, acc = self.accs[name]
        acc += time.time() - t0
        self.accs[name] = (0, sample_rate, acc)

    def flush_accumulator(self, name):
        """Flush an accumulator to logd."""
        if name not in self.accs:
            return
        _, sample_rate, dt = self.accs.pop(name)
        self.logd.time(name, dt, sample_rate)

    def flush(self):
        """Flush all accumulators."""
        for name in list(self.accs):
            _, sample_rate, dt = self.accs.pop(name)
            self.logd.time(name, dt, sample_rate)

class Logd(object):

    def __init__(self, host='localhost', port=8126, prefix=''):
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.prefix = prefix
        self.timer = Timer(self)

    def time(self, stat, time, sample_rate=1):
        """Log timing information."""
        self.send({'id': TIMER, 'key': stat, 'value': time}, sample_rate)

    def timed(self, name, sample_rate=1):
        """A decorator that wraps a function call in a timed block."""
        def decorator(f):
            @functools.wrap(f)
            def wrapped(*args, **kwargs):
                self.timer.start(name, sample_rate)
                ret = f(*args, **kwargs)
                self.timer.end(name)
                return ret
            return wrapped
        return decorator

    def set(self, stat, value, sample_rate=1):
        """Set a meter."""
        self.send({'id': METER, 'key': stat, 'value': value}, sample_rate)

    def increment(self, stat, sample_rate=1):
        """Increment a counter."""
        self.change_by(stat, 1, sample_rate)

    def decrement(self, stat, sample_rate=1):
        """Decrement a counter."""
        self.change_by(stat, -1, sample_rate)

    def change_by(self, stat, by, sample_rate=1):
        """Change a counter by ``by``."""
        self.send({'id': COUNTER, 'key': stat, 'value': by}, sample_rate)

    def send(self, data, sample_rate=1):
        """Send data over the wire to logd."""
        if sample_rate < 1:
            if random.random() > sample_rate:
                return
            data['rate'] = sample_rate
        if self.prefix:
            data['key'] = '%s:%s' % (self.prefix, data['key'])
        msg = msgpack.dumps(data)
        try:
            self.sock.sendto(msg, self.addr)
        except:
            # ironically, this might make its way to logd...
            logger.error("unexpected error:\n%s" % traceback.format_exc())


class Dummy(Logd):
    """A version of stats.Logd which does not send stats over the wire. """

    def send(self, data, sample_rate=1):
        """Do not send any data (DUMMY)."""
        return None
