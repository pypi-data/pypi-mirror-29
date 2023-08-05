# Duckietown world-wide swarm client

This is an experimental swarm client t


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
  