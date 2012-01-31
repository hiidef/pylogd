#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Configuration helpers for pylogd."""

import os
import shlex
import logging

defaults = dict(
    host = "localhost",
    port = 8126,
    logfile = "default.log",
    prefix = "stats",
)

# these locations are checked in this order
locations = ["~/.logdrc", "/etc/logd.conf", "/etc/logd/logd.conf",
    "/etc/default/logd.conf"]

def expand(path):
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path = os.path.abspath(path)
    return path

class ConfigFile(object):
    def __init__(self, path, defaults=defaults):
        self.path = path
        self.config = dict(defaults)
        if path is None or not os.path.exists(self.path):
            return
        self.parse()

    def parse(self):
        with open(self.path) as configfile:
            lexer = shlex.shlex(configfile)
            for name in lexer:
                equals = lexer.next()
                value = lexer.next()
                if name not in defaults:
                    raise ConfigError("Config option %s not valid" % name)
                if name == "port":
                    value = int(value)
                self.config[name] = value

    def update(self, d):
        self.config.update(d)

    def __getattr__(self, name):
        return self.config.get(name, '')

def autoconf(**kwargs):
    """Attempts to autoconfigure logging and returns a stats object, based
    on standard configuration files with overrides in kwargs."""
    from pylogd.handlers import PylogdHandler
    from pylogd.stats import Logd

    conf = ConfigFile(None)

    for path in locations:
        if os.path.exists(path):
            conf = ConfigFile(path)
            break

    conf.update(kwargs)

    # configure the root logger to use pylogd
    root_logger = logging.getLogger()
    for handler in filter(lambda x: x.__class__ == PylogdHandler, root_logger.handlers):
        root_logger.removeHandler(handler)
    handler = PylogdHandler(conf.logfile, host=conf.host, port=conf.port)
    root_logger.addHandler(handler)

    stats = Logd(conf.host, conf.port, conf.prefix)
    return stats


