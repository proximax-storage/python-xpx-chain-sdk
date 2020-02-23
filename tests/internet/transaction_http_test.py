from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config
from tests import responses
import binascii
import hashlib
import os
from xpxchain import util
from binascii import hexlify
import requests
import typing
import asyncio
from tests.helper import listen, listen_bonded, send_funds, prepare

_1 = config.divisibility * 1
_10 = _1 * 10
_100 = _1 * 100
_1000 = _1 * 1000


class TestTransactionHttp(harness.TestCase):

    t1: typing.Sequence[models.Account]
    t2: typing.Sequence[models.Account]
    t3: typing.Sequence[models.Account]
    t4: typing.Sequence[models.Account]
    hashes: typing.Sequence[str] = []

    @classmethod
    def setUpClass(cls):

        cls.t1 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(0)]
        cls.t2 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(9)]
        cls.t3 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(3)]
        cls.t4 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(1)]

        loop = asyncio.get_event_loop()
        cls.hashes = loop.run_until_complete(prepare(
            [send_funds(config.tester, account, _1) for account in cls.t1]
            + [send_funds(config.tester, account, _10) for account in cls.t2]
            + [send_funds(config.tester, account, _100) for account in cls.t3]
            + [send_funds(config.tester, account, _1000) for account in cls.t4]
        ))

    # TESTS

    def test_get_transaction(self):
        with client.TransactionHTTP(config.ENDPOINT) as http:
            reply = http.get_transaction(self.hashes[0])
            self.assertEqual(isinstance(reply, models.TransferTransaction), True)
            self.assertEqual(reply.transaction_info.hash, self.hashes[0])

    def test_get_transactions(self):
        with client.TransactionHTTP(config.ENDPOINT) as http:
            reply = http.get_transactions(self.hashes)
            self.assertEqual(len(reply), len(self.hashes))
            self.assertEqual(isinstance(reply[0], models.TransferTransaction), True)
            for tx in reply:
                self.assertEqual(tx.transaction_info.hash in self.hashes, True)

    def test_get_transaction_status(self):
        with client.TransactionHTTP(config.ENDPOINT) as http:
            reply = http.get_transaction_status(self.hashes[0])
            self.assertEqual(isinstance(reply, models.TransactionStatus), True)
            self.assertEqual(reply.hash, self.hashes[0])

    def test_get_transaction_statuses(self):
        with client.TransactionHTTP(config.ENDPOINT) as http:
            reply = http.get_transaction_statuses(self.hashes)
            self.assertEqual(len(reply), len(self.hashes))
            self.assertEqual(isinstance(reply[0], models.TransactionStatus), True)
            for hash in reply:
                self.assertEqual(hash.hash in self.hashes, True)

