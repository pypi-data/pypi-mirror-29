#!/usr/bin/env python
# Copyright (c) 2018 odoo_cep project
# This code is distributed under the GPLv3 License

import os
import asyncio
import logging
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout, XMPPError
from slixmpp.xmlstream import ET
from datetime import datetime

os.environ['PYTHONASYNCIODEBUG'] = '1'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REMOTE_FILENAME = 'remote.file'


class XmppManager(slixmpp.ClientXMPP):
    """
    A basic example of creating and using a SOCKS5 bytestream.
    """

    def __init__(self, jid=None, password=None, receiver=None, filename=None, server=None,
                 action=None, full_filename=None, node=None, path=None,
                 nick='cep', presence_file='/tmp/test.txt'):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        # loop = asyncio.get_event_loop()
        # self.init_future = loop.run_in_executor(None, self._reading_init)
        logger.info("XMPP Initialization")
        self.remote_filename = None
        self.receiver = receiver
        self.full_filename = full_filename
        self.filename = filename
        self.node = node
        self.pubsub_server = server
        self.action = action
        self.file_obj = None
        self.path = path
        self.presence_file = presence_file
        # at first, the receiver is marked offline
        self.write_presence_file(0)
        self.received = set()
        self.presences_received = asyncio.Event()
        if action == 'receive_file':
            # FIXME open a temporary file but rename it after
            self.file_obj = open(self.full_filename, 'wb')
        self.nick = nick
        # FIXME config
        self.room = 'bot@chat.agayon.be'
        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use.

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        # self.add_event_handler("muc::%s::got_online" % self.room,
        #                       self.muc_online)
        self.add_event_handler("groupchat_message", self.muc_message)

        self.add_event_handler("socks5_connected", self.stream_opened)
        self.add_event_handler("socks5_data", self.stream_data)
        self.add_event_handler("socks5_closed", self.stream_closed)

        self.add_event_handler('pubsub_publish', self._publish)
        self.add_event_handler('pubsub_purge', self._purge)
        self.add_event_handler("changed_status", self.wait_for_presences)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        pubsub_template_file = os.path.join(dir_path, './data/template.xml')
        with open(pubsub_template_file, 'r') as xmlfile:
            txt_xml = xmlfile.read()
        self.xml_publish = txt_xml

    @asyncio.coroutine
    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.plugin['xep_0045'].join_muc(self.room,
                                         self.nick,
                                         # If a room password is needed, use:
                                         # password=the_room_password,
                                         wait=True)

        logger.info("START")
        # try:
        #    yield from self.publish()
        # except:
        #    logger.error('START: could not execute: publish')

        # yield  from self.send_msg("PLOP") # OK
        if self.action == 'send_file':
            # yield from self.send_msg("I am online :-)")
            logger.info("Send file")
            yield from self.send_file()

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
            logger.debug("Received message : {}".format(msg['body']))

    @asyncio.coroutine
    def send_msg(self, msg):
        self.send_message(mto=self.receiver,
                          mbody=msg,
                          mtype='chat')  # normal or chat

    def send_muc(self, msg):
        self.send_message(mto=self.room,
                          mbody=msg,
                          mtype='groupchat')

    def muc_online(self, presence):
        """
        Process a presence stanza from a chat room. In this case,
        presences from users that have just come online are
        handled by sending a welcome message that includes
        the user's nickname and role in the room.

        Arguments:
            presence -- The received presence stanza. See the
                        documentation for the Presence stanza
                        to see how else it may be used.
        """
        if 'cep' not in presence['muc']['nick']:
            # mto=presence['from'].bare,
            self.send_message(mto=self.room,
                              mbody="Bonjour, %s %s" % (presence['muc']['role'],
                                                        presence['muc']['nick']),
                              mtype='groupchat')

    def muc_message(self, msg):
        """
            Process incoming message stanzas from any chat room. Be aware
            that if you also have any handlers for the 'message' event,
            message stanzas may be processed by both handlers, so check
            the 'type' attribute when using a 'message' event handler.
            Whenever the bot's nickname is mentioned, respond to
            the message.
            IMPORTANT: Always check that a message is not from yourself,
                       otherwise you will create an infinite loop responding
                       to your own messages.
            This handler will reply to messages that mention
            the bot's nickname.
            Arguments:
                msg -- The received message stanza. See the documentation
                       for stanza objects and the Message stanza to see
                       how it may be used.
            """
        if msg['mucnick'] != self.nick and self.nick in msg['body']:
            self.send_message(mto=msg['from'].bare,
                              mbody="I heard that, %s." % msg['mucnick'],
                              mtype='groupchat')

        if 'sender' in msg['mucnick']:
            if 'New file: ' in msg['body']:
                msg_split = msg['body'].split(': ')
                filename = msg_split[1]
                print(filename)
                self.remote_filename = filename

    # FILE STREAM s5b #

    # SEND FILE
    @asyncio.coroutine
    def send_file(self, ):
        logger.info("Send file")
        self.file_obj = open(self.full_filename, 'rb')
        try:
            # Open the S5B stream in which to write to.
            proxy = yield from self['xep_0065'].handshake(self.receiver)

            # Send the entire file.
            while True:
                data = self.file_obj.read(1048576)
                if not data:
                    break
                yield from proxy.write(data)

            # And finally close the stream.
            proxy.transport.write_eof()
        except (IqError, IqTimeout) as ex:
            logger.error('File transfer errored')
            logger.error(ex)
        else:
            logger.info('File transfer finished')
        finally:
            self.file_obj.close()
            # self.disconnect()
            yield from self.publish('sent')
            self.send_muc("Send file: {}".format(self.filename))

    # Receive file
    def stream_opened(self, sid):

        logger.info('Stream opened. %s', sid)

    def stream_data(self, data):
        self.file_obj.write(data)

    @asyncio.coroutine
    def stream_closed(self, exception):
        logger.info('Stream closed. %s', exception)
        self.file_obj.close()
        if not self.path in self.filename:
            self.send_muc("New file: {}".format(self.filename))
        if self.action == 'receive_file':
            yield from self.publish('received')
            path = os.path.dirname(self.full_filename)
            asyncio.sleep(5)
            if self.remote_filename:
                full_remote_filename = os.path.join(path, self.remote_filename)
            else:
                full_remote_filename = os.path.join(path, 'remote_not_found.file.xlsx')

            os.rename(self.full_filename, full_remote_filename)
            self.file_obj = open(self.full_filename, 'wb')

        # Once we have receive the file, we can disconnect
        if self.action == 'send_file':
            self.disconnect()

    # PUBSUB
    # EVENTS
    def _publish(self, msg):
        """Handle receiving a publish item event."""
        log_msg = 'Published item %s to %s:' % (
            msg['pubsub_event']['items']['item']['id'],
            msg['pubsub_event']['items']['node'])
        logger.info(log_msg)
        data = msg['pubsub_event']['items']['item']['payload']
        if data is not None:
            log_msg = "data in publish = {}".format(data)
            logger.info(log_msg)

        else:
            print('No item content')

    def _purge(self, msg):
        """Handle receiving a node purge event."""
        print('Purged all items from %s' % (
            msg['pubsub_event']['purge']['node']))

    @asyncio.coroutine
    def publish(self, action):

        string_entry = self.xml_publish
        datetime_str = str(datetime.now())
        # print(self.filename)
        string_entry = string_entry.replace('DATE', datetime_str).replace('*FILE*', self.filename).replace('ACTION',
                                                                                                           action)
        string_entry = string_entry.replace('AUTHOR', self.jid)
        # print(string_entry)
        payload = ET.fromstring(string_entry)
        try:
            result = yield from self['xep_0060'].publish(self.pubsub_server, self.node, payload=payload)
            logger.info('Published at item id: %s', result['pubsub']['publish']['item']['id'])
        except XMPPError as error:
            logger.error('PUBLISH ERROR: Could not publish to %s: %s', self.node, error.format())

    def wait_for_presences(self, presence):
        """
        track presence changes
        Inspired by https://github.com/poezio/slixmpp/blob/master/examples/roster_browser.py
        Thanks to Link Mauve
        """

        self.received.add(presence['from'])
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

        if self.receiver == str(presence['from']):
            if 'unavailable' == str(presence.values['type']):
                self.write_presence_file(0)
            else:
                self.write_presence_file(1)


    def write_presence_file(self, msg):
        try:
            with open(self.presence_file, 'w') as pf:
                pf.write('{}\n'.format(msg))
        except FileNotFoundError:
            self.create_presence_file(self.presence_file)


    def create_presence_file(self,presence_file):
        # the default presence is 0 (not connected)
        logger.info('Presence file {} donot exist. We create it with a disconnected value (0)'.format(self.presence_file))
        with open(presence_file, 'w') as pf:
            pf.write('0\n')


