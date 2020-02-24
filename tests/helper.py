
from xpxchain import client
from xpxchain import models
from xpxchain import util
from tests import config
import asyncio


async def announce(tx):
    async with client.Listener(f'{config.ENDPOINT}/ws') as listener:
        address = models.PublicAccount.create_from_public_key(tx.signer, config.network_type).address

        await listener.confirmed(address)
        await listener.status(address)

        async with client.AsyncTransactionHTTP(config.ENDPOINT) as http:
            await http.announce(tx)

        async for m in listener:
            if ((m.channel_name == 'status') and (m.message.hash == tx.hash.upper())):
                raise Exception(m.message)
            elif ((m.channel_name == 'confirmedAdded') and (m.message.transaction_info.hash == tx.hash.upper())):
                return m.message


async def announce_partial(tx):
    async with client.Listener(f'{config.ENDPOINT}/ws') as listener:
        address = models.PublicAccount.create_from_public_key(tx.signer, config.network_type).address

        await listener.aggregate_bonded_added(address)
        await listener.status(address)

        async with client.AsyncTransactionHTTP(config.ENDPOINT) as http:
            await http.announce_partial(tx)

        async for m in listener:
            if ((m.channel_name == 'status') and (m.message.hash == tx.hash.upper())):
                raise Exception(m.message)
            elif ((m.channel_name == 'partialAdded') and (m.message.transaction_info.hash == tx.hash.upper())):
                return m.message


async def announce_cosignature(tx):
    async with client.Listener(f'{config.ENDPOINT}/ws') as listener:
        address = models.PublicAccount.create_from_public_key(tx.signer, config.network_type).address

        await listener.confirmed(address)
        await listener.status(address)

        async with client.AsyncTransactionHTTP(config.ENDPOINT) as http:
            await http.announce_cosignature(tx)

        async for m in listener:
            if ((m.channel_name == 'status') and (m.message.hash == tx.hash.upper())):
                raise Exception(m.message)
            elif ((m.channel_name == 'confirmedAdded') and (m.message.transaction_info.hash == tx.parent_hash.upper())):
                return m.message


async def send_funds(sender, recipient, amount, quiet=False):
    tx = models.TransferTransaction.create(
        deadline=models.Deadline.create(),
        recipient=recipient.address,
        mosaics=[models.Mosaic(config.mosaic_id, amount)],
        network_type=config.network_type,
    )

    signed_tx = tx.sign_with(sender, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

    if (not quiet):
        print(f"Sending funds to {recipient.address.address} {signed_tx.hash}")

    return await announce(signed_tx)


async def prepare(plan, max_run=100):
    aws = plan[:max_run]
    plan = plan[max_run:]
    hashes = []

    while (aws):
        done, pending = await asyncio.wait(aws, return_when=asyncio.FIRST_COMPLETED)
        aws = []

        for task in done:
            tx = task.result()
            hashes.append(tx.transaction_info.hash)

        for task in pending:
            aws.append(task)

        planned = len(aws)
        if (planned < max_run):
            diff = max_run - planned
            aws += plan[:diff]
            plan = plan[diff:]

    return hashes


async def create_namespace(account, namespace):
    namespace = namespace.split(".")

    tx = models.RegisterNamespaceTransaction.create_root_namespace(
        deadline=models.Deadline.create(),
        network_type=config.network_type,
        namespace_name=namespace[0],
        duration=60
    )

    signed_tx = tx.sign_with(account, config.gen_hash)

    tx = await announce(signed_tx)

    if (len(namespace) > 1):
        # Create sub namespace
        tx = models.RegisterNamespaceTransaction.create_sub_namespace(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            namespace_name=namespace[1],
            parent_namespace=namespace[0]
        )

        signed_tx = tx.sign_with(account, config.gen_hash)

        tx = await announce(signed_tx)


async def create_mosaic(account, nonce):
    nonce = models.MosaicNonce(nonce)
    mosaic_id = models.MosaicId.create_from_nonce(nonce, account)

    tx = models.MosaicDefinitionTransaction.create(
        deadline=models.Deadline.create(),
        network_type=config.network_type,
        nonce=nonce,
        mosaic_id=mosaic_id,
        mosaic_properties=models.MosaicProperties(0x3, 3),
    )

    signed_tx = tx.sign_with(account, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

    tx = await announce(signed_tx)

    return mosaic_id
