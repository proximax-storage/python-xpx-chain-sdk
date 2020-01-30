#!/usr/bin/python

from xpxchain import client

# Get the current chain height of the Sirius test net
with client.BlockchainHTTP('bctestnet1.brimstone.xpxsirius.io:3000') as http:
    reply = http.get_blockchain_height()

print(reply)
