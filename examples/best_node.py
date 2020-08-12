#!/usr/bin/python

from xpxchain import models
from xpxchain import client

import asyncio
import sys
import getopt

ENDPOINTS = [
    'arcturus.xpxsirius.io:3000',
    'aldebaran.xpxsirius.io:3000',
    'betelgeuse.xpxsirius.io:3000',
    'westerlund.xpxsirius.io:3000',
    'canismajor.xpxsirius.io:3000',
    'delphinus.xpxsirius.io:3000',
    'eridanus.xpxsirius.io:3000',
    'lyrasithara.xpxsirius.io:3000',
]

NETWORK_TYPE = models.NetworkType.MAIN_NET


def usage():
    print(f"Usage: {sys.argv[0]} [OPTION]")
    print("Print node's address:port with the highest blockchain score")
    print()
    print("OPTION")
    print()
    print("  -v          Show scores of all nodes (on stderr)")
    print("  -h, --help  Display this help and exit")

async def check(endpoint, network_type=None):
    async with client.AsyncBlockchainHTTP(endpoint, network_type=network_type) as http:
        height = await http.get_blockchain_height()
        score = await http.get_blockchain_score()

        return endpoint, height, score.score


async def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv", ["help"])
    except getopt.GetoptError as err:
        print(str(err), file=sys.stderr)
        usage()
        sys.exit(2)

    verbose = False

    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()

    results = await asyncio.gather(*(check(ep, NETWORK_TYPE) for ep in ENDPOINTS))
    results.sort(key=lambda x: x[2], reverse=True)

    if (verbose):
        print('{:30} {} {}'.format('Node', 'Height', 'Score'), file=sys.stderr)

        for ep in results:
            print(f'{ep[0]:30} {ep[1]} {ep[2]}', file=sys.stderr)

        print(file=sys.stderr)

    print(results[0][0])
       
if (__name__ == '__main__'):
    asyncio.run(main())