class XmppHandler:
    def __init__(self):
        self.tmp_filename = None
        self.jid = None
        self.password = None
        self.receiver = None
        self.node = None
        self.server = None
        self.nick = None
        self.xmpp_instance = None
        self.forever = None
        self.debug = None
        self.path = None
        self.action = None
        self.filename = None
        self.full_filename = None

    def prepare(self, path=None, filename=None, action=None, forever=False, debug=False, xmpp_conf=None):
        logger.info("Start XMPP")
        self.path = path
        self.action = action
        self.forever = forever
        self.tmp_filename = 'tmp.file'
        self.jid = xmpp_conf['jid']
        self.password = xmpp_conf['password']
        self.receiver = xmpp_conf['receiver']
        self.node = xmpp_conf['node']
        self.server = xmpp_conf['pubsub_server']
        self.debug = debug
        self.presence_file = xmpp_conf['presence_file']
        if self.jid is None or self.password is None or self.receiver is None:
            logger.error("Error in config file")
            return 1

        if self.action == 'send_file':
            self.full_filename = os.path.join(path, filename)
            self.jid = self.jid + xmpp_conf['ressource_sender']
            self.nick = xmpp_conf['nick_sender']
        else:
            self.filename = os.path.join(self.path, self.tmp_filename)
            self.full_filename = self.filename
            self.jid = self.jid + xmpp_conf['ressource_receiver']
            self.nick = xmpp_conf['nick_receiver']

    @asyncio.coroutine
    def xmp_connect(self, ):
        logger.debug("Connect")
        self.xmpp_instance.connect()
        logger.debug('Process')
        # self.xmpp_instance.process(forever=self.forever)

    def ret_xmpp_instance(self):
        return self.xmpp_instance

    def update_filename(self, filename):
        self.filename = filename
        if self.action == 'send_file':
            self.full_filename = os.path.join(self.path, filename)
        else:
            self.filename = os.path.join(self.path, self.tmp_filename)
            self.full_filename = self.filename

    def update_xmpp_instance(self):
        self.xmpp_instance = XmppManager(jid=self.jid, password=self.password, receiver=self.receiver,
                                         filename=self.filename,
                                         server=self.server, action=self.action,
                                         full_filename=self.full_filename, node=self.node, nick=self.nick,
                                         path=self.path, presence_file=self.presence_file)

        self.xmpp_instance.register_plugin('xep_0030')  # Service Discovery
        # xmpp.register_plugin('xep_0065')  # SOCKS5 Bytestreams
        self.xmpp_instance.register_plugin('xep_0065', {'auto_accept': True})  # SOCKS5 Bytestreams
        self.xmpp_instance.register_plugin('xep_0030')
        self.xmpp_instance.register_plugin('xep_0045')
        self.xmpp_instance.register_plugin('xep_0059')
        self.xmpp_instance.register_plugin('xep_0060')


if __name__ == '__main__':
    PATH = '/home/arnaud/files/programmation/python/django/cep/odoo_cep/static/withdraw'
    file_name = 'test.txt'
    action = 'send_file'