#    def test_transfer_transaction(self):
#        self.send_funds(config.tester, alice, _10)
#
    async def test_message_transaction(self):
        alice = self.t2.pop()
        bob = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))

        message = models.PlainMessage(b'Hello world')

        tx = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=bob.address,
            network_type=config.network_type,
            message=message
        )

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)
        self.assertEqual(isinstance(tx, models.TransferTransaction), True)
        self.assertEqual(tx.recipient, bob.address)
        self.assertEqual(tx.message, message)

    async def test_account_link_transaction(self):
        alice = self.t2.pop()
        bob = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))

        tx = models.AccountLinkTransaction.create(
            deadline=models.Deadline.create(),
            remote_account_key=bob.public_key,
            link_action=models.LinkAction.LINK,
            network_type=config.network_type,
        )

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)
        self.assertEqual(isinstance(tx, models.AccountLinkTransaction), True)
        self.assertEqual(tx.remote_account_key, bob.public_key.upper())
        self.assertEqual(tx.link_action, models.LinkAction.LINK)

        tx = models.AccountLinkTransaction.create(
            deadline=models.Deadline.create(),
            remote_account_key=bob.public_key,
            link_action=models.LinkAction.UNLINK,
            network_type=config.network_type,
        )

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)
        self.assertEqual(isinstance(tx, models.AccountLinkTransaction), True)
        self.assertEqual(tx.remote_account_key, bob.public_key.upper())
        self.assertEqual(tx.link_action, models.LinkAction.UNLINK)

    async def test_modify_account_property_address_transaction(self):
        alice = self.t2.pop()
        bob = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))

        for property_type in [models.PropertyType.ALLOW_ADDRESS, models.PropertyType.BLOCK_ADDRESS]:
            for modification_type in [models.PropertyModificationType.ADD, models.PropertyModificationType.REMOVE]:

                tx = models.ModifyAccountPropertyAddressTransaction.create(
                    deadline=models.Deadline.create(),
                    network_type=config.network_type,
                    property_type=property_type,
                    modifications=[models.AccountPropertyModification(modification_type, bob.address)]
                )

                signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

                with client.TransactionHTTP(config.ENDPOINT) as http:
                    http.announce(signed_tx)

                tx = await listen(alice)
                self.assertEqual(isinstance(tx, models.ModifyAccountPropertyAddressTransaction), True)
                self.assertEqual(len(tx.modifications), 1)
                self.assertEqual(tx.property_type, property_type)
                self.assertEqual(tx.modifications[0].modification_type, modification_type)
                self.assertEqual(tx.modifications[0].value, bob.address)

    async def test_modify_account_property_mosaic_transaction(self):
        alice = self.t2.pop()

        for property_type in [models.PropertyType.ALLOW_MOSAIC, models.PropertyType.BLOCK_MOSAIC]:
            for modification_type in [models.PropertyModificationType.ADD, models.PropertyModificationType.REMOVE]:

                tx = models.ModifyAccountPropertyMosaicTransaction.create(
                    deadline=models.Deadline.create(),
                    network_type=config.network_type,
                    property_type=property_type,
                    modifications=[models.AccountPropertyModification(modification_type, config.mosaic_id)]
                )

                signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

                with client.TransactionHTTP(config.ENDPOINT) as http:
                    http.announce(signed_tx)

                tx = await listen(alice)
                self.assertEqual(isinstance(tx, models.ModifyAccountPropertyMosaicTransaction), True)
                self.assertEqual(len(tx.modifications), 1)
                self.assertEqual(tx.property_type, property_type)
                self.assertEqual(tx.modifications[0].modification_type, modification_type)
                self.assertEqual(tx.modifications[0].value, config.mosaic_id)

    async def test_modify_account_property_entity_type_transaction(self):
        alice = self.t2.pop()

        tx_type = models.TransactionType.AGGREGATE_COMPLETE

        for property_type in [models.PropertyType.BLOCK_TRANSACTION]:
            for modification_type in [models.PropertyModificationType.ADD, models.PropertyModificationType.REMOVE]:

                tx = models.ModifyAccountPropertyEntityTypeTransaction.create(
                    deadline=models.Deadline.create(),
                    network_type=config.network_type,
                    property_type=property_type,
                    modifications=[models.AccountPropertyModification(modification_type, tx_type)]
                )

                signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

                with client.TransactionHTTP(config.ENDPOINT) as http:
                    http.announce(signed_tx)

                tx = await listen(alice)
                self.assertEqual(isinstance(tx, models.ModifyAccountPropertyEntityTypeTransaction), True)
                self.assertEqual(len(tx.modifications), 1)
                self.assertEqual(tx.property_type, property_type)
                self.assertEqual(tx.modifications[0].modification_type, modification_type)
                self.assertEqual(tx.modifications[0].value, tx_type)

    async def test_register_namespace_transaction(self):
        alice = self.t4.pop()

        namespace_name = 'foo' + hexlify(os.urandom(4)).decode('utf-8')

        # Create namespace
        tx = models.RegisterNamespaceTransaction.create_root_namespace(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            namespace_name=namespace_name,
            duration=60
        )

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)
        self.assertEqual(isinstance(tx, models.RegisterNamespaceTransaction), True)
        self.assertEqual(tx.namespace_name, namespace_name)

        # Create sub namespace
        tx = models.RegisterNamespaceTransaction.create_sub_namespace(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            namespace_name='bar',
            parent_namespace=namespace_name
        )

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)
        self.assertEqual(isinstance(tx, models.RegisterNamespaceTransaction), True)
        self.assertEqual(tx.namespace_name, 'bar')

        alices_namespace = namespace_name + ".bar"

        # Link address alias
        for action_type in [models.AliasActionType.LINK, models.AliasActionType.UNLINK]:
            tx = models.AddressAliasTransaction.create(
                deadline=models.Deadline.create(),
                network_type=config.network_type,
                max_fee=1,
                action_type=action_type,
                namespace_id=models.NamespaceId(alices_namespace),
                address=alice.address
            )

            signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(config.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = await listen(alice)
            self.assertEqual(isinstance(tx, models.AddressAliasTransaction), True)
            self.assertEqual(tx.action_type, action_type)
            self.assertEqual(tx.address, alice.address)

        # Create mosaic
        nonce = models.MosaicNonce(1)
        mosaic_id = models.MosaicId.create_from_nonce(nonce, alice)

        tx = models.MosaicDefinitionTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            nonce=nonce,
            mosaic_id=mosaic_id,
            mosaic_properties=models.MosaicProperties(0x3, 3),
        )

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)
        self.assertEqual(isinstance(tx, models.MosaicDefinitionTransaction), True)
        self.assertEqual(tx.mosaic_id, mosaic_id)

        # Link mosaic alias
        for action_type in [models.AliasActionType.LINK, models.AliasActionType.UNLINK]:
            tx = models.MosaicAliasTransaction.create(
                deadline=models.Deadline.create(),
                network_type=config.network_type,
                max_fee=1,
                action_type=action_type,
                namespace_id=models.NamespaceId(alices_namespace),
                mosaic_id=mosaic_id,
            )

            signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(config.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = await listen(alice)
            self.assertEqual(isinstance(tx, models.MosaicAliasTransaction), True)
            self.assertEqual(tx.mosaic_id, mosaic_id)
            self.assertEqual(tx.action_type, action_type)

    async def test_secret_lock_transaction(self):
        alice = self.t2.pop()
        bob = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))

        random_bytes = os.urandom(20)
        h = hashlib.sha3_256(random_bytes)
        secret = binascii.hexlify(h.digest()).decode('utf-8').upper()
        proof = binascii.hexlify(random_bytes).decode('utf-8').upper()

        tx = models.SecretLockTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            mosaic=models.Mosaic(config.mosaic_id, _1),
            duration=60,
            hash_type=models.HashType.SHA3_256,
            secret=secret,
            recipient=bob.address,
        )

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)
        self.assertEqual(isinstance(tx, models.SecretLockTransaction), True)
        self.assertEqual(tx.recipient, bob.address)
        self.assertEqual(tx.secret, secret)

        tx = models.SecretProofTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            hash_type=models.HashType.SHA3_256,
            secret=secret,
            proof=proof,
            recipient=bob.address,
        )

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)
        self.assertEqual(isinstance(tx, models.SecretProofTransaction), True)
        self.assertEqual(tx.recipient, bob.address)
        self.assertEqual(tx.secret, secret)

    async def test_aggregate_transaction_with_cosigners(self):
        alice = self.t3.pop()
        bob = self.t2.pop()

        alice_to_bob = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=bob.address,
            mosaics=[models.Mosaic(config.mosaic_id, _1)],
            network_type=config.network_type,
        )

        bob_to_alice = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=alice.address,
            mosaics=[models.Mosaic(config.mosaic_id, _1)],
            network_type=config.network_type,
        )

        tx = models.AggregateTransaction.create_complete(
            deadline=models.Deadline.create(),
            inner_transactions=[bob_to_alice.to_aggregate(bob), alice_to_bob.to_aggregate(alice)],
            network_type=config.network_type,
        )

        signed_tx = tx.sign_transaction_with_cosignatories(alice, config.gen_hash, [bob], fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
        self.assertEqual(len(tx.inner_transactions), 2)
        self.assertEqual(tx.inner_transactions[0].recipient, alice.address)
        self.assertEqual(tx.inner_transactions[1].recipient, bob.address)

    async def test_aggregate_bonded_transaction(self):
        alice = self.t3.pop()
        bob = self.t2.pop()

        alice_to_bob = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=bob.address,
            mosaics=[models.Mosaic(config.mosaic_id, _1)],
            network_type=config.network_type,
        )

        bob_to_alice = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=alice.address,
            mosaics=[models.Mosaic(config.mosaic_id, _1)],
            network_type=config.network_type,
        )

        bonded = models.AggregateTransaction.create_bonded(
            deadline=models.Deadline.create(),
            inner_transactions=[bob_to_alice.to_aggregate(bob), alice_to_bob.to_aggregate(alice)],
            network_type=config.network_type,
        )

        signed_bonded = bonded.sign_transaction_with_cosignatories(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        lock = models.LockFundsTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            mosaic=models.Mosaic(config.mosaic_id, _10),
            duration=60,
            signed_transaction=signed_bonded,
        )

        signed_lock = lock.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_lock)

        tx = await listen(alice)
        self.assertEqual(isinstance(tx, models.LockFundsTransaction), True)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce_partial(signed_bonded)

        tx = await listen_bonded(alice)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

        with client.AccountHTTP(config.ENDPOINT) as http:
            reply = http.aggregate_bonded_transactions(bob)
            self.assertEqual(isinstance(reply[0], models.Transaction), True)
            self.assertEqual(isinstance(reply[0], models.AggregateTransaction), True)
            self.assertEqual(isinstance(reply[0], models.AggregateBondedTransaction), True)

            signed_cosig = models.CosignatureTransaction.create(reply[0]).sign_with(bob)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce_cosignature(signed_cosig)

        tx = await listen(bob)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

    async def test_create_multisig_and_send_funds(self):
        multisig = self.t3.pop()
        alice = self.t2.pop()
        bob = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))

        change_to_multisig = models.ModifyMultisigAccountTransaction.create(
            deadline=models.Deadline.create(),
            min_approval_delta=2,
            min_removal_delta=1,
            modifications=[
                models.MultisigCosignatoryModification.create(alice, models.MultisigCosignatoryModificationType.ADD),
                models.MultisigCosignatoryModification.create(bob, models.MultisigCosignatoryModificationType.ADD),
            ],
            network_type=config.network_type,
        )

        tx = models.AggregateTransaction.create_complete(
            deadline=models.Deadline.create(),
            inner_transactions=[change_to_multisig.to_aggregate(multisig)],
            network_type=config.network_type,
        )

        signed_tx = tx.sign_transaction_with_cosignatories(multisig, config.gen_hash, [alice, bob], fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(multisig)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

        multisig_to_tester = models.TransferTransaction.create(
            deadline=models.Deadline.create(),
            recipient=config.tester.address,
            mosaics=[models.Mosaic(config.mosaic_id, _1)],
            network_type=config.network_type,
        )

        tx = models.AggregateTransaction.create_complete(
            deadline=models.Deadline.create(),
            inner_transactions=[multisig_to_tester.to_aggregate(multisig)],
            network_type=config.network_type,
        )

        signed_tx = tx.sign_transaction_with_cosignatories(alice, config.gen_hash, [bob], fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)
