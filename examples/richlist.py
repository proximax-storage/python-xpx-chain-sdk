#!/usr/bin/python

from xpxchain import models
from xpxchain import client

import asyncio
import sys
import getopt
import datetime

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


async def check(endpoint, network_type=None):
    async with client.AsyncBlockchainHTTP(endpoint, network_type=network_type) as http:
        height = await http.get_blockchain_height()
        score = await http.get_blockchain_score()

        return endpoint, height, score.score


async def main():

    results = await asyncio.gather(*(check(ep, NETWORK_TYPE) for ep in ENDPOINTS))
    results.sort(key=lambda x: x[2], reverse=True)

    with client.MosaicHTTP(results[0][0], network_type=NETWORK_TYPE) as http:
        accounts = http.get_mosaic_richlist('402B2F579FAEBC59', params={'pageSize':str(1000)})

    print(f"Blockchain height: {results[0][1]}")    
    print(f"        Timestamp: {datetime.datetime.now(datetime.timezone.utc).strftime('%b %d %Y %H:%M:%S %Z')}")
    print(f"           Source: {results[0][0]}")
    print()

    top10 = 0
    top100 = 0
    top1000 = 0
    supply = 9000000000
    divisibility = 1000000
    i = 1

    for account in accounts:
        if (i <= 10):
            top10 += account.amount
        if (i <= 100):
            top100 += account.amount
        if (i <= 1000):
            top1000 += account.amount
        
        i += 1
    
    print(f'Top 10:   {int(top10 / divisibility):13,} XPX {top10 / supply / divisibility * 100:6.2f}%')
    print(f'Top 100:  {int(top100 / divisibility):13,} XPX {top100 / supply / divisibility * 100:6.2f}%')
    print(f'Top 1000: {int(top1000 / divisibility):13,} XPX {top1000 / supply / divisibility * 100:6.2f}%')
    print()

    i = 1
    for account in accounts:
        print(f'{i:4}. {account.address.pretty()} {int(account.amount / divisibility):13,} {account.amount / supply / divisibility * 100:5.2f}%')
        i += 1
    

if (__name__ == '__main__'):
    asyncio.run(main())
