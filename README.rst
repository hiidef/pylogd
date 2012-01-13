pylogd
------

pylogd is a python interface to `logd`_.  It pushes log messages or statistics
to logd over a UDP socket.

usage
-----

pylogd ships various utilities to deal with `logd`_, python `logging`_ handlers,
and a ``Stats`` object which makes it trivial to record statistics.

logging
~~~~~~~

To log to logd using the python logging module, create a new handler with your
logd server's host and port and then set it up as your default logging handler::

    from pylogd.handlers import PylogdHandler
    handler = PylogdHandler('mylogpath.log', '127.0.0.1', 8126)
    logger = logging.getLogger()
    logger.setHandler(handler)

Now, subsequent calls to ``logger.(error|warn|etc)`` will log to your logd
server.  If you do this on the root logger (``getLogger('base')``), it will
apply to all subsequently created loggers.

To delete a log, use ``pylogd.delete_log`` with the host and port of logd::

    from pylogd import delete_log
    delete_log('mylogpath.log', host='127.0.0.1', 8126)

stats
~~~~~

To use stats, create a stats handle::

    from pylogd.stats import Logd
    stats = Logd('127.0.0.1', 8126)

You can also supply an optional prefix which will be prepended to all of your
stats, so that multiple applications can use the same logd/graphite server
without having to repeate their per-app key for every stats call.

Once you have a Logd object, you can increment & decrment counters (with an 
optional sample rate)::

    stats.increment('my.counter')
    stats.change_by('my.counter', 10)
    stats.decrement('my.counter', 0.05) # only update 5% of the time

You can also set the value of a meter::

    stats.set('my.meter', 30)
    stats.set('my.meter', 30, 0.25) # only set 25% of the time

There's a basic time interface as well as a convenient timer interface::

    stats.time('my.timer', 11.43) # time manually

    # automatically start & stop a timer
    stats.timer.start('my.timer')
    do_some_timed_operation()
    stats.timer.stop('my.timer')

    # time this function with a 10% sample rate
    @stats.timed('my.long_operation', 0.1)
    def long_operation():
        pass

    # accumulate time done doing various similar tasks
    stats.timer.start_accumulator('timers.mysql')
    do_some_mysql_stuff()
    stats.timer.stop_accumulator('timers.mysql')
    non_mysql_things()
    stats.timer.start_accumulator('timers.mysql')
    do_some_more_mysql_stuff()
    stats.timer.stop_accumulator('timers.mysql')

    # send this timing information to logd
    stats.timer.flush_accumulator('timers.mysql')


twisted support
---------------

For twisted users, use ``pylogd.twisted`` (included) instead of ``pylogd``, and 
note that log messages and stats will not go to logd until the reactor has been
started.

.. _logd: https://github.com/hiidef/logd
.. _logging: http://docs.python.org/library/logging.html
