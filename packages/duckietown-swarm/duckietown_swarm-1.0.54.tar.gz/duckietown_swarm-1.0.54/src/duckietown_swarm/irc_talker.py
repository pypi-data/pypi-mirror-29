#! /usr/bin/env python

from collections import defaultdict
import random
import socket
from tempfile import mkdtemp
import time

from contracts import contract
from irc.bot import SingleServerIRCBot
from irc.client import ServerNotConnectedError, MessageTooLong

from . import __version__
from .crypto import CryptoKey
from .dcache import  create_propose_message
from .dcache import Envelope, CouldNotReadEnvelope
from .fragments import fragmentize, Assembler
from .ipfs_utils import IPFSInterface


class SwarmBot(SingleServerIRCBot):

    def __init__(self, servers, stream_name, mi, channel, nickname):
        SingleServerIRCBot.__init__(self, servers, nickname, nickname)
        self.mi = mi
        self.target = channel

        self.stream_name = stream_name
        self.seen = {}
        self.tmpdir = mkdtemp(prefix='swarm')

        self.admitted = False
        self.disconnected = False
        self.last_broadcast = 0

        self.lateness = random.uniform(0, 10)
        self.nusers = 10

        self.nreceived = 0
        self.assemblers = defaultdict(Assembler)

    def on_pubmsg(self, c, e):
        self._handle(c, e)

    def on_privmsg(self, c, e):
        self._handle(c, e)

    def _handle(self, _c, e):
        self.nreceived += 1
        s = str(e.arguments[0])
        # {'source': u'andrea!~andrea@nutonomy02.n.subnet.rcn.com',
        # 'tags': [], 'type': 'pubmsg', 'target': u'#duckiebots', 'arguments': [u'deplep']}
        source = e.source
        if '!' in source:
            source = source[:source.index('!')]

        sn = '/' + str(source)

        self.assemblers[sn].push(s)
        msgs = self.assemblers[sn].pop()
        for msg in msgs:
            try:
                envelope = Envelope.from_json(msg)
            except CouldNotReadEnvelope as e:
                em = 'Could not read envelope from %s: %s' % (sn, e)
                print(em)
            else:
                envelope.maddr_from = sn + envelope.maddr_from
                self.mi.dispatch(envelope)

    def on_welcome(self, connection, _event):
#        print('welcome message from %s: \n%s' % (connection.server, " ".join(event.arguments)))
        connection.join(self.target)
        print('Connected to %s on IRC server %s.' % (self.target, connection.server))
        self.admitted = True

    def on_join(self, _c, _e):
        users = self.channels[self.target].users()
        self.nusers = len(users)
#        print('current users: %s' % users)

    def on_disconnect(self, _c, event):
        print('Disconnected', event.__dict__)
        self.disconnected = True

    @contract(d=str)
    def send_message(self, target, d):
        self.connection.privmsg(target, d)
#        print('to %s: %s' % (target, d))
        self.last_broadcast = time.time()


def start_irc(mi, server, channel):
    random.seed()

    ipfsi = IPFSInterface(mi.ipfs_path)
    identity = ipfsi.ipfs_id()
    hostname = socket.gethostname()
    printable = ''.join(ch for ch in hostname if ch.isalnum())
    printable = printable[:8]
    nickname = '%s_' % (__version__[-3:].replace('.', '')) + printable + '_' + identity[-4:]
    print('Using nickname %s' % nickname)

    delta_wait_for_welcome = 60
    stream_name = '/dns4/' + server[0] + '/tcp/' + str(server[1]) + '/irc'
    assert stream_name in mi.name2queue
    assert stream_name == mi.my_maddr

    key0 = CryptoKey(str(random.randint(0, 10000)), str(random.randint(0, 10000)))
    key0.hash = ipfsi.ipfs_id()

    t = time.time()
    irc_names = [
        stream_name + '/' + nickname,
        stream_name + '/' + channel,
    ]
    for irc_name in irc_names:
        msg = create_propose_message(('pri', identity, 'addresses'), irc_name, validity=[t, t + 300])
        mi.send_to_brain('', msg, sign=True)

    c = SwarmBot([server], stream_name, mi, channel, nickname)
    while True:

        while True:
            attempt_start = time.time()
            c.admitted = False
            print('server list: %s' % [_.host for _ in c.server_list])
            c._connect()
            while not c.admitted:
                # print('Waiting for welcome')
                time.sleep(1)
                c.reactor.process_once()

                delta = time.time() - attempt_start
                give_up = delta > delta_wait_for_welcome
                if give_up:
                    print('Could not receive welcome. giving up after %d s'
                          % delta_wait_for_welcome)
                    break
            if c.admitted:
                break
            print('Changing server')
            c.jump_server()

        c.disconnected = False

        while True:
            time.sleep(1.0)
            c.reactor.process_once(1.0)
            if c.disconnected:
                break

            xs = mi.get_many_for_me(timeout=1.0)

            for envelope in xs:
                try:
                    if not envelope.maddr_to or envelope.maddr_to[0] != '/':
                        msg = 'Invalid addr_to: %r' % envelope.maddr_to
                        print(msg)
                        continue

                    tokens = envelope.maddr_to.split('/')
                    assert tokens[0] == ''  # starts with '/'
                    dest = tokens[1]  # = '#duckiebots'
                    rest = '/' + "/".join(tokens[2:])

                    envelope.maddr_to = rest
                    envelope_json = envelope.to_json()

                    limit, chunk_size = 300, 150
                    try:
                        if len(envelope_json) < limit:
                            raw = [envelope_json]
                        else:
                            raw = fragmentize(envelope_json, max_chunk_length=chunk_size)

                        for r in raw:
                            if len(r) > 415:
                                print('Do not expect a string of len %s to be ok.' % len(r))
                            c.send_message(dest, r)
                    except MessageTooLong as e:
                        print(e)
                        msg = 'Envelope size is %s' % len(envelope_json)
                        print(msg)
#                    mi.send_to_brain(envelope.maddr_to, envelope.contents)
                except ServerNotConnectedError:
                    break
