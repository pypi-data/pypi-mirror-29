Types of peer

* Duckiebot running
* Duckiebot charging
* Edge server
* Cloud storage
* Laptop
* Simulation server


What changes

IPFS:
* off
* on
   - swarm.key: bool
   - pubsub: bool
   - dhtclient: bool
   - relay: bool

IRC: which server?
UDP: which interface?

Behavior:
when to read summaries
when to create summaries
whether to reply to requests



Buckets:

    /files
    /verified
    /safe
    /discard


### Proposer = `directory_watcher`

The proposer looks for new files in its input directory DIR.

Creates an archive, add to IPFS, get archive hash Q.

If Q is already in /verified, /safe, or /discard: return

Publishes the archive in `/files`.

(optional) Remove the file from DIR


### Verifier

The verifier looks for new entries in `/files`.

If Q is already in `/verified`, `/safe,` or `/discard`, return.

Otherwise it performs a test.

If the test passes, the file is put in `/verified`.

If the test does not pass, Q is put in `/discard`.

Q is removed from `/files`


### Pinner

The pinner looks for new files in `/verified`.

If Q is `/discard` or `/safe`, return.

After pinned, put it in `/pri/~/pinned`

Periodically, look for pinned files, and if they are in `/discard` or `/safe` (with N votes), unpin them.


### Saver

The saver is the one that takes the files and puts them on the disk in directory OUT.

Look for new files in `/verified`.

If they are in `OUT/q`, then ignore


After pinned, put it in `/safe`.


At the beginning:

look for directories in OUT/q; for each one, put `q`.
