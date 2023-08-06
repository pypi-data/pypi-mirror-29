Protocol
--------

There are two primitives:


    propose(dcaddress, string, [t0, t1])
    dismiss(dcaddress, string, [t0, t1])


where:

    dcaddress = [bucket1, bucket2, ...]
    validity = [from, to] or [null, to] or [from, null]

The semantics of

    propose([bucket1, bucke2], string, [t0, t1])
    state['bucket1']['bucket2'].add(string)

    so that it is true that

        string in state['bucket1']['bucket2'] for t0 < t < t1

This is true, unless a "dismiss" or "replace" command is given.

Summaries
---------

There is a message:

    ask-summary
    summary(ipfs)

where ipfs is the multihash of a list of YAML messages to be interpreted.


Signatures
-------

    {mtype:'signed', what='QmContent', peerid='QmPublicKeyHash', signature='...'}

Envelope
-------

There is some meta-information associated:

    signatures: a list of signatures



Signature
---------

A signature has:

    ID: (hash of public key)
    Signature: bytes
    Validity: [t0, t1]

Routing
-------

channels: channels in which this was circulated, or None



Python API querying
========

In Python, a dcaddress is represented by a tuple of strings.

    dcaddress = ('my', 'prefix')

A client is able to query as follows:

    h = storage.dca(dcaddress)

List the contents

    ss = storage.list(dcprefix)

    for s in sl:
        s.data        # data
        s.validity    # t0, inf
        s.channels    # channels this was received from
        s.signatures  # collected signatures

Distributed authenticated sets

    peer [PeerID]  The host HASH is a Duckiebot

        propose: peer
        dismiss: admin

    trusted [PeerID]

        propose: admin
        dismiss: admin

    admin [PeerID]

        propose: mama
        dismiss: mama

    summary [Hash]

        propose: anybody
        dismiss: trusted

    networks

        propose: admin
        dismiss: admin

        examples:

            /irc/address
            /udp/address

    files / HASH

        propose: anybody
        dismiss: trusted

    uploads / HASH

        propose: trusted
        dismiss: trusted

    propose('files', ipfs)
    dismiss('files', ipfs)

    propose('valid', ipfs)
    dismiss('valid', ipfs)
    replace('valid', ifps1, ipfs2)

    propose('summary', H('irc1'))

    propose('network', H('irc1'))
    propose('network', H('irc1'))

    propose(ipfs_host, 'role')



Addresses

/duckieswarm/<ID>/verifier
/duckieswarm/<ID>/brain

/dns4/frankfurt.co-design.science/tcp/6667/irc/#duckiebots
/dns4/frankfurt.co-design.science/tcp/6667/irc/NickName
/ip4/10.0.0.0/udp/6060/duckieswarmcall
