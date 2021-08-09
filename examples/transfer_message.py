from xpxchain import models
from xpxchain import client
from xpxchain import errors

import requests
import asyncio
import sys

nodes = [
    "bctestnet1.brimstone.xpxsirius.io:3000",
    "bctestnet2.brimstone.xpxsirius.io:3000",
    "bctestnet3.brimstone.xpxsirius.io:3000",
]

# Choosing one of the endpoints
endpoint = nodes[1]    

async def announce(tx):
    address = models.PublicAccount.create_from_public_key(tx.signer, tx.network_type).address

    # Create listener and subscribe to confirmed / unconfirmed transactions and error status
    # Subscription should occur prior to announcing the transaction
    async with client.Listener(f'{endpoint}/ws') as listener:
        await listener.confirmed(address)
        await listener.status(address)
        await listener.unconfirmed_added(address)

        # Announce the transaction to the network
        print(f"Sending a message to {bob.address.address}\n")
        with client.TransactionHTTP(endpoint) as http:
            http.announce(tx)

        # Listener gets all messages regarding the address given but we care only
        # about our transaciton
        async for m in listener:
            if ((m.channel_name == 'status') and (m.message.hash == tx.hash.upper())):
                # An error occured and the transaction was rejected by the node
                raise errors.TransactionError(m.message)
            elif ((m.channel_name == 'unconfirmedAdded') and (m.message.transaction_info.hash == tx.hash.upper())):
                # The transaction was accepted by the node and is about to be included in a block
                print(f"Unconfirmed transaction {m.message.transaction_info.hash}")
                print("Waiting for confirmation\n")
            elif ((m.channel_name == 'confirmedAdded') and (m.message.transaction_info.hash == tx.hash.upper())):
                # The transaction was included in a block
                return m.message


def print_account_info(account): 
    print(f"    Address: {account.address.address}")
    #print(f"Private key: {account.private_key}")
    print(f" Public key: {account.public_key}")


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


alice = models.Account.create_from_private_key("6b2a97945d0f318114215ee80c012a5ea2ad39a3cd472a9ff2caf7488c4c2ede", network_type)

# Ask for test XPX from the faucet
try:
	print(f"Requesting test XPX for {alice.address.address}")
	reply = requests.get(f"https://bctestnetfaucet.xpxsirius.io/api/faucet/GetXpx/{alice.address.address}").json()
	print(f"{reply}\n")
	
except:
	print("not available")

# Generate Bob's account
bob = models.PublicAccount.create_from_public_key("65509a4793d1cc5bbeceaa9f362cef4ae2d4382e8e40a35ef6444d19a22607e9", network_type)

# Print their account credentials
print_account_info(alice)
print_account_info(bob)

msg = models.PlainMessage(b'Hello world')

# Create message and transfer to bob

tx = models.TransferTransaction.create(
    deadline=models.Deadline.create(),
    recipient=bob.address,
	message=msg,
    network_type=network_type,
)

# Sign the transaction with Alice's account
signed_tx = tx.sign_with(
    account=alice, 
    gen_hash=block_info.generation_hash
)

# We run announce() as an asynchronous function because it uses Listener that comes
# only in async implementation
result = asyncio.run(announce(signed_tx))

print("Message has been successfully sent")
