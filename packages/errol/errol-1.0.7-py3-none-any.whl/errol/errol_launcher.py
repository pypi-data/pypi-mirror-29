#!/usr/bin/env python3
# Copyright (c) 2018 errol project
# This code is distributed under the GPLv3 License

from errol import watcher
from errol import xmpp
from errol import config_parser
import logging
import argparse


# @asyncio.coroutine
def launcher():
    parser = argparse.ArgumentParser(description='Automatic XMPP file sender and directory watcher')
    parser.add_argument("-e", "--events",
                        type=int,
                        default=10000,
                        help='Number of events to watch (delete, create modify) in the directory. '
                             'Once reached, the programs stops.')
    parser.add_argument("-f", "--file",
                        help='Config file containing XMPP parameters',
                        required=False, default='config.ini')
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)
    parser.add_argument("-p", "--path",
                        help='The path watched.',
                        required=True)

    parser.add_argument("-c", "--command",
                        help='The executed command: xmpp or watcher',
                        required=True)

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel, format='%(levelname)-8s %(message)s')

    debug = False
    if args.loglevel == logging.DEBUG:
        debug = True

    conf = config_parser.read_config(args.file)

    if args.command == "xmpp":
        xmpp_handler = xmpp.XmppHandler()
        xmpp_handler.prepare(path=args.path, filename='test.tmp', action='receive_file',
                              forever=True, xmpp_conf=conf['xmpp'],)
        xmpp_handler.update_xmpp_instance()
        xmpp_instance = xmpp_handler.ret_xmpp_instance()
        xmpp_instance.connect()
        xmpp_instance.process()
    elif args.command == "watcher":
        watcher.watch(path=args.path, events=args.events, debug=debug, conf=conf)

if __name__ == '__main__':
    launcher()
