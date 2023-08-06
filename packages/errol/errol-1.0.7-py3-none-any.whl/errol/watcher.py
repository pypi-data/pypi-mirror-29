#!/usr/bin/env python
# Copyright (c) 2018 errol project
# This code is distributed under the GPLv3 License
# The code is inspired from https://github.com/rbarrois/aionotify

import aionotify
import asyncio
import signal

import os
from datetime import datetime
from . import xmpp

os.environ['PYTHONASYNCIODEBUG'] = '1'

import logging
logger = logging.getLogger(__name__)


class Watcher:
    def __init__(self):
        self.loop = None
        self.watcher = None
        self.task = None
        self.path = None
        self.count = 0
        self.xmpp_handler = None
        self.conf_xmpp = None

    def prepare(self, path, conf_xmpp):
        self.path = path
        self.conf_xmpp = conf_xmpp
        self.watcher = aionotify.Watcher()
        self.watcher.watch(path, aionotify.Flags.MODIFY | aionotify.Flags.CREATE | aionotify.Flags.DELETE)
        self.xmpp_handler = xmpp.XmppHandler()
        self.xmpp_handler.prepare(path=path, filename='test.tmp', action='send_file',
                                  forever=False, xmpp_conf=self.conf_xmpp)

    @asyncio.coroutine
    def _run(self, max_events, loop):
        yield from self.watcher.setup(self.loop)
        for _i in range(max_events):
            event = yield from self.watcher.get_event()
            msg = str(event.name) + ' - ' + str(aionotify.Flags.parse(event.flags))
            logger.info(msg)
            if 'Flags.CREATE' in msg or 'Flags.MODIFY' in msg:
                print("flag OK")
                filename = event.name
                # A new file has been uploaded
                datetime_str = str(datetime.now())
                full_filename = os.path.join(self.path , filename)
                self.count += 1
                logger.debug(self.count, filename)
                self.xmpp_handler.update_filename(filename)
                self.xmpp_handler.update_xmpp_instance()
                xmpp_instance = self.xmpp_handler.ret_xmpp_instance()
                xmpp_instance.connect()



        #self.shutdown()

    def run(self, loop, max_events):
        self.loop = loop
        self.task = loop.create_task(self._run(max_events, loop))

    def shutdown(self):
        self.watcher.close()
        if self.task is not None:
            self.task.cancel()
        self.loop.stop()

def setup_signal_handlers(loop, watcher):
    for sig in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(sig, watcher.shutdown)


def watch(path='', events=1000, debug=False, conf=None):

    wa = Watcher()
    wa.prepare(path, conf['xmpp'])
    loop = asyncio.get_event_loop()
    if debug:
        loop.set_debug(True)
    setup_signal_handlers(loop, wa)
    wa.run(loop, events)
    try:
        loop.run_forever()
    finally:
        loop.close()
