from nem2 import client
from nem2 import models
from tests import harness
from tests import config
from tests import responses
from tests import aitertools
import datetime
import binascii
import asyncio
import hashlib
import os
from nem2 import util

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
#        #nemesis = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#        #self.assertEqual(nemesis.address.address, 'SBGS2IGUED476REYI5ZZGISVSEHAF6YIQZV6YJFQ')
#        #recipient = models.Address('SAFSPPRI4MBM3R7USYLJHUODAD5ZEK65YUP35NV6')
#        
#        nemesis = models.Account.create_from_private_key('85CFAB0E6079DAA58D7FF0990ACA64E571EC58527A16DB9391C87C436261190C', models.NetworkType.MIJIN_TEST)
#        self.assertEqual(nemesis.address.address, 'SC4YXLM6XTLSWVM4STVSOYEPN634CGREPOFNIMS3')
#
#        bob = models.Account.create_from_private_key('75CFAB0E6079DAA58D7FF0990ACA64E571EC58527A16DB9391C87C436261190C', models.NetworkType.MIJIN_TEST)
#
#        recipient = bob.address
#
#        mosaic_id = models.MosaicId.create_from_hex('0dc67fbe1cad29e3')
#        amount = 1000000
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
#                    self.assertEqual(tx.address, account.address)
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
#                    self.assertEqual(tx.address, account.address)
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
#                    self.assertEqual(tx.address, account.address)
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
#        
#    async def test_modify_account_property_entity_type_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        tx_type = models.TransactionType.AGGREGATE_COMPLETE
#        #account = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#        #account = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#        account = models.Account.create_from_private_key('75CFAB0E6079DAA58D7FF0990ACA64E571EC58527A16DB9391C87C436261190C', models.NetworkType.MIJIN_TEST)
#
#        async def announce(account, value, property_type, modification_type):
#            tx = models.ModifyAccountPropertyEntityTypeTransaction.create(
#                deadline=models.Deadline.create(),
#                network_type=models.NetworkType.MIJIN_TEST,
#                max_fee=1,
#                property_type=property_type,
#                modifications=[models.AccountPropertyModification(modification_type, value)]
#            )
#            
#            signed_tx = tx.sign_with(account, gen_hash)
#
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_tx)
#
#        async def listen(account, value, property_type, modification_type):
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(account.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.ModifyAccountPropertyEntityTypeTransaction), True)
#                    self.assertEqual(len(tx.modifications), 1)
#                    self.assertEqual(tx.property_type, property_type)
#                    self.assertEqual(tx.modifications[0].modification_type, modification_type)
#                    self.assertEqual(tx.modifications[0].value, value)
#                    break
#
#        for property_type in [models.PropertyType.BLOCK_TRANSACTION]:
#            #for modification_type in [models.PropertyModificationType.ADD, models.PropertyModificationType.REMOVE]:
#            for modification_type in [models.PropertyModificationType.ADD]:
#                await asyncio.gather(listen(account, tx_type, property_type, modification_type), announce(account, tx_type, property_type, modification_type))
#    
#    async def test_register_namespace_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        #account = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#        account = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#
#        tx = models.RegisterNamespaceTransaction.create_root_namespace(
#            deadline=models.Deadline.create(),
#            network_type=models.NetworkType.MIJIN_TEST,
#            namespace_name='foobar',
#            duration=60
#        )
#        
#        signed_tx = tx.sign_with(account, gen_hash)
#
#        async def announce():
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_tx)
#
#        async def listen():
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(account.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.RegisterNamespaceTransaction), True)
#                    self.assertEqual(tx.namespace_name, 'foobar')
#                    break
#
#        await asyncio.gather(listen(), announce())

#    async def test_address_alias_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        #account = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#        account = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#
#        async def announce(action_type):
#            tx = models.AddressAliasTransaction.create(
#                deadline=models.Deadline.create(),
#                network_type=models.NetworkType.MIJIN_TEST,
#                max_fee=1,
#                action_type=action_type,
#                namespace_id=models.NamespaceId(0xb8ffeb12bcf3840f),
#                address=account.address
#            )
#            
#            signed_tx = tx.sign_with(account, gen_hash)
#
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_tx)
#
#        async def listen(action_type):
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(account.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.AddressAliasTransaction), True)
#                    self.assertEqual(tx.action_type, action_type)
#                    self.assertEqual(tx.address, account.address)
#                    break
#
#        for action in [models.AliasActionType.LINK, models.AliasActionType.UNLINK]:
#            await asyncio.gather(listen(action), announce(action))

