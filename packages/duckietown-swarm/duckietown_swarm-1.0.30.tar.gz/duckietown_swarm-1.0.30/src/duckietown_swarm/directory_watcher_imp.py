from collections import OrderedDict
from datetime import datetime
from duckietown_swarm.dcache_wire import create_propose_message
from duckietown_swarm.ipfs_utils import add_ipfs_dir, IPFSInterface
from duckietown_swarm.utils import yaml_dump_omaps
import getpass
import os
import shutil
import socket
from tempfile import mkdtemp
import time

from conf_tools.utils.locate_files_imp import locate_files
from system_cmd.structures import CmdException


def directory_watcher(mi, watch_dir):
    seen = {}
    tmpdir = mkdtemp(prefix='swarm')

    def look_for_files(d, pattern='*'):
        if not os.path.exists(d):
            msg = 'Logs directory does not exist: %s' % d
            raise ValueError(msg)

        filenames = locate_files(d, pattern)
        for f in filenames:
            if 'cache' in f:
                continue

            if not f in seen:

                try:
                    hashed = _add_file(f)
                except Exception as e:
                    print('error adding %s:\n%s' % (f, e))
                    continue

                print('found local %s %s' % (hashed, f))

                DAYS = 24 * 60 * 60
                interval = [time.time(), time.time() + 7 * DAYS]
                msg = create_propose_message('files', hashed, interval)
                mi.send_to_brain('', msg, sign=True)

    def _add_file(filename):
        d = setup_dir_for_file(tmpdir, filename)
        try:
            hashed = add_ipfs_dir(d)
            seen[filename] = hashed
            return hashed
        except CmdException as e:
            raise Exception(str(e))

    while True:
        look_for_files(watch_dir)
        time.sleep(15)


def setup_dir_for_file(tmpdir, filename):
    b0 = os.path.basename(filename)
    b = b0.replace('.', '_')
    d = os.path.join(tmpdir, b)
    if not os.path.exists(d):
        os.mkdir(d)
    dest = os.path.join(d, b0)

    if not os.path.exists(dest):
        try:
            os.link(filename, dest)
        except OSError:
            shutil.copy(filename, dest)

    r = OrderedDict()
    r['filename'] = b0
    mtime = os.path.getmtime(filename)
    r['ctime'] = datetime.fromtimestamp(mtime)
    r['upload_host'] = socket.gethostname()
    # no - otherwise it changes every time
    # r['upload_date'] = datetime.now()
    ipfsi = IPFSInterface()
    r['upload_node'] = ipfsi.ipfs_id()
    r['upload_user'] = getpass.getuser()
    info = os.path.join(d, 'upload_info1.yaml')
    with open(info, 'w') as f:
        y = yaml_dump_omaps(r)
        f.write(y)
    return d
