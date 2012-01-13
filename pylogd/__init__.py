#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pylogd is a python library for interacting with logd.  It provides
a logging handler for sending messages to logd and some simple to use stats
handlers for easily recording and sending stats."""

__all__ = ['VERSION', 'delete_log']

VERSION = (0, 2)

import socket
import msgpack
import logging
import traceback

logger = logging.getLogger(__name__)

DELETE_LOG = 1000

def delete_log(path, host='localhost', port=8126):
    """Delete the log at `path`.  This uses the DELETE_LOG message type
    in logd, so this is done over UDP and is thus async and can potentially
    fail."""
    addr = (host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(msgpack.dumps({'id': DELETE_LOG, 'path': path}), addr)
    except:
        logger.error("unexpected error:\n%s" % traceback.format_exc())

