from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config
from tests import responses
from tests import aitertools
import datetime
import binascii
import asyncio
import hashlib
import os
from xpxchain import util
import time
from binascii import hexlify
#import nest_asyncio
#nest_asyncio.apply()

M = 1000000
M1 = M
M10 = 10 * M
M100 = 100 * M
M1000 = 1000 * M

class Error(Exception):
    pass

class TestTransactionHttp(harness.TestCase):

    alice: models.Account
    bob: models.Account
    mike: models.Account

    def __init__(self, task) -> None:
        super().__init__(task)

        if (task == 'test_get_transaction'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))

        elif (task == 'test_get_transactions'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))

        elif (task == 'test_get_transaction_status'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))

        elif (task == 'test_get_transaction_statuses'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))

        elif (task == 'test_transfer_transaction'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))

        elif (task == 'test_message_transaction'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.bob = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, M10)
        
        elif (task == 'test_account_link_transaction'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.bob = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, M100)
        
        elif (task == 'test_modify_account_property_address_transaction'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.bob = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, M100)
        
        elif (task == 'test_modify_account_property_mosaic_transaction'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, M100)
        
        elif (task == 'test_modify_account_property_entity_type_transaction'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, M100)
        
        elif (task == 'test_register_namespace_transaction'):
            self.mike = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.mike, 4 * M1000)
        
        elif (task == 'test_secret_lock_transaction'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.bob = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, M100)
            self.send_funds(config.nemesis, self.bob, M100)
        
        elif (task == 'test_aggregate_transaction_with_cosigners'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.bob = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, M100)
            self.send_funds(config.nemesis, self.bob, M100)

        elif (task == 'test_aggregate_bonded_transaction'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.bob = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, M100)
            self.send_funds(config.nemesis, self.bob, M100)

        elif (task == 'test_create_multisig_and_send_funds'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.bob = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.multisig = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy = lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, M100)
            self.send_funds(config.nemesis, self.bob, M100)
            self.send_funds(config.nemesis, self.multisig, M100)

    
    async def listen(self, account):
        async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
            await listener.confirmed(account.address)
            await listener.status(account.address)
       
            async for m in listener:
                if (m.channel_name == 'status'):
                    raise Error(m.message)
                elif (m.channel_name == 'confirmedAdded'):
                    return m.message
    
    async def listen_bonded(self, account):
        async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
            await listener.aggregate_bonded_added(account.address)
            await listener.status(account.address)
       
            async for m in listener:
                if (m.channel_name == 'status'):
                    raise Error(m.message)
                elif (m.channel_name == 'partialAdded'):
                    return m.message

    def send_funds(self, sender, recipient, amount):
        tx = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=recipient.address,
            mosaics=[models.Mosaic(config.mosaic_id, amount)],
            network_type=models.NetworkType.MIJIN_TEST,
        )

        signed_tx = tx.sign_with(sender, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)
        
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = self.listen(sender)
        self.assertEqual(isinstance(tx, models.TransferTransaction), True)
        self.assertEqual(tx.recipient, recipient.address)
        self.assertEqual(len(tx.mosaics), 1)
        self.assertEqual(tx.mosaics[0].id, config.mosaic_id)
        self.assertEqual(tx.mosaics[0].amount, amount)

        return tx.transaction_info.hash
    

    # TESTS
    def test_get_transaction(self):
        hash = self.send_funds(config.nemesis, self.alice, M10)

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            reply = http.get_transaction(hash)
            self.assertEqual(isinstance(reply, models.TransferTransaction), True)
            self.assertEqual(reply.transaction_info.hash, hash)

    
    def test_get_transactions(self):
        hash1 = self.send_funds(config.nemesis, self.alice, M10)
        hash2 = self.send_funds(config.nemesis, self.alice, M10)

        hashes = [hash1, hash2]
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            reply = http.get_transactions(hashes)
            self.assertEqual(len(reply), 2)
            self.assertEqual(isinstance(reply[0], models.TransferTransaction), True)
            self.assertEqual(reply[0].transaction_info.hash in hashes, True)
            self.assertEqual(reply[1].transaction_info.hash in hashes, True)

    
    def test_get_transaction_status(self):
        hash = self.send_funds(config.nemesis, self.alice, M10)

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            reply = http.get_transaction_status(hash)
            self.assertEqual(isinstance(reply, models.TransactionStatus), True)
            self.assertEqual(reply.hash, hash)


    def test_get_transaction_statuses(self):
        hash1 = self.send_funds(config.nemesis, self.alice, M10)
        hash2 = self.send_funds(config.nemesis, self.alice, M10)

        hashes = [hash1, hash2]
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            reply = http.get_transaction_statuses(hashes)
            self.assertEqual(len(reply), 2)
            self.assertEqual(isinstance(reply[0], models.TransactionStatus), True)
            self.assertEqual(reply[0].hash in hashes, True)
            self.assertEqual(reply[1].hash in hashes, True)

    