#    async def test_register_sub_namespace_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        #account = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#        account = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#
#        tx = models.RegisterNamespaceTransaction.create_sub_namespace(
#            deadline=models.Deadline.create(),
#            network_type=models.NetworkType.MIJIN_TEST,
#            namespace_name='subfoobar',
#            parent_namespace='foobar'
#        )
#        
#        signed_tx = tx.sign_with(account, gen_hash)
#
#        async def announce():
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_tx)
#
#        async def listen():
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(account.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.RegisterNamespaceTransaction), True)
#                    self.assertEqual(tx.namespace_name, 'subfoobar')
#                    break
#
#        await asyncio.gather(listen(), announce())
    
#    async def test_secret_lock_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        account = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#        account2 = models.Account.create_from_private_key('2C8178EF9ED7A6D30ABDC1E4D30D68B05861112A98B1629FBE2C8D16FDE97A1C', models.NetworkType.MIJIN_TEST)
#        mosaic_id = models.MosaicId.create_from_hex('0dc67fbe1cad29e3')
#
#        random_bytes = os.urandom(20)
#        h = hashlib.sha3_256(random_bytes)
#        secret = binascii.hexlify(h.digest()).decode('utf-8').upper()
#        proof = binascii.hexlify(random_bytes).decode('utf-8').upper()
#
#        async def announce_lock():
#            lock_tx = models.SecretLockTransaction.create(
#                deadline=models.Deadline.create(),
#                network_type=models.NetworkType.MIJIN_TEST,
#                mosaic=models.Mosaic(mosaic_id, 1000),
#                duration=60,
#                hash_type=models.HashType.SHA3_256,
#                secret=secret,
#                recipient=account2.address,
#            )
#            
#            signed_lock_tx = lock_tx.sign_with(account, gen_hash)
#            
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_lock_tx)
#
#        async def listen_lock():
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(account.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.SecretLockTransaction), True)
#                    self.assertEqual(tx.recipient, account2.address)
#                    self.assertEqual(tx.secret, secret)
#                    break
#       
#        async def announce_proof():
#            proof_tx = models.SecretProofTransaction.create(
#                deadline=models.Deadline.create(),
#                network_type=models.NetworkType.MIJIN_TEST,
#                hash_type=models.HashType.SHA3_256,
#                secret=secret,
#                proof=proof,
#                recipient=account2.address,
#            )
#            
#            signed_proof_tx = proof_tx.sign_with(account, gen_hash)
#            
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_proof_tx)
#
#        async def listen_proof():
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(account.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.SecretProofTransaction), True)
#                    self.assertEqual(tx.recipient, account2.address)
#                    self.assertEqual(tx.secret, secret)
#                    break
#
#        await asyncio.gather(listen_lock(), announce_lock())
#        await asyncio.gather(listen_proof(), announce_proof())
#    async def test_mosaic_definition_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        account = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#        self.assertEqual(account.address.address, 'SBGS2IGUED476REYI5ZZGISVSEHAF6YIQZV6YJFQ')
#
#        nonce = models.MosaicNonce(6)
#        mosaic_id = models.MosaicId.create_from_nonce(nonce, account)
#
#        tx = models.MosaicDefinitionTransaction.create(
#            deadline=models.Deadline.create(),
#            network_type=models.NetworkType.MIJIN_TEST,
#            max_fee=1,
#            nonce=nonce,
#            mosaic_id=mosaic_id,
#            mosaic_properties=models.MosaicProperties(0x3, 3),
#        )
#        
#        signed_tx = tx.sign_with(account, gen_hash)
#
#        async def announce():
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_tx)
#
#        async def listen():
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(account.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.MosaicDefinitionTransaction), True)
#                    self.assertEqual(tx.mosaic_id, mosaic_id)
#                    break
#
#        await asyncio.gather(listen(), announce())

