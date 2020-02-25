from xpxchain import models
from xpxchain import client
import os
import requests

gen_hash = None
mosaic_id = None
divisibility = None
tester = None
nemesis = None

if (not tester):

    ENDPOINT = os.environ.get('ENDPOINT', '//localhost:3000')
    FAUCET = os.environ.get('FAUCET', '')
    PRIVATE_KEY = os.environ.get('PRIVATE_KEY', '')

    print()
    print(f"Endpoint: '{ENDPOINT}'")
    if (FAUCET):
        print(f"  Faucet: '{FAUCET}'")

    if (not ENDPOINT):
        raise Exception('No endpoint provided.')

    if ((not FAUCET) and (not PRIVATE_KEY)):
        raise Exception('Neither of faucet or private key were provided.')

    # Get network type
    with client.NodeHTTP(ENDPOINT) as http:
        node_info = http.get_node_info()
        network_type = node_info.network_identifier

    # Get generation hash and main mosaic
    with client.BlockchainHTTP(ENDPOINT) as http:
        block = http.get_block_by_height(1)
        gen_hash = block.generation_hash
        nemesis = block.signer

        receipts = http.get_block_receipts(2)
        for statement in receipts.transaction_statements:
            for receipt in statement.receipts:
                if (receipt.type == models.ReceiptType.VALIDATE_FEE):
                    mosaic_id = receipt.mosaic.id
                    break

    # Checking the divisibility
    with client.MosaicHTTP(ENDPOINT) as http:
        mosaic_info = http.get_mosaic(mosaic_id)
        divisibility = 10 ** mosaic_info.properties.divisibility

    # Prepare the testing account
    if (PRIVATE_KEY):
        account = models.Account.create_from_private_key(PRIVATE_KEY, network_type)
    else:
        account = models.Account.generate_new_account(network_type, entropy=lambda x: os.urandom(32))
        reply = requests.get(f"{FAUCET}{account.address.address}").json()
        if (reply != 'XPX sent!'):
            raise Exception(f"Error getting funds from faucet: {reply}")

    print()
    print(f"Testing account")
    print(f"---------------")
    print(f"    Address: {account.address.address}")
    print(f"Private key: {account.private_key}")
    print(f" Public key: {account.public_key}")
    print()

    tester = account
