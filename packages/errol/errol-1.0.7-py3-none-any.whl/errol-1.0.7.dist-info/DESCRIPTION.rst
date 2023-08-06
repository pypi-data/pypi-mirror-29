Errol
=====

Errol is a file sender that rely on
`inotify <https://en.wikipedia.org/wiki/Inotify>`__. It can be used to
watch a directory and automatically transfers the new files (or modified
ones) with XMPP.

Prerequisites
-------------

Errol needs the following requirements:

-  A system supporting
   `inotify <https://en.wikipedia.org/wiki/Inotify>`__ (Linux).
-  an XMPP (jabber) account supporting the following XEPs: `Stream
   Management <https://xmpp.org/extensions/xep-0198.html>`__,
   `Publish-Subscribe <https://xmpp.org/extensions/xep-0060.html>`__,
   `Multi-User Chat <https://xmpp.org/extensions/xep-0045.html>`__
-  A pubsub service where the nodes can be set as open. The node name is
   defined in the configuration file. I personally use
   `sat_pubsub <https://blog.agayon.be/sat_pubsub.html>`__. A pubsub
   component developed for the project `Salut à
   Toi <https://salut-a-toi.org/>`__.
-  A Multi-User Chat because not all XMPP accounts support PubSub. For
   now, some information are still shared through MUC messages. This
   behavior could change in the future.

| You can use your own XMPP server or choose a XMPP service among the
  following list.
| https://conversations.im/compliance/

Create the pubsub node
^^^^^^^^^^^^^^^^^^^^^^

This step is optional if you already have a write access on the pubsub
node. The following example use
`jp <https://blog.agayon.be/sat_jp.html>`__, the Salut à  Toi
command-line interface but
`slixmpp <https://dev.louiz.org/projects/slixmpp>`__ or
`sleekxmpp <https://github.com/fritzy/SleekXMPP>`__ can be used.

::

    $ jp pubsub node create -f publish_model open be.agayon.errol:0 -s pubsub.agayon.be -c

The node name be.agayon.errol:0 is recommended in order to identify the
functionnality.

As an example, there are the node options on the service
pubsub.agayon.be:

::

    $ jp pubsub node info be.agayon.errol:0 -s pubsub.agayon.be
    persist_items: True
    deliver_payloads: True
    serial_ids: False
    publish_model: open
    access_model: open
    send_last_published_item: on_sub

Tests
~~~~~

You can test your setup with the examples scripts of
`slixmpp <https://git.poez.io/slixmpp>`__.

-  `pubsub_client.py <https://git.poez.io/slixmpp/tree/examples/pubsub_client.py>`__
-  `pubsub_events.py <https://git.poez.io/slixmpp/tree/examples/pubsub_events.py>`__
-  `s5b_receiver.py <https://git.poez.io/slixmpp/tree/examples/s5b_transfer/s5b_receiver.py>`__
-  `s5b_sender.py <https://git.poez.io/slixmpp/tree/examples/s5b_transfer/s5b_sender.py>`__

Example:

::

    ./s5b_file_sender.py -j jid@example.org -p pass -r john@example.org -f /path/to/file.txt 

See the scripts for more information.

Getting started with Errol
--------------------------

First you need to clone the repository. Errol needs the following
dependencies:

-  `slixmpp <https://dev.louiz.org/projects/slixmpp>`__ (python 3 only)
-  `asyncio <https://docs.python.org/3/library/asyncio.html>`__
-  `configparser <https://docs.python.org/3/library/configparser.html>`__
-  `aionotify <https://github.com/rbarrois/aionotify>`__

Installing
----------

You can easily install errol with pip:

.. code:: sh

    $ pip install errol

**git**

::

     $ python3 setup.py install

Errol can easily be installed in a
`virtualenv <https://virtualenv.pypa.io/en/stable/userguide/>`__.

**Archlinux**

::

    A PKGBUILD will be available soon.

Configuration
-------------

You need to provide information about the XMPP account.

::

    $ cat config.example.ini

    [XMPP]
    pubsub=pubsub.example.org
    node=be.agayon.errol:0
    room=chat@chat.example.org
    jid=jid@example.org/errol
    password=pass
    ressource_receiver=-receiver
    ressource_sender=-
    nick_sender=example_sender
    nick_receiver=example_receiver
    receiver=jid@example.org/errol-receiver
    presence_file=/tmp/errol_presence.txt

-  jid : the jabber account
-  password: the xmpp password
-  pubsub: the pubsub server (publish activity)
-  room: the MUC (chatroom) where errol display information.
-  presence_file: a writable file used to keep track of presences. When
   receiver is online, the file contains ‘1’ and ‘0’ otherwise.

The files will be sent by jid@example.org/errol-0 and received by
jid@example.org/errol-receiver . The nicks are the usernames used on the
MUC.

Running
-------

Once installed, Errol can be launched in a terminal.

::

    $ errol --help
    usage: errol [-h] [-e EVENTS] [-f FILE] [-d] -p PATH -c COMMAND

    Automatic XMPP file sender and directory watcher

    optional arguments:
      -h, --help            show this help message and exit
      -e EVENTS, --events EVENTS
                            Number of events to watch (delete, create modify) in
                            the directory. Once reached, the program stops.
      -f FILE, --file FILE  Config file containing XMPP parameters
      -d, --debug           set logging to DEBUG
      -p PATH, --path PATH  The path watched.
      -c COMMAND, --command COMMAND
                            The executed command: xmpp or watcher

**On device A**

If you want to watch the directory /tmp/sender, the following command
can be used:

::

    $ errol -f config.example.ini -p /tmp/sender -c watcher

All modified or new files created in the watched location will be sent
by XMPP.

**On device B**

If you want to receive the files, you have to launch Errol with the
following command line.

::

    $ errol -f config.example.ini -p /tmp/receiver -c xmpp

All the received files will be stored in the directory defined with the
option ‘-p’.

Launch with systemd
===================

Errol can be launched with systemd. Two unit files are provided to help
you:

-  errol_sender.service
-  errol_watcher.service

First, you need to create the config directory and copy the unit files.

::

    $ mkdir -p ~/.config/errol/
    $ mkdir -p ~/.config/systemd/user/
    $ cp systemd/environment.sh ~/.config/errol/
    $ cp systemd/errol_watcher.service ~/.config/systemd/user/
    $ cp systemd/errol_sender.service ~/.config/systemd/user/

Then, you can edit the environment and the unit files to match your
preferences and reload the units.

::

    $ systemctl --user daemon-reload

The units can then be launched and activated at boot:

::

    $  systemctl --user start errol_sender
    $  systemctl --user start errol_watcher
    $  systemctl --user enable errol_sender
    $  systemctl --user enable errol_watcher

If you encounter some problems, you can read the logs with the following
command:

::

    $ journalctl --user -xe
    $ systemctl --user status errol_watcher.service
    $ systemctl --user status errol_sender.service

License
-------

This project is licensed under the GPLv3 - see the
`LICENSE.txt <https://gitlab.com/jnanar/errol/blob/master/LICENCE.txt>`__
file for details

Acknowledgments
---------------

-  `Slixmpp <https://github.com/poezio/slixmpp>`__ for their nice
   library.
-  French XMPP community (sat@chat.jabberfr.org,
   jabberfr@chat.jabberfr.org)
-  Goffi from the `Salut à Toi <https://salut-a-toi.org/>`__ project.


