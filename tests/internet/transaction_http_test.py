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
import time
from binascii import hexlify
import nest_asyncio
nest_asyncio.apply()

M = 1000000
M1 = M
M10 = 10 * M
M100 = 100 * M
M1000 = 1000 * M

class Error(Exception):
    pass

async def status(account):
    async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
        await listener.status(account.address)
        
        async for m in listener:
            tx = m.message
            raise Error(tx.status)

async def confirmed(account):
    async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
        await listener.confirmed(account.address)
        
        async for m in listener:
            return m.message

async def aggregate_bonded_added(account):
    async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
        await listener.aggregate_bonded_added(account.address)
        
        async for m in listener:
            return m.message

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

    gen_hash: str = '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'
    sleep_timeout: int = 60
    step: float = 0.1

    nemesis: models.Account
    alice: models.Account
    bob: models.Account
    mike: models.Account

    mosaic_id: models.MosaicId

    def __init__(self, task) -> None:
        super().__init__(task)

        self.nemesis = models.Account.create_from_private_key('28FCECEA252231D2C86E1BCF7DD541552BDBBEFBB09324758B3AC199B4AA7B78', models.NetworkType.MIJIN_TEST)
        self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
        self.bob = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
        self.mike = models.Account.create_from_private_key   ('0000000000000000000000000000000000000000000000000000000000000001', models.NetworkType.MIJIN_TEST)
        self.mosaic_id = models.MosaicId.create_from_hex('0dc67fbe1cad29e3')
    
    
    async def send_funds(self, sender, recipient, amount):
        tx = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=recipient.address,
            mosaics=[models.Mosaic(self.mosaic_id, amount)],
            network_type=models.NetworkType.MIJIN_TEST,
            fee_strategy=util.FeeCalculationStrategy.MEDIUM
        )

        signed_tx = tx.sign_with(sender, self.gen_hash)
        
        task1 = asyncio.create_task(confirmed(sender))
        task2 = asyncio.create_task(status(sender))
      
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.TransferTransaction), True)
                self.assertEqual(tx.recipient, recipient.address)
                self.assertEqual(len(tx.mosaics), 1)
                self.assertEqual(tx.mosaics[0].id, self.mosaic_id)
                self.assertEqual(tx.mosaics[0].amount, amount)
                break

            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step
    

    async def test_transfer_transaction(self): 
        self.send_funds(self.nemesis, self.alice, M10)

    
    async def test_message_transaction(self):
        self.send_funds(self.nemesis, self.alice, M10)
        
        message = models.PlainMessage(b'Hello world')

        tx = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=self.bob.address,
            network_type=models.NetworkType.MIJIN_TEST,
            fee_strategy=util.FeeCalculationStrategy.MEDIUM,
            message=message
        )

        signed_tx = tx.sign_with(self.alice, self.gen_hash)

        task1 = asyncio.create_task(confirmed(self.alice))
        task2 = asyncio.create_task(status(self.alice))

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.TransferTransaction), True)
                self.assertEqual(tx.recipient, self.bob.address)
                self.assertEqual(tx.message, message)
                break
            
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step

    
    async def test_account_link_transaction(self):
        self.send_funds(self.nemesis, self.alice, M100)
        
        tx = models.AccountLinkTransaction.create(
            deadline=models.Deadline.create(),
            remote_account_key=self.bob.public_key,
            link_action=models.LinkAction.LINK,
            network_type=models.NetworkType.MIJIN_TEST,
            fee_strategy=util.FeeCalculationStrategy.MEDIUM,
        )

        signed_tx = tx.sign_with(self.alice, self.gen_hash)
        
        task1 = asyncio.create_task(confirmed(self.alice))
        task2 = asyncio.create_task(status(self.alice))
        
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.AccountLinkTransaction), True)
                self.assertEqual(tx.remote_account_key, self.bob.public_key.upper())
                self.assertEqual(tx.link_action, models.LinkAction.LINK)
                break
            
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step
        
        tx = models.AccountLinkTransaction.create(
            deadline=models.Deadline.create(),
            remote_account_key=self.bob.public_key,
            link_action=models.LinkAction.UNLINK,
            network_type=models.NetworkType.MIJIN_TEST,
            fee_strategy=util.FeeCalculationStrategy.MEDIUM,
        )

        signed_tx = tx.sign_with(self.alice, self.gen_hash)
        
        task1 = asyncio.create_task(confirmed(self.alice))
        
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.AccountLinkTransaction), True)
                self.assertEqual(tx.remote_account_key, self.bob.public_key.upper())
                self.assertEqual(tx.link_action, models.LinkAction.UNLINK)
                break
            
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step
    
    
    async def test_modify_account_property_address_transaction(self):
        self.send_funds(self.nemesis, self.alice, M100)
        
        task2 = asyncio.create_task(status(self.alice))

        for property_type in [models.PropertyType.ALLOW_ADDRESS, models.PropertyType.BLOCK_ADDRESS]:
            for modification_type in [models.PropertyModificationType.ADD, models.PropertyModificationType.REMOVE]:
        
                tx = models.ModifyAccountPropertyAddressTransaction.create(
                    deadline=models.Deadline.create(),
                    network_type=models.NetworkType.MIJIN_TEST,
                    fee_strategy=util.FeeCalculationStrategy.MEDIUM,
                    property_type=property_type,
                    modifications=[models.AccountPropertyModification(modification_type, self.bob.address)]
                )
                
                signed_tx = tx.sign_with(self.alice, self.gen_hash)

                task1 = asyncio.create_task(confirmed(self.alice))

                with client.TransactionHTTP(responses.ENDPOINT) as http:
                    http.announce(signed_tx)

                slept = 0
                while (slept < self.sleep_timeout):
                    if (task1.done()):
                        tx = task1.result()
                        self.assertEqual(isinstance(tx, models.ModifyAccountPropertyAddressTransaction), True)
                        self.assertEqual(len(tx.modifications), 1)
                        self.assertEqual(tx.property_type, property_type)
                        self.assertEqual(tx.modifications[0].modification_type, modification_type)
                        break
                
                    if (task2.done()):
                        task2.result()

                    await asyncio.sleep(self.step)
                    slept += self.step

        
    async def test_modify_account_property_mosaic_transaction(self):
        self.send_funds(self.nemesis, self.alice, M100)
        
        task2 = asyncio.create_task(status(self.alice))

        for property_type in [models.PropertyType.ALLOW_MOSAIC, models.PropertyType.BLOCK_MOSAIC]:
            for modification_type in [models.PropertyModificationType.ADD, models.PropertyModificationType.REMOVE]:

                tx = models.ModifyAccountPropertyMosaicTransaction.create(
                    deadline=models.Deadline.create(),
                    network_type=models.NetworkType.MIJIN_TEST,
                    fee_strategy=util.FeeCalculationStrategy.MEDIUM,
                    property_type=property_type,
                    modifications=[models.AccountPropertyModification(modification_type, self.mosaic_id)]
                )
                
                signed_tx = tx.sign_with(self.alice, self.gen_hash)

                task1 = asyncio.create_task(confirmed(self.alice))

                with client.TransactionHTTP(responses.ENDPOINT) as http:
                    http.announce(signed_tx)

                slept = 0
                while (slept < self.sleep_timeout):
                    if (task1.done()):
                        tx = task1.result()
                        self.assertEqual(isinstance(tx, models.ModifyAccountPropertyMosaicTransaction), True)
                        self.assertEqual(len(tx.modifications), 1)
                        self.assertEqual(tx.property_type, property_type)
                        self.assertEqual(tx.modifications[0].modification_type, modification_type)
                        self.assertEqual(tx.modifications[0].value, self.mosaic_id)
                        break
                    
                    if (task2.done()):
                        task2.result()

                    await asyncio.sleep(self.step)
                    slept += self.step

        
    async def test_modify_account_property_entity_type_transaction(self):
        self.send_funds(self.nemesis, self.alice, M100)
        
        task2 = asyncio.create_task(status(self.alice))
        tx_type = models.TransactionType.AGGREGATE_COMPLETE

        for property_type in [models.PropertyType.BLOCK_TRANSACTION]:
            for modification_type in [models.PropertyModificationType.ADD, models.PropertyModificationType.REMOVE]:

                tx = models.ModifyAccountPropertyEntityTypeTransaction.create(
                    deadline=models.Deadline.create(),
                    network_type=models.NetworkType.MIJIN_TEST,
                    fee_strategy=util.FeeCalculationStrategy.MEDIUM,
                    property_type=property_type,
                    modifications=[models.AccountPropertyModification(modification_type, tx_type)]
                )
                
                signed_tx = tx.sign_with(self.alice, self.gen_hash)

                task1 = asyncio.create_task(confirmed(self.alice))

                with client.TransactionHTTP(responses.ENDPOINT) as http:
                    http.announce(signed_tx)

                slept = 0
                while (slept < self.sleep_timeout):
                    if (task1.done()):
                        tx = task1.result()
                        self.assertEqual(isinstance(tx, models.ModifyAccountPropertyEntityTypeTransaction), True)
                        self.assertEqual(len(tx.modifications), 1)
                        self.assertEqual(tx.property_type, property_type)
                        self.assertEqual(tx.modifications[0].modification_type, modification_type)
                        self.assertEqual(tx.modifications[0].value, tx_type)
                        break

                    if (task2.done()):
                        task2.result()

                    await asyncio.sleep(self.step)
                    slept += self.step

    
    async def test_register_namespace_transaction(self):
        self.send_funds(self.nemesis, self.mike, 4 * M1000)
        
        namespace_name = 'foo' + hexlify(os.urandom(4)).decode('utf-8')
        #namespace_name = 'foo'

        # Create namespace
        tx = models.RegisterNamespaceTransaction.create_root_namespace(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            namespace_name=namespace_name,
            duration=60
        )
        
        signed_tx = tx.sign_with(self.mike, self.gen_hash)

        task1 = asyncio.create_task(confirmed(self.mike))
        task2 = asyncio.create_task(status(self.mike))

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.RegisterNamespaceTransaction), True)
                self.assertEqual(tx.namespace_name, namespace_name)
                break
                    
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step

        # Create sub namespace
        tx = models.RegisterNamespaceTransaction.create_sub_namespace(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            namespace_name='bar',
            parent_namespace=namespace_name
        )
        
        signed_tx = tx.sign_with(self.mike, self.gen_hash)

        task1 = asyncio.create_task(confirmed(self.mike))
        
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.RegisterNamespaceTransaction), True)
                self.assertEqual(tx.namespace_name, 'bar')
                break
            
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step
    
        self.mikes_namespace = namespace_name + ".bar"

        # Link address alias
        for action_type in [models.AliasActionType.LINK, models.AliasActionType.UNLINK]:
            tx = models.AddressAliasTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                max_fee=1,
                fee_strategy=util.FeeCalculationStrategy.MEDIUM,
                action_type=action_type,
                namespace_id=models.NamespaceId(self.mikes_namespace),
                address=self.mike.address
            )
            
            signed_tx = tx.sign_with(self.mike, self.gen_hash)

            task1 = asyncio.create_task(confirmed(self.mike))
        
            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            slept = 0
            while (slept < self.sleep_timeout):
                if (task1.done()):
                    tx = task1.result()
                    self.assertEqual(isinstance(tx, models.AddressAliasTransaction), True)
                    self.assertEqual(tx.action_type, action_type)
                    self.assertEqual(tx.address, self.mike.address)
                    break

                if (task2.done()):
                    task2.result()

                await asyncio.sleep(self.step)
                slept += self.step

        # Create mosaic
        nonce = models.MosaicNonce(6)
        mosaic_id = models.MosaicId.create_from_nonce(nonce, self.mike)

        tx = models.MosaicDefinitionTransaction.create(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            fee_strategy=util.FeeCalculationStrategy.MEDIUM,
            nonce=nonce,
            mosaic_id=mosaic_id,
            mosaic_properties=models.MosaicProperties(0x3, 3),
        )
        
        signed_tx = tx.sign_with(self.mike, self.gen_hash)
        
        task1 = asyncio.create_task(confirmed(self.mike))
        task2 = asyncio.create_task(status(self.mike))

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)
        
        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.MosaicDefinitionTransaction), True)
                self.assertEqual(tx.mosaic_id, mosaic_id)
                break
            
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step

        # Link mosaic alias
        for action_type in [models.AliasActionType.LINK, models.AliasActionType.UNLINK]:
            tx = models.MosaicAliasTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                max_fee=1,
                action_type=action_type,
                namespace_id=models.NamespaceId(self.mikes_namespace),
                mosaic_id=mosaic_id,
            )

            signed_tx = tx.sign_with(self.mike, self.gen_hash)
        
            task1 = asyncio.create_task(confirmed(self.mike))

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            slept = 0
            while (slept < self.sleep_timeout):
                if (task1.done()):
                    tx = task1.result()
                    self.assertEqual(isinstance(tx, models.MosaicAliasTransaction), True)
                    self.assertEqual(tx.mosaic_id, mosaic_id)
                    self.assertEqual(tx.action_type, action_type)
                    break
            
                if (task2.done()):
                    task2.result()

                await asyncio.sleep(self.step)
                slept += self.step
   

    async def test_secret_lock_transaction(self):
        self.send_funds(self.nemesis, self.alice, M100)
        self.send_funds(self.nemesis, self.bob, M100)
        
        random_bytes = os.urandom(20)
        h = hashlib.sha3_256(random_bytes)
        secret = binascii.hexlify(h.digest()).decode('utf-8').upper()
        proof = binascii.hexlify(random_bytes).decode('utf-8').upper()

        tx = models.SecretLockTransaction.create(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            mosaic=models.Mosaic(self.mosaic_id, M1),
            duration=60,
            hash_type=models.HashType.SHA3_256,
            secret=secret,
            recipient=self.bob.address,
            fee_strategy=util.FeeCalculationStrategy.MEDIUM,
        )
        
        signed_tx = tx.sign_with(self.alice, self.gen_hash)
        
        task1 = asyncio.create_task(confirmed(self.alice))
        task2 = asyncio.create_task(status(self.alice))

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.SecretLockTransaction), True)
                self.assertEqual(tx.recipient, self.bob.address)
                self.assertEqual(tx.secret, secret)
                break
            
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step
       
        tx = models.SecretProofTransaction.create(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            hash_type=models.HashType.SHA3_256,
            secret=secret,
            proof=proof,
            recipient=self.bob.address,
            fee_strategy=util.FeeCalculationStrategy.MEDIUM,
        )
        
        signed_tx = tx.sign_with(self.alice, self.gen_hash)
        
        task1 = asyncio.create_task(confirmed(self.alice))
        
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.SecretProofTransaction), True)
                self.assertEqual(tx.recipient, self.bob.address)
                self.assertEqual(tx.secret, secret)
                break
            
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step
    

    async def test_aggregate_transaction_with_cosigners(self):
        self.send_funds(self.nemesis, self.alice, M100)
        self.send_funds(self.nemesis, self.bob, M100)

        alice_to_bob = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=self.bob.address,
            mosaics=[models.Mosaic(self.mosaic_id, M10)],
            network_type=models.NetworkType.MIJIN_TEST,
        )

        bob_to_alice = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=self.alice.address,
            mosaics=[models.Mosaic(self.mosaic_id, M10)],
            network_type=models.NetworkType.MIJIN_TEST,
        )
        
        tx = models.AggregateTransaction.create_complete(
            deadline=models.Deadline.create(),
            inner_transactions=[bob_to_alice.to_aggregate(self.bob), alice_to_bob.to_aggregate(self.alice)],
            network_type=models.NetworkType.MIJIN_TEST,
            fee_strategy=util.FeeCalculationStrategy.MEDIUM,
        )

        signed_tx = tx.sign_transaction_with_cosignatories(self.alice, self.gen_hash, [self.bob])
        
        task1 = asyncio.create_task(confirmed(self.alice))
        task2 = asyncio.create_task(status(self.alice))
    
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)
        
        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
                self.assertEqual(len(tx.inner_transactions), 2)
                self.assertEqual(tx.inner_transactions[0].recipient, self.alice.address)
                self.assertEqual(tx.inner_transactions[1].recipient, self.bob.address)
                break
            
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step
       
    
    async def test_aggregate_bonded_transaction(self):
        self.send_funds(self.nemesis, self.alice, M100)
        self.send_funds(self.nemesis, self.bob, M100)

        alice_to_bob = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=self.bob.address,
            mosaics=[models.Mosaic(self.mosaic_id, M10)],
            network_type=models.NetworkType.MIJIN_TEST,
        )

        bob_to_alice = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=self.alice.address,
            mosaics=[models.Mosaic(self.mosaic_id, M10)],
            network_type=models.NetworkType.MIJIN_TEST,
        )
        
        bonded = models.AggregateTransaction.create_bonded(
            deadline=models.Deadline.create(),
            inner_transactions=[bob_to_alice.to_aggregate(self.bob), alice_to_bob.to_aggregate(self.alice)],
            network_type=models.NetworkType.MIJIN_TEST,
            fee_strategy=util.FeeCalculationStrategy.MEDIUM,
        )

        signed_bonded = bonded.sign_transaction_with_cosignatories(self.alice, self.gen_hash)

        lock = models.LockFundsTransaction.create(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            mosaic=models.Mosaic(self.mosaic_id, M10),
            duration=60,
            signed_transaction=signed_bonded,
            fee_strategy=util.FeeCalculationStrategy.MEDIUM,
        )
        
        signed_lock = lock.sign_with(self.alice, self.gen_hash)

        task1 = asyncio.create_task(confirmed(self.alice))
        task2 = asyncio.create_task(status(self.alice))
    
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_lock)

        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.LockFundsTransaction), True)
                break
        
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step
       
        task1 = asyncio.create_task(aggregate_bonded_added(self.alice))
       
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce_partial(signed_bonded)

        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
                break
      
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step

        with client.AccountHTTP(responses.ENDPOINT) as http:
            reply = http.aggregate_bonded_transactions(self.bob)
            self.assertEqual(isinstance(reply[0], models.Transaction), True)
            self.assertEqual(isinstance(reply[0], models.AggregateTransaction), True)
            self.assertEqual(isinstance(reply[0], models.AggregateBondedTransaction), True)

            signed_cosig = models.CosignatureTransaction.create(reply[0]).sign_with(self.bob)
            
        task1 = asyncio.create_task(confirmed(self.bob))
        task2 = asyncio.create_task(status(self.bob))

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce_cosignature(signed_cosig)

        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
                break
            
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step


    async def test_create_multisig_and_send_funds(self):
        multisig = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
        
        self.send_funds(self.nemesis, self.alice, M100)
        self.send_funds(self.nemesis, self.bob, M100)
        self.send_funds(self.nemesis, multisig, M100)

        change_to_multisig = models.ModifyMultisigAccountTransaction.create(
            deadline=models.Deadline.create(),
            min_approval_delta=2,
            min_removal_delta=1,
            modifications=[
                models.MultisigCosignatoryModification.create(self.alice, models.MultisigCosignatoryModificationType.ADD),
                models.MultisigCosignatoryModification.create(self.bob, models.MultisigCosignatoryModificationType.ADD),
            ],
            network_type=models.NetworkType.MIJIN_TEST,
        )

        tx = models.AggregateTransaction.create_complete(
            deadline=models.Deadline.create(),
            inner_transactions=[change_to_multisig.to_aggregate(multisig)],
            network_type=models.NetworkType.MIJIN_TEST,
            fee_strategy=util.FeeCalculationStrategy.MEDIUM,
        )

        signed_tx = tx.sign_transaction_with_cosignatories(multisig, self.gen_hash, [self.alice, self.bob])
        
        task1 = asyncio.create_task(confirmed(multisig))
        task2 = asyncio.create_task(status(multisig))

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
                break
            
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step
        
        multisig_to_nemesis = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=self.nemesis.address,
            mosaics=[models.Mosaic(self.mosaic_id, M10)],
            network_type=models.NetworkType.MIJIN_TEST,
        )
            
        tx = models.AggregateTransaction.create_complete(
            deadline=models.Deadline.create(),
            inner_transactions=[multisig_to_nemesis.to_aggregate(multisig)],
            network_type=models.NetworkType.MIJIN_TEST,
            fee_strategy=util.FeeCalculationStrategy.MEDIUM,
        )

        signed_tx = tx.sign_transaction_with_cosignatories(self.alice, self.gen_hash, [self.bob])
      
        task1 = asyncio.create_task(confirmed(self.alice))
        task2 = asyncio.create_task(status(self.alice))
        
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        slept = 0
        while (slept < self.sleep_timeout):
            if (task1.done()):
                tx = task1.result()
                self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
                break
            
            if (task2.done()):
                task2.result()

            await asyncio.sleep(self.step)
            slept += self.step
        
