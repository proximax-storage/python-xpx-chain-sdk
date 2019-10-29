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
#        {
#            #/transaction/{transactionId}
#            'name': 'test_get_transaction',
#            'params': [config.Transaction.hash],
#            'method': 'get_transaction',
#            'validation': [
#                lambda x: (isinstance(x, models.Transaction), True),
#            ]
#        },
#        {
#            #/transaction/{transactionId}
#            'name': 'test_get_transactions',
#            'params': [[config.Transaction.hash, '024C08B8767FCA0DCF7B631EC2631D9575FFB84E8E5EFA7C656B18FB1A1F34E8']],
#            'method': 'get_transactions',
#            'validation': [
#                lambda x: (len(x), 2),
#                lambda x: (isinstance(x[0], models.Transaction), True),
#            ]
#        },
#        {
#            #/transaction/{hash}/status
#            'name': 'test_get_transaction_status',
#            'params': [config.Transaction.hash],
#            'method': 'get_transaction_status',
#            'validation': [
#                lambda x: (isinstance(x, models.TransactionStatus), True),
#            ]
#        },
#        {
#            #/transaction/statuses
#            'name': 'test_get_transaction_statuses',
#            'params': [[config.Transaction.hash, '024C08B8767FCA0DCF7B631EC2631D9575FFB84E8E5EFA7C656B18FB1A1F34E8']],
#            'method': 'get_transaction_statuses',
#            'validation': [
#                lambda x: (len(x), 2),
#                lambda x: (isinstance(x[0], models.TransactionStatus), True),
#            ]
#        },
    ],
})
class TestTransactionHttp(harness.TestCase):
#    async def test_transfer_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        nemesis = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#        self.assertEqual(nemesis.address.address, 'SBGS2IGUED476REYI5ZZGISVSEHAF6YIQZV6YJFQ')
#
#        recipient = models.Address('SAFSPPRI4MBM3R7USYLJHUODAD5ZEK65YUP35NV6')
#        mosaic_id = models.MosaicId.create_from_hex('0dc67fbe1cad29e3')
#        amount = 1000
#
#        tx = models.TransferTransaction.create(
#            deadline=models.Deadline.create(),
#            recipient=recipient,
#            mosaics=[models.Mosaic(mosaic_id, amount)],
#            network_type=models.NetworkType.MIJIN_TEST,
#            max_fee=1
#        )
#
#        signed_tx = tx.sign_with(nemesis, gen_hash)
#
#        async def announce():
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_tx)
#
#        async def listen():
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(nemesis.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.TransferTransaction), True)
#                    self.assertEqual(tx.recipient, recipient)
#                    self.assertEqual(len(tx.mosaics), 1)
#                    self.assertEqual(tx.mosaics[0].id, mosaic_id)
#                    self.assertEqual(tx.mosaics[0].amount, amount)
#                    break
#
#        await asyncio.gather(listen(), announce())
#
#    
#    async def test_message_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        nemesis = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#        self.assertEqual(nemesis.address.address, 'SBGS2IGUED476REYI5ZZGISVSEHAF6YIQZV6YJFQ')
#
#        recipient = models.Address('SAFSPPRI4MBM3R7USYLJHUODAD5ZEK65YUP35NV6')
#        message = models.PlainMessage(b'Hello world')
#
#        tx = models.TransferTransaction.create(
#            deadline=models.Deadline.create(),
#            recipient=recipient,
#            network_type=models.NetworkType.MIJIN_TEST,
#            max_fee=1,
#            message=message
#        )
#
#        signed_tx = tx.sign_with(nemesis, gen_hash)
#
#        async def announce():
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_tx)
#
#        async def listen():
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(nemesis.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.TransferTransaction), True)
#                    self.assertEqual(tx.recipient, recipient)
#                    self.assertEqual(tx.message, message)
#                    break
#
#        await asyncio.gather(listen(), announce())
    
    
#    async def test_account_link_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        nemesis = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#        self.assertEqual(nemesis.address.address, 'SBGS2IGUED476REYI5ZZGISVSEHAF6YIQZV6YJFQ')
#
#        linked_account = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#        print(linked_account.address.address)
#
#        tx = models.AccountLinkTransaction.create(
#            deadline=models.Deadline.create(),
#            remote_account_key=linked_account.public_key,
#            link_action=models.LinkAction.LINK,
#            network_type=models.NetworkType.MIJIN_TEST,
#            max_fee=1            
#        )
#
#        signed_tx = tx.sign_with(nemesis, gen_hash)
#        
#        async def announce():
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_tx)
#
#        async def listen(action):
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(nemesis.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.AccountLinkTransaction), True)
#                    self.assertEqual(tx.remote_account_key, linked_account.public_key.upper())
#                    self.assertEqual(tx.link_action, action)
#                    break
#
#        await asyncio.gather(listen(models.LinkAction.LINK), announce())
#        
#        tx = models.AccountLinkTransaction.create(
#            deadline=models.Deadline.create(),
#            remote_account_key=linked_account.public_key,
#            link_action=models.LinkAction.UNLINK,
#            network_type=models.NetworkType.MIJIN_TEST
#        )
#
#        signed_tx = tx.sign_with(nemesis, gen_hash)
#        
#        await asyncio.gather(listen(models.LinkAction.UNLINK), announce())
    
    
#    async def test_modify_account_property_address_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        account = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#        nemesis = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#
#        print(account.address.address)
#
#        async def announce(nemesis, account, property_type, modification_type):
#            tx = models.ModifyAccountPropertyAddressTransaction.create(
#                deadline=models.Deadline.create(),
#                network_type=models.NetworkType.MIJIN_TEST,
#                max_fee=1,
#                property_type=property_type,
#                modifications=[models.AccountPropertyModification(modification_type, account.address)]
#            )
#            
#            signed_tx = tx.sign_with(nemesis, gen_hash)
#
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_tx)
#
#        async def listen(property_type, modification_type):
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(nemesis.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.ModifyAccountPropertyAddressTransaction), True)
#                    self.assertEqual(len(tx.modifications), 1)
#                    self.assertEqual(tx.property_type, property_type)
#                    self.assertEqual(tx.modifications[0].modification_type, modification_type)
#                    break
#
#        for property_type in [models.PropertyType.ALLOW_ADDRESS, models.PropertyType.BLOCK_ADDRESS]:
#            for modification_type in [models.PropertyModificationType.ADD, models.PropertyModificationType.REMOVE]:
#                await asyncio.gather(listen(property_type, modification_type), announce(nemesis, account, property_type, modification_type))
        
