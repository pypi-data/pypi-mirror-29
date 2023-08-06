from Queue import Empty
import argparse
from collections import OrderedDict
from duckietown_swarm import __version__
from duckietown_swarm.utils import duration_compact
import getpass
import random
import subprocess
import sys

from contracts import contract
from system_cmd import CmdException
from termcolor import colored
import yaml

from .brain import DistributedRepoSwarm
from .constants import DSwarmConstants
from .dcache import Envelope, interpret_message
from .dcache_wire import create_command_message
from .dcache_wire import create_request_message, MsgPong
from .ipfs_utils import IPFSInterface
from .irc2 import duckietown_swarm_main
from .packaging import find_more_information
from .ping import duckietown_swarm_ping_main
from .socket_utils import AsyncLineBasedConnection
from .utils import now_until


@contract(returns=DistributedRepoSwarm, patterns=list)
def get_snapshot(host, port, patterns):

    albc = AsyncLineBasedConnection(host, port)
    maddr_from = '/cli'

    inbound = albc.get_q_inbound()
    outbound = albc.get_q_outbound()

    msg = create_request_message(patterns, validity=now_until(105))

    e = Envelope(maddr_from=maddr_from,
                 maddr_to='/dswarm/*/brain',
                 contents=msg)

    outbound.put(e)

    dc = DistributedRepoSwarm()
    from_channel = 'stdin'
    i = 0

#    wait_since_last = 15.0
#    t_last = time.time()
    while True:
        try:
            env = inbound.get(block=True, timeout=1.0)
#            t_last = time.time()
            is_signature = 'signature' in env.contents
            if is_signature:
                sys.stderr.write('S')
            else:
                sys.stderr.write('r')
        except Empty:
            pass
#            if i > 0:
#                if time.time() - t_last > wait_since_last:
#                    break
        else:
#            print env
            msg = interpret_message(env.contents)
            if isinstance(msg, MsgPong):
                break
            dc.process(env.contents, from_channel)
        i += 1
    print('processed %s messages' % i)
    return dc


commands = OrderedDict()


def command(x):
    commands[x.__name__.replace('cmd_', '')] = x
    return x


@command
def cmd_version(parsed, args):  #@UnusedVariable
    print('%s' % __version__)


@command
def cmd_summary(parsed, args):
    ''' Writes summary'''
    host = parsed.host
    port = DSwarmConstants.port_dswarm

    if args:
        what = args
    else:
        what = ['*']

    dc = get_snapshot(host, port, what)
    data = dc.summary_dict()

    print(yaml.dump(data))


@command
def cmd_online(parsed, args):
    host = parsed.host
    port = DSwarmConstants.port_dswarm

    what = ['/pri/*/version/dswarm', '/pri/*/info/hostname']

    dc = get_snapshot(host, port, what)
    data = dc.summary_dict(True, True)
    print
    h = []
    hosts = list(data['pri'])
    for mh in hosts:
        hostname = data['pri'][mh]['info']['hostname']['value']
        version = data['pri'][mh]['info']['version']['dswarm']['value']
        age = data['pri'][mh]['info']['version']['dswarm']['age']
        h.append(dict(version=version, age=age, hostname=hostname, mh=mh))

    h = sorted(h, key=lambda x: x['age'])
    for x in h:
        print('%s   %7s  %10s   %s' % (x['mh'], x['version'], duration_compact(x['age']), x['hostname'],))

#    print(yaml.dump(data))


@command
def cmd_help(parsed, args):  #@UnusedVariable
    print("Commands available:\n")
    for name, cmd in commands.items():
        use = 'dt-swarm %s ' % colored(name, attrs=['bold'])
        doc = cmd.__doc__
        if doc is not None: doc = doc.strip()
        else:
            doc = ''
        print('   %-20s %s' % (use, doc))


@command
def cmd_report(parsed, args):
    host = parsed.host
    port = DSwarmConstants.port_dswarm

    what = ['/verified', '/files', '/safe']
    dc = get_snapshot(host, port, what)
    ipfsi = IPFSInterface(None)

    if args:
        find_provs = True
        provs_timeout = args.pop(0)
    else:
        find_provs = False
        provs_timeout = None

    s = create_safe_index(ipfsi, dc, find_provs, provs_timeout)
    mh = ipfsi.add(s)
    url = 'http://localhost:6080/ipfs/' + mh

    print url


