
from Queue import Empty
from duckietown_swarm.brain import DistributedRepoSwarm
from duckietown_swarm.dcache_wire import create_request_message, MsgPong
from duckietown_swarm.ipfs_utils import IPFSInterface
from duckietown_swarm.packaging import find_more_information
from duckietown_swarm.utils import now_until
import getpass
import random
import subprocess
import sys
import time

from contracts import contract
from system_cmd.structures import CmdException
import yaml

from .dcache import Envelope, interpret_message
from .socket_utils import AsyncLineBasedConnection


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


def duckietown_swarm_cli_main():
#    import argparse

#    parser = argparse.ArgumentParser(description='Ping the swarm')
#    parser.add_argument('host', type=str, default='localhost')
#    parser.add_argument('what', default='*', help='what to request')

    args = sys.argv[1:]
    print args
    host = args.pop(0)
    port = 8000
    cmd = args.pop(0)

    if cmd == 'summary':
        if args:
            what = args
        else:
            what = ['*']

        dc = get_snapshot(host, port, what)
        data = dc.summary_dict()

        print(yaml.dump(data))

    elif cmd == 'report':
#    args = parser.parse_args()
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
    elif cmd == 'ssh':

        what = ["/pri/*/info/hostname"]
        dc = get_snapshot(host, port, what)
        data = dc.summary_dict()
        ipfsi = IPFSInterface(None)
        hostname2peerid = {}
        for peer, values in data['pri'].items():
            _hostname = list(values['info']['hostname'])[0]
            hostname2peerid[_hostname] = peer
        print('known: %s' % hostname2peerid)
        spec = args.pop(0)
        if '@' in spec:
            user = spec[:spec.index('@')]
            hostname = spec[spec.index('@') + 1:]
        else:
            user = getpass.getuser()
            hostname = spec

        print('Connecting to %r at %r' % (user, hostname))

        if not hostname in hostname2peerid:
            print('No host %r found in %s' % (hostname, hostname2peerid))
        else:
            peer = hostname2peerid[hostname]

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

    else:
        raise Exception(cmd)


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