#    async def test_modify_account_property_mosaic_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        mosaic_id = models.MosaicId.create_from_hex('0dc67fbe1cad29e3')
#        nemesis = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#
#        async def announce(nemesis, value, property_type, modification_type):
#            tx = models.ModifyAccountPropertyMosaicTransaction.create(
#                deadline=models.Deadline.create(),
#                network_type=models.NetworkType.MIJIN_TEST,
#                max_fee=1,
#                property_type=property_type,
#                modifications=[models.AccountPropertyModification(modification_type, value)]
#            )
#            
#            signed_tx = tx.sign_with(nemesis, gen_hash)
#
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_tx)
#
#        async def listen(property_type, modification_type, value):
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(nemesis.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.ModifyAccountPropertyMosaicTransaction), True)
#                    self.assertEqual(len(tx.modifications), 1)
#                    self.assertEqual(tx.property_type, property_type)
#                    self.assertEqual(tx.modifications[0].modification_type, modification_type)
#                    self.assertEqual(tx.modifications[0].value, value)
#                    break
#
#        for property_type in [models.PropertyType.ALLOW_MOSAIC, models.PropertyType.BLOCK_MOSAIC]:
#            for modification_type in [models.PropertyModificationType.ADD, models.PropertyModificationType.REMOVE]:
#                await asyncio.gather(listen(property_type, modification_type, mosaic_id), announce(nemesis, mosaic_id, property_type, modification_type))
        
    async def test_modify_account_property_entity_type_transaction(self):
        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'

        tx_type = models.TransactionType.LINK_ACCOUNT
        #account = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        account = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)

        async def announce(account, value, property_type, modification_type):
            tx = models.ModifyAccountPropertyEntityTypeTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                max_fee=1,
                property_type=property_type,
                modifications=[models.AccountPropertyModification(modification_type, value)]
            )
            
            signed_tx = tx.sign_with(account, gen_hash)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

        async def listen(account, value, property_type, modification_type):
            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
                await listener.confirmed(account.address)

                async for m in listener:
                    #TODO: Check for more transactions. It could not always be the first one.
                    #TODO: Implement timeout.
                    tx = m.message
                    self.assertEqual(isinstance(tx, models.ModifyAccountPropertyEntityTypeTransaction), True)
                    self.assertEqual(len(tx.modifications), 1)
                    self.assertEqual(tx.property_type, property_type)
                    self.assertEqual(tx.modifications[0].modification_type, modification_type)
                    self.assertEqual(tx.modifications[0].value, value)
                    break

        for property_type in [models.PropertyType.BLOCK_TRANSACTION]:
            for modification_type in [models.PropertyModificationType.ADD, models.PropertyModificationType.REMOVE]:
                await asyncio.gather(listen(account, tx_type, property_type, modification_type), announce(account, tx_type, property_type, modification_type))