@command
def cmd_ipfs(_parsed, args):
    ipfsi = IPFSInterface(None)
    ipfs = ipfsi.get_executable()
    cmd = [ipfs] + args
    p = subprocess.Popen(
            cmd,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            bufsize=0,
            cwd='.',
            env=ipfsi._get_env())
    p.wait()


@command
def cmd_ping(_, _a):
    duckietown_swarm_ping_main()


@command
def cmd_daemon(_parsed, _args):
    duckietown_swarm_main()


def duckietown_swarm_cli_main():

    if len(sys.argv) == 1:
        cmd_help(None, [])
        return

    parser = argparse.ArgumentParser(description='Ping the swarm')
    parser.add_argument('--host', type=str, help='host to use', default='localhost')
    parser.add_argument('command', type=str, help='command')
    parser.add_argument('rest', nargs=argparse.REMAINDER, help='rest')
    parsed = parser.parse_args()

    cmd = parsed.command
    args = parsed.rest

    if not cmd in commands:
        cmd_help(parsed, args)
        return

    f = commands[cmd]
    f(parsed, args)


@command
def cmd_quit(parsed, _args):
    parameters = {}
    host = parsed.host
    send_cmd(host, 'quit', parameters)


@command
def cmd_shell(parsed, args):
    host = parsed.host
    ipfsi = IPFSInterface(None)
    hostname = args.pop(0)
    port = DSwarmConstants.port_dswarm

    try:
        peer = resolve_name(host, port, hostname)
    except NoNameFound as e:
        print e
        return

    print('connecting to peer %s' % peer)
    try:
        ipfsi.swarm_connect("/p2p-circuit/ipfs/%s" % peer)
    except CmdException as e:
        print e
    port = random.randint(22000, 23232)

    cmd = ['ipfs', 'p2p', 'stream', 'dial', '--timeout', '60s',
           peer , 'p2p-shell', '/ip4/127.0.0.1/tcp/%d' % port]
    print(" ".join(cmd))
    res = ipfsi._cmd(cmd)
    print(res.stdout)

    cmd = ['ncat', 'localhost', str(port)]
    print(" ".join(cmd))

    p = subprocess.Popen(
                cmd,
                stdout=sys.stdout,
                stderr=sys.stderr,
                stdin=sys.stdin,
                bufsize=0,
                cwd='.')

    try:
        p.wait()

        ret = p.returncode
        print('Daemon exit: %s' % ret)
        if ret:
            raise Exception(ret)
    finally:
        print('Finished')


class NoNameFound(Exception):
    pass


@command
def cmd_ssh(parsed, args):
    host = parsed.host
    ipfsi = IPFSInterface(None)
    spec = args.pop(0)
    if '@' in spec:
        user = spec[:spec.index('@')]
        hostname = spec[spec.index('@') + 1:]
    else:
        user = getpass.getuser()
        hostname = spec

    port = DSwarmConstants.port_dswarm
    try:
        peer = resolve_name(host, port, hostname)
    except NoNameFound:
        return

    print('Connecting to %r at %r' % (user, hostname))

    print('connecting to peer %s' % peer)
    try:
        ipfsi.swarm_connect("/p2p-circuit/ipfs/%s" % peer)
    except CmdException as e:
        print e
    port = random.randint(22000, 23232)

    cmd = ['ipfs', 'p2p', 'stream', 'dial', '--timeout', '60s',
           peer , 'p2p-ssh', '/ip4/127.0.0.1/tcp/%d' % port]
    print(" ".join(cmd))
    res = ipfsi._cmd(cmd)
    print(res.stdout)

    cmd = ['ssh', '-p', str(port), '-o', 'StrictHostKeyChecking=no',
           '%s@localhost' % user]
    print(" ".join(cmd))

    p = subprocess.Popen(
                cmd,
                stdout=sys.stdout,
                stderr=sys.stderr,
                stdin=sys.stdin,
                bufsize=0,
                cwd='.')

    try:
        p.wait()

        ret = p.returncode
        print('Daemon exit: %s' % ret)
        if ret:
            raise Exception(ret)
    finally:
        print('Finished')


def resolve_name(host, port, hostname):
    what = ["/pri/*/info/hostname"]
    dc = get_snapshot(host, port, what)
    data = dc.summary_dict()
    hostname2peerid = {}
    for peer, values in data['pri'].items():
        _hostname = list(values['info']['hostname'])[0]
        hostname2peerid[_hostname] = peer

    if not hostname in hostname2peerid:
        msg = ('No host %r found in %s' % (hostname, hostname2peerid))
        raise NoNameFound(msg)

    return hostname2peerid[hostname]


