from nem2 import client
from nem2 import models
from tests import harness
from tests import config
from tests import responses
import datetime
from binascii import unhexlify
import asyncio
from tests import aitertools

@harness.http_test_case({
    'clients': (client.TransactionHTTP, client.AsyncTransactionHTTP),
    'tests': [
        {
            #/transaction/{transactionId}
            'name': 'test_get_transaction',
            'params': [config.Transaction.hash],
            'method': 'get_transaction',
            'validation': [
                lambda x: (isinstance(x, models.Transaction), True),
            ]
        },
        {
            #/transaction/{transactionId}
            'name': 'test_get_transactions',
            'params': [[config.Transaction.hash, '024C08B8767FCA0DCF7B631EC2631D9575FFB84E8E5EFA7C656B18FB1A1F34E8']],
            'method': 'get_transactions',
            'validation': [
                lambda x: (len(x), 2),
                lambda x: (isinstance(x[0], models.Transaction), True),
            ]
        },
        {
            #/transaction/{hash}/status
            'name': 'test_get_transaction_status',
            'params': [config.Transaction.hash],
            'method': 'get_transaction_status',
            'validation': [
                lambda x: (isinstance(x, models.TransactionStatus), True),
            ]
        },
        {
            #/transaction/statuses
            'name': 'test_get_transaction_statuses',
            'params': [[config.Transaction.hash, '024C08B8767FCA0DCF7B631EC2631D9575FFB84E8E5EFA7C656B18FB1A1F34E8']],
            'method': 'get_transaction_statuses',
            'validation': [
                lambda x: (len(x), 2),
                lambda x: (isinstance(x[0], models.TransactionStatus), True),
            ]
        },
    ],
})
class TestTransactionHttp(harness.TestCase):
    async def test_transaction(self):
        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'

        nemesis = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
        self.assertEqual(nemesis.address.address, 'SBGS2IGUED476REYI5ZZGISVSEHAF6YIQZV6YJFQ')

        recipient = models.Address('SAFSPPRI4MBM3R7USYLJHUODAD5ZEK65YUP35NV6')
        mosaic_id = models.MosaicId.create_from_hex('0dc67fbe1cad29e3')
        amount = 1000

        tx = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=recipient,
            mosaics=[models.Mosaic(mosaic_id, amount)],
            network_type=models.NetworkType.MIJIN_TEST,
            max_fee=1
        )

        async def announce():
            signed_tx = tx.sign_with(nemesis, gen_hash)
            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

        async def listen():
            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
                await listener.confirmed(nemesis.address)

                async for m in listener:
                    #TODO: Check for more transactions. It could not always be the first one.
                    #TODO: Implement timeout.
                    tx = m.message
                    self.assertEqual(isinstance(tx, models.TransferTransaction), True)
                    self.assertEqual(tx.recipient, recipient)
                    self.assertEqual(len(tx.mosaics), 1)
                    self.assertEqual(tx.mosaics[0].id, mosaic_id)
                    self.assertEqual(tx.mosaics[0].amount, amount)
                    break

        await asyncio.gather(listen(), announce())

