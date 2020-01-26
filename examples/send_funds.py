#!/usr/bin/python

from nem2 import models
from nem2 import client
from nem2 import util

import requests
import asyncio

nodes = [
    "bctestnet1.brimstone.xpxsirius.io:3000",
    "bctestnet2.brimstone.xpxsirius.io:3000",
    "bctestnet3.brimstone.xpxsirius.io:3000",
]

# Choosing one of the endpoints
endpoint = nodes[0]
    

async def listen(account):
    # Create listener and subscribe to confirmed / unconfirmed transactions and error status
    async with client.Listener(f'{endpoint}/ws') as listener:
        await listener.confirmed(account.address)
        await listener.status(account.address)
        await listener.unconfirmed_added(account.address)

        async for m in listener:
            if (m.channel_name == 'status'):
                # An error occured and the transaction was rejected by the node
                raise Exception(m.message.status)
            elif (m.channel_name == 'unconfirmedAdded'):
                # The transaction was accepted by the node and is about to be included in a block
                print(f"Unconfirmed transaction {m.message.transaction_info.hash}")
                print("Waiting for confirmation\n")
            elif (m.channel_name == 'confirmedAdded'):
                # The transaction was included in a block
                return m.message


def print_account_info(account): 
    print(f"    Address: {account.address.address}")
    print(f"Private key: {account.private_key}")
    print(f" Public key: {account.public_key}")
    print()


def print_account_mosaics(account):
    print(f"Address: {account.address.address}")

    # Get the account info
    with client.AccountHTTP(endpoint) as http:
        account_info = http.get_account_info(account.address)
    
    # Get names and divisibility of all mosaics on the account
    for mosaic in account_info.mosaics:
        with client.MosaicHTTP(endpoint) as http:
            mosaic_info = http.get_mosaic(mosaic.id)
            mosaic_names = http.get_mosaic_names([mosaic.id])
    
        divisibility = 10**mosaic_info.properties.divisibility
        name = mosaic_names[0].names[0]

        print(f" Mosaic: {name} {mosaic.amount / divisibility}")
    print()

# Get network type
with client.NodeHTTP(endpoint) as http:
    node_info = http.get_node_info()
    network_type = node_info.network_identifier

# Get generation hash of this blockchain
with client.BlockchainHTTP(endpoint) as http:
    block_info = http.get_block_by_height(1)

# Get the XPX mosaic by its namespace alias. Mosaics don't have names, you can only asign an alias to them.
# Namespace will give us the mosaic id.
with client.NamespaceHTTP(endpoint) as http:
    namespace_info = http.get_namespace(models.NamespaceId('prx.xpx'))

# Get mosaic info by its id.
with client.MosaicHTTP(endpoint) as http:
    xpx = http.get_mosaic(namespace_info.alias.value)

# Generate two random accounts: Alice and Bob
alice = models.Account.generate_new_account(network_type)
bob = models.Account.generate_new_account(network_type)

# Print their addresses, private and public keys
print_account_info(alice)
print_account_info(bob)

# Ask for test XPX from the faucet
print(f"Requesting test XPX for {alice.address.address}")
reply = requests.get(f"https://bctestnetfaucet.xpxsirius.io/api/faucet/GetXpx/{alice.address.address}").json()
print(f"{reply}\n")

amount = 1

# Create transfer transactions of 1 XPX to Bob
tx = models.TransferTransaction.create(
    deadline=models.Deadline.create(),
    recipient=bob.address,
    mosaics=[models.Mosaic(xpx.mosaic_id, amount * 10**xpx.properties.divisibility)],
    network_type=network_type,
)

# Sign the transaction with Alice's account
signed_tx = tx.sign_with(
    account=alice, 
    gen_hash=block_info.generation_hash, 
    fee_strategy=util.FeeCalculationStrategy.MEDIUM
)

# Announce the transaction to the blockchain
print(f"Sending {amount} XPX to {bob.address.address}\n")
with client.TransactionHTTP(endpoint) as http:
    http.announce(signed_tx)

# Create event loop for asynchronous listener
loop = asyncio.get_event_loop()
result = loop.run_until_complete(listen(alice))
print(f"Confirmed transaction {result.transaction_info.hash}\n")

# Print resulting account balances
print_account_mosaics(alice)
print_account_mosaics(bob)
