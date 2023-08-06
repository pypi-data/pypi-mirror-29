#!/usr/bin/env python
# Copyright (c) 2018 odoo_cep project
# This code is distributed under the GPLv3 License
# The code is inspired from https://github.com/rbarrois/aionotify

import configparser


def read_config(filename='example.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    section='XMPP'
    pubsub_server = config.get(section, 'pubsub')
    node=config.get(section, 'node')
    room=config.get(section, 'room')
    jid = config.get(section, 'jid')
    password =config.get(section, 'password')
    ressource_receiver= config.get(section, 'ressource_receiver')
    ressource_sender =config.get(section, 'ressource_sender')
    nick_sender =config.get(section, 'nick_sender')
    nick_receiver = config.get(section, 'nick_receiver')
    receiver = config.get(section, 'receiver')
    presence_file = config.get(section, 'presence_file')
    conf = {'xmpp': {'pubsub_server' : pubsub_server, 'node': node, 'room': room,
                     'jid': jid, 'password':password, 'ressource_receiver': ressource_receiver,
                     'ressource_sender': ressource_sender, 'nick_sender': nick_sender,
                     'nick_receiver': nick_receiver, 'receiver':receiver, 'presence_file': presence_file}}
    return conf

if __name__ =='__main__':
    conf = read_config('../config.example.ini')
    print(conf)