def send_cmd(host, name, parameters):
    port = DSwarmConstants.port_dswarm
    albc = AsyncLineBasedConnection(host, port)
    maddr_from = '/cli'

    inbound = albc.get_q_inbound()
    outbound = albc.get_q_outbound()

    msg = create_command_message(name, parameters, validity=now_until(105))

    e = Envelope(maddr_from=maddr_from,
                 maddr_to='/dswarm/*/brain',
                 contents=msg)

    outbound.put(e)

    reply = inbound.get()
    print reply


def create_safe_index(ipfsi, dc, find_provs, provs_timeout):
    ''' Creates a webpage showing the safe data uploaded '''
    data = dc.summary_dict()

    print(yaml.dump(data))

    s = "<html><head></head><body>"

    verified = []

    data_files = data.get('files', set())
    data_safe = data.get('safe', set())
    data_verified = data.get('verified', set())

    all_mh = set(data_files) | set(data_safe) | set(data_verified)

    for mh in all_mh:
#        s += '\n<a href="/ipfs/%s">%s</a>' % (v, v)
        try:
            more_info = find_more_information(ipfsi, mh, find_provs=find_provs,
                                              provs_timeout=provs_timeout)
            if find_provs:
                print('%15s provided by %s' % (more_info.filename, more_info.providers_payload))
            sys.stderr.write(',')
        except Exception as e:
            print(e)
        else:
            verified.append(more_info)

#            if len(verified) > 10:
#                break
    verified = sorted(verified, key=lambda mi: mi.ctime)

    s += '''
        <style>
        .mh { font-family: monospace; }
        thead { font-weight: bold; }
        td { padding-left: 1em; }
        </style>

        <table>
        <thead><tr><td>Filename</td><td>Size</td><td>Upload by</td><td>node</td>
        <td></td>
        <td>safe</td>
        <td>verified</td>

        <td>ipfs_container</td>
        <td>ipfs_payload</td>
        <td>providers</td>

        </tr></thead>
        <tbody>
    '''
    for more_info in verified:
        d = more_info._asdict()
        d['is_safe'] = 'safe' if more_info.ipfs in data.get('safe', []) else ''
        d['is_verified'] = 'verified' if more_info.ipfs in data.get('verified', []) else ''
        d['date'] = more_info.ctime.strftime('%Y-%m-%d %H:%M')

        def shorten(mh):
            return '<a class="mh" href="/ipfs/%s">%s</a>' % (mh, mh[:4] + '...' + mh[-4:])

        def shorten_node(mh):
            return '<a class="mh" href="/ipns/%s">%s</a>' % (mh, mh[:4] + '...' + mh[-4:])

        d['upload_node_short'] = shorten_node(more_info.upload_node)
        d['ipfs_short'] = shorten(d['ipfs'])
        d['ipfs_payload_short'] = shorten(d['ipfs_payload'])

        d['providers'] = " ".join(map(shorten_node, more_info.providers_info))
        si = '''\n<tr><td><a href="/ipfs/{ipfs_payload}">{filename}</td><td>{size}</td>
        <td>{date}</td>
             <td></td><td> {upload_node_short}</td>
             <td>{is_safe}</td>
             <td>{is_verified}</td>
              <td>{ipfs_short}</td>
              <td>{ipfs_payload_short}</td>
                <td>{providers}</td>
              </tr> '''

        s += si.format(**d)
#        ipfs='QmTJ6sFnB2Pxe1SG7hkd84gkv1YcaEai2tP86mbJKAdBdz', ipfs_payload='QmZYND3nJUW7KAmFMKNjHRMPmtL3FZtqSXW9qNRNcownoG', ipfs_info='QmbWEnQoAL8hPsk2GftZAYC4kTjK7HFYp6eM4D7ULyKA5r', filename='stasera.txt', upload_host='dorothy-7.local', upload_node='QmQDCfGCaYk7Uqc27k6gfgYD13pjny6MZSFQDk8Ra651Jo', upload_user='andrea', ctime=datetime.datetime(2018, 2, 7, 20, 49, 41), size=26, providers_payload=[], providers_info=[])

    s += '</tbody></table>'
    s += '</body>'
    s += '</html>'
    return s


if __name__ == '__main__':
    duckietown_swarm_cli_main()
