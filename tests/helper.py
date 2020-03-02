
from xpxchain import client
from xpxchain import models
from xpxchain import errors
from tests import config
import asyncio


async def announce(tx):
    async with client.Listener(f'{config.ENDPOINT}/ws', network_type=config.network_type) as listener:
        address = models.PublicAccount.create_from_public_key(tx.signer, config.network_type).address

        await listener.confirmed(address)
        await listener.status(address)

        async with client.AsyncTransactionHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            await http.announce(tx)

        async for m in listener:
            if ((m.channel_name == 'status') and (m.message.hash == tx.hash.upper())):
                raise errors.TransactionError(m.message)
            elif ((m.channel_name == 'confirmedAdded') and (m.message.transaction_info.hash == tx.hash.upper())):
                return m.message


async def announce_partial(tx):
    async with client.Listener(f'{config.ENDPOINT}/ws', network_type=config.network_type) as listener:
        address = models.PublicAccount.create_from_public_key(tx.signer, config.network_type).address

        await listener.aggregate_bonded_added(address)
        await listener.status(address)

        async with client.AsyncTransactionHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            await http.announce_partial(tx)

        async for m in listener:
            if ((m.channel_name == 'status') and (m.message.hash == tx.hash.upper())):
                raise errors.TransactionError(m.message)
            elif ((m.channel_name == 'partialAdded') and (m.message.transaction_info.hash == tx.hash.upper())):
                return m.message


async def announce_cosignature(tx):
    async with client.Listener(f'{config.ENDPOINT}/ws', network_type=config.network_type) as listener:
        address = models.PublicAccount.create_from_public_key(tx.signer, config.network_type).address

        await listener.confirmed(address)
        await listener.status(address)

        async with client.AsyncTransactionHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            await http.announce_cosignature(tx)

        async for m in listener:
            if ((m.channel_name == 'status') and (m.message.hash == tx.hash.upper())):
                raise errors.TransactionError(m.message)
            elif ((m.channel_name == 'confirmedAdded') and (m.message.transaction_info.hash == tx.parent_hash.upper())):
                return m.message


async def send_funds(sender, recipient, amount, quiet=True):
    tx = models.TransferTransaction.create(
        deadline=models.Deadline.create(),
        recipient=recipient.address,
        mosaics=[models.Mosaic(config.mosaic_id, amount)],
        network_type=config.network_type,
    )

    signed_tx = tx.sign_with(sender, config.gen_hash)

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
            try:
                tx = task.result()
            except errors.TransactionError as e:
                print(f"Error transaction {e.hash}: {e}")

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
    namespace_name = namespace.split(".")

    tx = models.RegisterNamespaceTransaction.create_root_namespace(
        deadline=models.Deadline.create(),
        network_type=config.network_type,
        namespace_name=namespace_name[0],
        duration=60
    )

    signed_tx = tx.sign_with(account, config.gen_hash)

    tx = await announce(signed_tx)
    n1 = models.NamespaceName(tx.namespace_id, tx.namespace_name)

    if (len(namespace_name) > 1):
        # Create sub namespace
        tx = models.RegisterNamespaceTransaction.create_sub_namespace(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            namespace_name=namespace_name[1],
            parent_namespace=namespace_name[0]
        )

        signed_tx = tx.sign_with(account, config.gen_hash)

        tx = await announce(signed_tx)
        n2 = models.NamespaceName(tx.namespace_id, tx.namespace_name, n1.namespace_id)

        return n1, n2

    return n1


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

    signed_tx = tx.sign_with(account, config.gen_hash)

    tx = await announce(signed_tx)

    return mosaic_id