#    async def test_mosaic_alias_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        account = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#        self.assertEqual(account.address.address, 'SBGS2IGUED476REYI5ZZGISVSEHAF6YIQZV6YJFQ')
#
#        mosaic_id = models.MosaicId.create_from_hex('647F9824FCAD73B0')
#
#
#        async def announce(action_type):
#            tx = models.MosaicAliasTransaction.create(
#                deadline=models.Deadline.create(),
#                network_type=models.NetworkType.MIJIN_TEST,
#                max_fee=1,
#                action_type=action_type,
#                namespace_id=models.NamespaceId(0xb8ffeb12bcf3840f),
#                mosaic_id=mosaic_id,
#            )
#
#            signed_tx = tx.sign_with(account, gen_hash)
#
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_tx)
#
#        async def listen(action_type):
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(account.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.MosaicAliasTransaction), True)
#                    self.assertEqual(tx.mosaic_id, mosaic_id)
#                    self.assertEqual(tx.action_type, action_type)
#                    break
#
#        await asyncio.gather(listen(models.AliasActionType.LINK), announce(models.AliasActionType.LINK))
#        await asyncio.gather(listen(models.AliasActionType.UNLINK), announce(models.AliasActionType.UNLINK))
    
#    async def test_aggregate_single_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        alice = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#        bob = models.Account.create_from_private_key('2C8178EF9ED7A6D30ABDC1E4D30D68B05861112A98B1629FBE2C8D16FDE97A1C', models.NetworkType.MIJIN_TEST)
#        mosaic_id = models.MosaicId.create_from_hex('0dc67fbe1cad29e3')
#        amount = 1000
#
#        alice_to_bob = models.TransferTransaction.create(
#            deadline=models.Deadline.create(),
#            recipient=bob.address,
#            mosaics=[models.Mosaic(mosaic_id, amount)],
#            network_type=models.NetworkType.MIJIN_TEST,
#            max_fee=1
#        )
#
#        aggregate = models.AggregateTransaction.create_complete(
#            deadline=models.Deadline.create(),
#            inner_transactions=[alice_to_bob.to_aggregate(alice)],
#            network_type=models.NetworkType.MIJIN_TEST,
#        )
#
#        agregate_signed = aggregate.sign_transaction_with_cosignatories(alice, gen_hash, None)
#    
#        async def announce_lock():
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(agregate_signed)
#
#        async def listen_lock():
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(alice.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
#                    self.assertEqual(len(tx.inner_transactions), 1)
#                    self.assertEqual(tx.inner_transactions[0].recipient, bob.address)
#                    break
#       
#        await asyncio.gather(listen_lock(), announce_lock())


#    async def test_aggregate_transaction_with_cosigners(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        alice = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#        bob = models.Account.create_from_private_key('75CFAB0E6079DAA58D7FF0990ACA64E571EC58527A16DB9391C87C436261190C', models.NetworkType.MIJIN_TEST)
#        mosaic_id = models.MosaicId.create_from_hex('0dc67fbe1cad29e3')
#        amount = 1000
#
#        alice_to_bob = models.TransferTransaction.create(
#            deadline=models.Deadline.create(),
#            recipient=bob.address,
#            mosaics=[models.Mosaic(mosaic_id, amount)],
#            network_type=models.NetworkType.MIJIN_TEST,
#            max_fee=1
#        )
#
#        bob_to_alice = models.TransferTransaction.create(
#            deadline=models.Deadline.create(),
#            recipient=alice.address,
#            mosaics=[models.Mosaic(mosaic_id, amount)],
#            network_type=models.NetworkType.MIJIN_TEST,
#            max_fee=1
#        )
#        
#        initiator = alice
#        cosignatories = [bob]
#        inner_transactions=[bob_to_alice.to_aggregate(bob), alice_to_bob.to_aggregate(alice)]
#            
#        aggregate = models.AggregateTransaction.create_complete(
#            deadline=models.Deadline.create(),
#            inner_transactions=inner_transactions,
#            network_type=models.NetworkType.MIJIN_TEST,
#            max_fee=75000
#        )
#
#        agregate_signed = aggregate.sign_transaction_with_cosignatories(initiator, gen_hash, cosignatories)
#    
#        async def announce_lock():
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(agregate_signed)
#
#        async def listen_lock():
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(initiator.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
#                    self.assertEqual(len(tx.inner_transactions), len(inner_transactions))
#                    self.assertEqual(tx.inner_transactions[0].recipient, alice.address)
#                    self.assertEqual(tx.inner_transactions[1].recipient, bob.address)
#                    break
#       
#        await asyncio.gather(listen_lock(), announce_lock())
    
#    async def test_aggregate_bonded_transaction(self):
#        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
#
#        alice = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
#        bob = models.Account.create_from_private_key('2C8178EF9ED7A6D30ABDC1E4D30D68B05861112A98B1629FBE2C8D16FDE97A1C', models.NetworkType.MIJIN_TEST)
#        mosaic_id = models.MosaicId.create_from_hex('0dc67fbe1cad29e3')
#        amount = 10000000
#
#        alice_to_bob = models.TransferTransaction.create(
#            deadline=models.Deadline.create(),
#            recipient=bob.address,
#            mosaics=[models.Mosaic(mosaic_id, amount)],
#            network_type=models.NetworkType.MIJIN_TEST,
#            max_fee=1
#        )
#
#        bob_to_alice = models.TransferTransaction.create(
#            deadline=models.Deadline.create(),
#            recipient=alice.address,
#            mosaics=[models.Mosaic(mosaic_id, amount)],
#            network_type=models.NetworkType.MIJIN_TEST,
#            max_fee=1
#        )
#        
#        inner_transactions=[bob_to_alice.to_aggregate(bob), alice_to_bob.to_aggregate(alice)]
#            
#        bonded = models.AggregateTransaction.create_bonded(
#            deadline=models.Deadline.create(),
#            inner_transactions=inner_transactions,
#            network_type=models.NetworkType.MIJIN_TEST,
#            max_fee=75000
#        )
#
#        bonded_signed = bonded.sign_transaction_with_cosignatories(alice, gen_hash)
#
#        lock_tx = models.LockFundsTransaction.create(
#            deadline=models.Deadline.create(),
#            network_type=models.NetworkType.MIJIN_TEST,
#            mosaic=models.Mosaic(mosaic_id, amount),
#            duration=60,
#            signed_transaction=bonded_signed
#        )
#        
#        signed_lock_tx = lock_tx.sign_with(alice, gen_hash)
#
#        async def announce_lock():
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce(signed_lock_tx)
#
#        async def listen_lock():
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(alice.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.LockFundsTransaction), True)
#                    break
#       
#        await asyncio.gather(listen_lock(), announce_lock())
#
#        async def announce_bonded():
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce_partial(bonded_signed)
#
#        async def listen_bonded():
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.aggregate_bonded_added(alice.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
#                    break
#       
#        await asyncio.gather(listen_bonded(), announce_bonded())
#
#        with client.AccountHTTP(responses.ENDPOINT) as http:
#            reply = http.aggregate_bonded_transactions(bob)
#            self.assertEqual(isinstance(reply[0], models.Transaction), True)
#            self.assertEqual(isinstance(reply[0], models.AggregateTransaction), True)
#            self.assertEqual(isinstance(reply[0], models.AggregateBondedTransaction), True)
#
#            cosig_signed = models.CosignatureTransaction.create(reply[0]).sign_with(bob)
#            
#        async def announce_cosig():
#            with client.TransactionHTTP(responses.ENDPOINT) as http:
#                http.announce_cosignature(cosig_signed)
#
#        async def listen_cosig():
#            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
#                await listener.confirmed(bob.address)
#
#                async for m in listener:
#                    #TODO: Check for more transactions. It could not always be the first one.
#                    #TODO: Implement timeout.
#                    tx = m.message
#                    self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
#                    break
#       
#        await asyncio.gather(listen_cosig(), announce_cosig())

    async def test_create_multisig_and_send_funds(self):
        gen_hash = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'

        nemesis = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
        
        alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
        bob = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
        multisig = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
        

        mosaic_id = models.MosaicId.create_from_hex('0dc67fbe1cad29e3')

        nemesis_to_alice = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=alice.address,
            mosaics=[models.Mosaic(mosaic_id, 10000000)],
            network_type=models.NetworkType.MIJIN_TEST,
            max_fee=1
        )
        nemesis_to_bob = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=bob.address,
            mosaics=[models.Mosaic(mosaic_id, 10000000)],
            network_type=models.NetworkType.MIJIN_TEST,
            max_fee=1
        )
        nemesis_to_multisig = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=multisig.address,
            mosaics=[models.Mosaic(mosaic_id, 100000000)],
            network_type=models.NetworkType.MIJIN_TEST,
            max_fee=1
        )
            
        aggregate = models.AggregateTransaction.create_complete(
            deadline=models.Deadline.create(),
            inner_transactions=[
                nemesis_to_alice.to_aggregate(nemesis), 
                nemesis_to_bob.to_aggregate(nemesis),
                nemesis_to_multisig.to_aggregate(nemesis),
            ],
            network_type=models.NetworkType.MIJIN_TEST,
            max_fee=75000
        )

        aggregate_signed = aggregate.sign_transaction_with_cosignatories(nemesis, gen_hash, [])
      
        async def announce():
            with client.TransactionHTTP(responses.ENDPOINT) as http:
                print('Announcing %s' % aggregate_signed.hash)
                http.announce(aggregate_signed)

        async def listen():
            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
                await listener.confirmed(nemesis.address)

                async for m in listener:
                    #TODO: Check for more transactions. It could not always be the first one.
                    #TODO: Implement timeout.
                    tx = m.message
                    self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
                    break

        await asyncio.gather(listen(), announce())

        change_to_multisig = models.ModifyMultisigAccountTransaction.create(
            deadline=models.Deadline.create(),
            min_approval_delta=2,
            min_removal_delta=1,
            modifications=[
                models.MultisigCosignatoryModification.create(alice, models.MultisigCosignatoryModificationType.ADD),
                models.MultisigCosignatoryModification.create(bob, models.MultisigCosignatoryModificationType.ADD),
            ],
            network_type=models.NetworkType.MIJIN_TEST,
            max_fee=1
        )

        change_to_multisig_aggregate = models.AggregateTransaction.create_complete(
            deadline=models.Deadline.create(),
            inner_transactions=[change_to_multisig.to_aggregate(multisig)],
            network_type=models.NetworkType.MIJIN_TEST,
            max_fee=75000
        )

        change_to_multisig_aggregate_signed = change_to_multisig_aggregate.sign_transaction_with_cosignatories(multisig, gen_hash, [alice, bob])
        
        async def announce_multisig():
            with client.TransactionHTTP(responses.ENDPOINT) as http:
                print('Announcing %s' % change_to_multisig_aggregate_signed.hash)
                http.announce(change_to_multisig_aggregate_signed)

        async def listen_multisig():
            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
                await listener.confirmed(multisig.address)

                async for m in listener:
                    #TODO: Check for more transactions. It could not always be the first one.
                    #TODO: Implement timeout.
                    tx = m.message
                    self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
                    break

        await asyncio.gather(listen_multisig(), announce_multisig())
        
        multisig_to_nemesis = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=nemesis.address,
            mosaics=[models.Mosaic(mosaic_id, 1000000)],
            network_type=models.NetworkType.MIJIN_TEST,
            max_fee=1
        )
            
        multisig_to_nemesis_aggregate = models.AggregateTransaction.create_complete(
            deadline=models.Deadline.create(),
            inner_transactions=[multisig_to_nemesis.to_aggregate(multisig)],
            network_type=models.NetworkType.MIJIN_TEST,
            max_fee=75000
        )

        multisig_to_nemesis_aggregate_signed = multisig_to_nemesis_aggregate.sign_transaction_with_cosignatories(alice, gen_hash, [bob])
      
        async def announce3():
            with client.TransactionHTTP(responses.ENDPOINT) as http:
                print('Announcing %s' % multisig_to_nemesis_aggregate_signed.hash)
                http.announce(multisig_to_nemesis_aggregate_signed)

        async def listen3():
            async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
                await listener.confirmed(multisig.address)

                async for m in listener:
                    #TODO: Check for more transactions. It could not always be the first one.
                    #TODO: Implement timeout.
                    tx = m.message
                    self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
                    break

        await asyncio.gather(listen3(), announce3())
