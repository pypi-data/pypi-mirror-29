# Inter-Planetary Swarm of Duckiebots (IPSD)

The Inter-Planetary Swarm of Duckiebots (IPSD) is a system that makes
the Duckiebots

The system provides:

- Duckiebot Discovery service, both at the LAN level, as well as over WAN.
- Collective log sharing and upload.
- Collection of Duckiebots diagnostics and usage statistics.
- Coordinated software update.


## Design goals

- The same system provides both local and global services.
- The same system is used for in-world needs (Duckiebot discovering each other) as well as out-world needs (Duckietown diagnostics).
- The Duckiebots will experience intermittent internet connection. The networks might be
  interrupted and badly configured.


## Current design

A client, `duckietown_swarm` runs on every Duckiebot as well as Duckietown servers.

[IPFS][ipfs] is used as the backend for file sharing. IPFS keys are used for peer identification and cryptographic signatures.

Clients communicate with each other with a number of methods:

  * UDP broadcasts on the local network;
  * IPFS pubsub, an experimental feature of IPFS.
  * An IRC server.

The clients interaction happens through the creation of distributed sets.

Each client maintains a set of "buckets". A bucket contains a set of records.
Each record has a validity period and a set of associated signatures attached to it.
For example, there is a bucket called "files" that contains IPFS multihashes
of files that are declared to be logs.

The state is updated in a distributed way using gossip protocols.
When a client receives a message in one channel, it broadcastes it to the other channels. So eventually, all information reaches everybody else (unless it becomes obsolete in the process).
Nodes also create summary checkpoints every few minutes, that are used by new nodes
to quickly catch up with others.

[Example of message streams generated](http://gateway.ipfs.io/ipfs/QmWtxzez1pGGDREBuQxjc824TojFQ434v8VxMKdvBpGkFx/machines.txt)

[Example of state summary](http://gateway.ipfs.io/ipfs/QmWtxzez1pGGDREBuQxjc824TojFQ434v8VxMKdvBpGkFx/humans.txt)




[ipfs]: http://ipfs.io

## Current functionality



## Installation of IPFS

Install [IPFS](https://ipfs.io/docs/install/).

Commands:

    $ wget https://dist.ipfs.io/go-ipfs/v0.4.13/gco-ipfs_v0.4.13_linux-amd64.tar.gz
    $ tar xvzf gco-ipfs_v0.4.13_linux-amd64.tar.gz
    $ cd go-ipfs
    $ sudo ./install.sh

Initialize the IPFS repo:

    $ ipfs init

## Install this package

Install this package by using:

    $ pip install --user -U duckietown_swarm

## Run

In one terminal, start IPFS by using:

    $ ipfs daemon --enable-pubsub-experiment

In another terminal, run using:

    $ dt-swarm

Now put any (log) file in the directory `~/shared-logs`.

These files will be shared with the worldwide swarm.
