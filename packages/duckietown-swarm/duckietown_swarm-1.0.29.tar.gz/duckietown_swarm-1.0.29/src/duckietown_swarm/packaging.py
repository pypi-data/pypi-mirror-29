#! /usr/bin/env python

from collections import  namedtuple

from system_cmd import CmdException

from .ipfs_utils import IPFSInterface
from .utils import memoize_simple, yaml_load_omaps


class UnexpectedFormat(Exception):
    pass


MoreInfo = namedtuple('MoreInfo', 'ipfs ipfs_payload ipfs_info filename upload_host upload_node'
                      ' upload_user ctime size providers_payload providers_info')

INFO = 'upload_info1.yaml'


@memoize_simple
def find_more_information(ipfsi, h, find_provs=False):
    contents = ipfsi.ls(h, timeout="3s")
    timeout = "1h"
    if not INFO in contents:
        raise UnexpectedFormat(str(contents))

    try:
        info_data = ipfsi.get(h + '/' + INFO, timeout=timeout)
    except CmdException as e:
        if 'no link named' in e.res.stderr:
            raise UnexpectedFormat(e.res.stderr)
        raise

    try:
        info = yaml_load_omaps(info_data)
    except:
        raise UnexpectedFormat()

    try:
        filename = info['filename']
        ctime = info['ctime']
        upload_host = info['upload_host']
        upload_node = info['upload_node']
        upload_user = info['upload_user']
    except KeyError as e:
        msg = 'Invalid format: %s' % e
        raise UnexpectedFormat(msg)

    try:
        ipfs_info = contents[INFO].hash
        ipfs_payload = contents[filename].hash
        size = contents[filename].size
    except KeyError as e:
        raise UnexpectedFormat(str(e))
    ipfsi = IPFSInterface()

    if find_provs:
        providers_info = ipfsi.dht_findprovs(ipfs_info)
        providers_payload = ipfsi.dht_findprovs(ipfs_payload)
    else:
        providers_info = []
        providers_payload = []

    return MoreInfo(ipfs=h,
                    ipfs_payload=ipfs_payload,
                    ipfs_info=ipfs_info,
                    filename=filename,
                    ctime=ctime,
                    size=size,
                    providers_info=providers_info,
                    providers_payload=providers_payload,
                    upload_host=upload_host,
                    upload_node=upload_node,
                    upload_user=upload_user)