#    def test_transfer_transaction(self): 
#        self.send_funds(config.nemesis, self.alice, M10)


    def test_message_transaction(self):
        message = models.PlainMessage(b'Hello world')

        tx = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=self.bob.address,
            network_type=models.NetworkType.MIJIN_TEST,
            message=message
        )

        signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = self.listen(self.alice)
        self.assertEqual(isinstance(tx, models.TransferTransaction), True)
        self.assertEqual(tx.recipient, self.bob.address)
        self.assertEqual(tx.message, message)

    
    def test_account_link_transaction(self):
        tx = models.AccountLinkTransaction.create(
            deadline=models.Deadline.create(),
            remote_account_key=self.bob.public_key,
            link_action=models.LinkAction.LINK,
            network_type=models.NetworkType.MIJIN_TEST,
        )

        signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)
        
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = self.listen(self.alice)
        self.assertEqual(isinstance(tx, models.AccountLinkTransaction), True)
        self.assertEqual(tx.remote_account_key, self.bob.public_key.upper())
        self.assertEqual(tx.link_action, models.LinkAction.LINK)
        
        tx = models.AccountLinkTransaction.create(
            deadline=models.Deadline.create(),
            remote_account_key=self.bob.public_key,
            link_action=models.LinkAction.UNLINK,
            network_type=models.NetworkType.MIJIN_TEST,
        )

        signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)
        
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = self.listen(self.alice)
        self.assertEqual(isinstance(tx, models.AccountLinkTransaction), True)
        self.assertEqual(tx.remote_account_key, self.bob.public_key.upper())
        self.assertEqual(tx.link_action, models.LinkAction.UNLINK)
    
    
    def test_modify_account_property_address_transaction(self):
        for property_type in [models.PropertyType.ALLOW_ADDRESS, models.PropertyType.BLOCK_ADDRESS]:
            for modification_type in [models.PropertyModificationType.ADD, models.PropertyModificationType.REMOVE]:
        
                tx = models.ModifyAccountPropertyAddressTransaction.create(
                    deadline=models.Deadline.create(),
                    network_type=models.NetworkType.MIJIN_TEST,
                    property_type=property_type,
                    modifications=[models.AccountPropertyModification(modification_type, self.bob.address)]
                )
                
                signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

                with client.TransactionHTTP(responses.ENDPOINT) as http:
                    http.announce(signed_tx)

                tx = self.listen(self.alice)
                self.assertEqual(isinstance(tx, models.ModifyAccountPropertyAddressTransaction), True)
                self.assertEqual(len(tx.modifications), 1)
                self.assertEqual(tx.property_type, property_type)
                self.assertEqual(tx.modifications[0].modification_type, modification_type)

        
    def test_modify_account_property_mosaic_transaction(self):
        for property_type in [models.PropertyType.ALLOW_MOSAIC, models.PropertyType.BLOCK_MOSAIC]:
            for modification_type in [models.PropertyModificationType.ADD, models.PropertyModificationType.REMOVE]:

                tx = models.ModifyAccountPropertyMosaicTransaction.create(
                    deadline=models.Deadline.create(),
                    network_type=models.NetworkType.MIJIN_TEST,
                    property_type=property_type,
                    modifications=[models.AccountPropertyModification(modification_type, config.mosaic_id)]
                )
                
                signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

                with client.TransactionHTTP(responses.ENDPOINT) as http:
                    http.announce(signed_tx)

                tx = self.listen(self.alice)
                self.assertEqual(isinstance(tx, models.ModifyAccountPropertyMosaicTransaction), True)
                self.assertEqual(len(tx.modifications), 1)
                self.assertEqual(tx.property_type, property_type)
                self.assertEqual(tx.modifications[0].modification_type, modification_type)
                self.assertEqual(tx.modifications[0].value, config.mosaic_id)

        
    def test_modify_account_property_entity_type_transaction(self):
        tx_type = models.TransactionType.AGGREGATE_COMPLETE

        for property_type in [models.PropertyType.BLOCK_TRANSACTION]:
            for modification_type in [models.PropertyModificationType.ADD, models.PropertyModificationType.REMOVE]:

                tx = models.ModifyAccountPropertyEntityTypeTransaction.create(
                    deadline=models.Deadline.create(),
                    network_type=models.NetworkType.MIJIN_TEST,
                    property_type=property_type,
                    modifications=[models.AccountPropertyModification(modification_type, tx_type)]
                )
                
                signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

                with client.TransactionHTTP(responses.ENDPOINT) as http:
                    http.announce(signed_tx)

                tx = self.listen(self.alice)
                self.assertEqual(isinstance(tx, models.ModifyAccountPropertyEntityTypeTransaction), True)
                self.assertEqual(len(tx.modifications), 1)
                self.assertEqual(tx.property_type, property_type)
                self.assertEqual(tx.modifications[0].modification_type, modification_type)
                self.assertEqual(tx.modifications[0].value, tx_type)

    
    def test_register_namespace_transaction(self):
        namespace_name = 'foo' + hexlify(os.urandom(4)).decode('utf-8')
        #namespace_name = 'foo'

        # Create namespace
        tx = models.RegisterNamespaceTransaction.create_root_namespace(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            namespace_name=namespace_name,
            duration=60
        )
        
        signed_tx = tx.sign_with(self.mike, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = self.listen(self.mike)
        self.assertEqual(isinstance(tx, models.RegisterNamespaceTransaction), True)
        self.assertEqual(tx.namespace_name, namespace_name)

        # Create sub namespace
        tx = models.RegisterNamespaceTransaction.create_sub_namespace(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            namespace_name='bar',
            parent_namespace=namespace_name
        )
        
        signed_tx = tx.sign_with(self.mike, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = self.listen(self.mike)
        self.assertEqual(isinstance(tx, models.RegisterNamespaceTransaction), True)
        self.assertEqual(tx.namespace_name, 'bar')
    
        mikes_namespace = namespace_name + ".bar"

        # Link address alias
        for action_type in [models.AliasActionType.LINK, models.AliasActionType.UNLINK]:
            tx = models.AddressAliasTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                max_fee=1,
                action_type=action_type,
                namespace_id=models.NamespaceId(mikes_namespace),
                address=self.mike.address
            )
            
            signed_tx = tx.sign_with(self.mike, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.mike)
            self.assertEqual(isinstance(tx, models.AddressAliasTransaction), True)
            self.assertEqual(tx.action_type, action_type)
            self.assertEqual(tx.address, self.mike.address)

        # Create mosaic
        nonce = models.MosaicNonce(1)
        mosaic_id = models.MosaicId.create_from_nonce(nonce, self.mike)

        tx = models.MosaicDefinitionTransaction.create(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            nonce=nonce,
            mosaic_id=mosaic_id,
            mosaic_properties=models.MosaicProperties(0x3, 3),
        )
        
        signed_tx = tx.sign_with(self.mike, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)
        
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)
        
        tx = self.listen(self.mike)
        self.assertEqual(isinstance(tx, models.MosaicDefinitionTransaction), True)
        self.assertEqual(tx.mosaic_id, mosaic_id)

        # Link mosaic alias
        for action_type in [models.AliasActionType.LINK, models.AliasActionType.UNLINK]:
            tx = models.MosaicAliasTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                max_fee=1,
                action_type=action_type,
                namespace_id=models.NamespaceId(mikes_namespace),
                mosaic_id=mosaic_id,
            )

            signed_tx = tx.sign_with(self.mike, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)
        
            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.mike)
            self.assertEqual(isinstance(tx, models.MosaicAliasTransaction), True)
            self.assertEqual(tx.mosaic_id, mosaic_id)
            self.assertEqual(tx.action_type, action_type)
   

    def test_secret_lock_transaction(self):
        random_bytes = os.urandom(20)
        h = hashlib.sha3_256(random_bytes)
        secret = binascii.hexlify(h.digest()).decode('utf-8').upper()
        proof = binascii.hexlify(random_bytes).decode('utf-8').upper()

        tx = models.SecretLockTransaction.create(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            mosaic=models.Mosaic(config.mosaic_id, M1),
            duration=60,
            hash_type=models.HashType.SHA3_256,
            secret=secret,
            recipient=self.bob.address,
        )
        
        signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = self.listen(self.alice)
        self.assertEqual(isinstance(tx, models.SecretLockTransaction), True)
        self.assertEqual(tx.recipient, self.bob.address)
        self.assertEqual(tx.secret, secret)
       
        tx = models.SecretProofTransaction.create(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            hash_type=models.HashType.SHA3_256,
            secret=secret,
            proof=proof,
            recipient=self.bob.address,
        )
        
        signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)
        
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = self.listen(self.alice)
        self.assertEqual(isinstance(tx, models.SecretProofTransaction), True)
        self.assertEqual(tx.recipient, self.bob.address)
        self.assertEqual(tx.secret, secret)
    

    def test_aggregate_transaction_with_cosigners(self):
        alice_to_bob = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=self.bob.address,
            mosaics=[models.Mosaic(config.mosaic_id, M10)],
            network_type=models.NetworkType.MIJIN_TEST,
        )

        bob_to_alice = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=self.alice.address,
            mosaics=[models.Mosaic(config.mosaic_id, M10)],
            network_type=models.NetworkType.MIJIN_TEST,
        )

        tx = models.AggregateTransaction.create_complete(
            deadline=models.Deadline.create(),
            inner_transactions=[bob_to_alice.to_aggregate(self.bob), alice_to_bob.to_aggregate(self.alice)],
            network_type=models.NetworkType.MIJIN_TEST,
        )

        signed_tx = tx.sign_transaction_with_cosignatories(self.alice, config.gen_hash, [self.bob], fee_strategy=util.FeeCalculationStrategy.MEDIUM)
        
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)
        
        tx = self.listen(self.alice)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
        self.assertEqual(len(tx.inner_transactions), 2)
        self.assertEqual(tx.inner_transactions[0].recipient, self.alice.address)
        self.assertEqual(tx.inner_transactions[1].recipient, self.bob.address)
       
    
    def test_aggregate_bonded_transaction(self):
        alice_to_bob = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=self.bob.address,
            mosaics=[models.Mosaic(config.mosaic_id, M10)],
            network_type=models.NetworkType.MIJIN_TEST,
        )

        bob_to_alice = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=self.alice.address,
            mosaics=[models.Mosaic(config.mosaic_id, M10)],
            network_type=models.NetworkType.MIJIN_TEST,
        )
        
        bonded = models.AggregateTransaction.create_bonded(
            deadline=models.Deadline.create(),
            inner_transactions=[bob_to_alice.to_aggregate(self.bob), alice_to_bob.to_aggregate(self.alice)],
            network_type=models.NetworkType.MIJIN_TEST,
        )

        signed_bonded = bonded.sign_transaction_with_cosignatories(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        lock = models.LockFundsTransaction.create(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            mosaic=models.Mosaic(config.mosaic_id, M10),
            duration=60,
            signed_transaction=signed_bonded,
        )
        
        signed_lock = lock.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_lock)

        tx = self.listen(self.alice)
        self.assertEqual(isinstance(tx, models.LockFundsTransaction), True)
       
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce_partial(signed_bonded)

        tx = self.listen_bonded(self.alice)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

        with client.AccountHTTP(responses.ENDPOINT) as http:
            reply = http.aggregate_bonded_transactions(self.bob)
            self.assertEqual(isinstance(reply[0], models.Transaction), True)
            self.assertEqual(isinstance(reply[0], models.AggregateTransaction), True)
            self.assertEqual(isinstance(reply[0], models.AggregateBondedTransaction), True)

            signed_cosig = models.CosignatureTransaction.create(reply[0]).sign_with(self.bob)
            
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce_cosignature(signed_cosig)

        tx = self.listen(self.bob)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)


    def test_create_multisig_and_send_funds(self):
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
            inner_transactions=[change_to_multisig.to_aggregate(self.multisig)],
            network_type=models.NetworkType.MIJIN_TEST,
        )

        signed_tx = tx.sign_transaction_with_cosignatories(self.multisig, config.gen_hash, [self.alice, self.bob], fee_strategy=util.FeeCalculationStrategy.MEDIUM)
        
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = self.listen(self.multisig)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
        
        self.multisig_to_nemesis = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=config.nemesis.address,
            mosaics=[models.Mosaic(config.mosaic_id, M10)],
            network_type=models.NetworkType.MIJIN_TEST,
        )
            
        tx = models.AggregateTransaction.create_complete(
            deadline=models.Deadline.create(),
            inner_transactions=[self.multisig_to_nemesis.to_aggregate(self.multisig)],
            network_type=models.NetworkType.MIJIN_TEST,
        )

        signed_tx = tx.sign_transaction_with_cosignatories(self.alice, config.gen_hash, [self.bob], fee_strategy=util.FeeCalculationStrategy.MEDIUM)
      
        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = self.listen(self.alice)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
        
