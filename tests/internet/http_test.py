from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config
import binascii
import hashlib
import os
from binascii import hexlify
import typing
import asyncio
from tests import helper

send_funds = helper.send_funds
announce = helper.announce
announce_partial = helper.announce_partial
announce_cosignature = helper.announce_cosignature

_1 = config.divisibility * 1
_10 = _1 * 10
_100 = _1 * 100
_1000 = _1 * 1000
_10000 = _1 * 10000


class TestT1Http(harness.TestCase):

    t1: typing.Sequence[models.Account]
    t2: typing.Sequence[models.Account]
    t3: typing.Sequence[models.Account]
    t4: typing.Sequence[models.Account]
    t5: typing.Sequence[models.Account]
    t6: typing.Sequence[models.Account]
    hashes: typing.Sequence[str] = []

    @classmethod
    def setUpClass(cls):

        print("Setting up tests... ")

        cls.t1 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(2)]
        cls.t2 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(19)]
        cls.t3 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(3)]
        cls.t4 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(2)]
        cls.t5 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(3)]
        cls.t6 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(1)]

        loop = asyncio.get_event_loop()
        cls.hashes = loop.run_until_complete(helper.prepare(
            [send_funds(config.tester, account, _1) for account in cls.t1]
            + [send_funds(config.tester, account, _10) for account in cls.t2]
            + [send_funds(config.tester, account, _100) for account in cls.t3]
            + [send_funds(config.tester, account, _10000 + _100) for account in cls.t4]
            + [send_funds(config.tester, account, 2 * _10000 + _100) for account in cls.t5]
            + [send_funds(config.tester, account, 3 * _10000 + _100) for account in cls.t6],
            max_run=10
        ))

    # TESTS

    def test_get_transaction(self):
        with client.TransactionHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            reply = http.get_transaction(self.hashes[0])
            self.assertEqual(isinstance(reply, models.TransferTransaction), True)
            self.assertEqual(reply.transaction_info.hash, self.hashes[0])

    def test_get_transactions(self):
        with client.TransactionHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            reply = http.get_transactions(self.hashes[:2])
            self.assertEqual(len(reply), len(self.hashes[:2]))
            self.assertEqual(isinstance(reply[0], models.TransferTransaction), True)
            for tx in reply:
                self.assertEqual(tx.transaction_info.hash in self.hashes, True)

    def test_get_transaction_status(self):
        with client.TransactionHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            reply = http.get_transaction_status(self.hashes[0])
            self.assertEqual(isinstance(reply, models.TransactionStatus), True)
            self.assertEqual(reply.hash, self.hashes[0])

    def test_get_transaction_statuses(self):
        with client.TransactionHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            reply = http.get_transaction_statuses(self.hashes[:2])
            self.assertEqual(len(reply), len(self.hashes[:2]))
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

        signed_tx = tx.sign_with(alice, config.gen_hash)

        tx = await announce(signed_tx)
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

        signed_tx = tx.sign_with(alice, config.gen_hash)

        tx = await announce(signed_tx)
        self.assertEqual(isinstance(tx, models.AccountLinkTransaction), True)
        self.assertEqual(tx.remote_account_key, bob.public_key.upper())
        self.assertEqual(tx.link_action, models.LinkAction.LINK)

        tx = models.AccountLinkTransaction.create(
            deadline=models.Deadline.create(),
            remote_account_key=bob.public_key,
            link_action=models.LinkAction.UNLINK,
            network_type=config.network_type,
        )

        signed_tx = tx.sign_with(alice, config.gen_hash)

        tx = await announce(signed_tx)
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

                signed_tx = tx.sign_with(alice, config.gen_hash)

                tx = await announce(signed_tx)
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

                signed_tx = tx.sign_with(alice, config.gen_hash)

                tx = await announce(signed_tx)
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

                signed_tx = tx.sign_with(alice, config.gen_hash)

                tx = await announce(signed_tx)
                self.assertEqual(isinstance(tx, models.ModifyAccountPropertyEntityTypeTransaction), True)
                self.assertEqual(len(tx.modifications), 1)
                self.assertEqual(tx.property_type, property_type)
                self.assertEqual(tx.modifications[0].modification_type, modification_type)
                self.assertEqual(tx.modifications[0].value, tx_type)

    async def test_register_namespace_transaction(self):
        alice = self.t6.pop()

        namespace_l1 = 'foo' + hexlify(os.urandom(4)).decode('utf-8')
        namespace_l2 = 'bar'
        namespace_name = namespace_l1 + '.' + namespace_l2

        n1, n2 = await helper.create_namespace(alice, namespace_name)
        self.assertEqual(n1.name, namespace_l1)
        self.assertEqual(n2.name, namespace_l2)
        self.assertEqual(isinstance(n2.parent_id, models.NamespaceId), True)

        # Link address alias
        for action_type in [models.AliasActionType.LINK, models.AliasActionType.UNLINK]:
            tx = models.AddressAliasTransaction.create(
                deadline=models.Deadline.create(),
                network_type=config.network_type,
                max_fee=1,
                action_type=action_type,
                namespace_id=n2.namespace_id,
                address=alice.address
            )

            signed_tx = tx.sign_with(alice, config.gen_hash)

            tx = await announce(signed_tx)
            self.assertEqual(isinstance(tx, models.AddressAliasTransaction), True)
            self.assertEqual(tx.action_type, action_type)
            self.assertEqual(tx.address, alice.address)

        mosaic_id = await helper.create_mosaic(alice, 1)
        self.assertEqual(isinstance(mosaic_id, models.MosaicId), True)

        # Link mosaic alias
        for action_type in [models.AliasActionType.LINK, models.AliasActionType.UNLINK]:
            tx = models.MosaicAliasTransaction.create(
                deadline=models.Deadline.create(),
                network_type=config.network_type,
                max_fee=1,
                action_type=action_type,
                namespace_id=n2.namespace_id,
                mosaic_id=mosaic_id,
            )

            signed_tx = tx.sign_with(alice, config.gen_hash)

            tx = await announce(signed_tx)
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

        signed_tx = tx.sign_with(alice, config.gen_hash)

        tx = await announce(signed_tx)
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

        signed_tx = tx.sign_with(alice, config.gen_hash)

        tx = await announce(signed_tx)
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

        signed_tx = tx.sign_transaction_with_cosignatories(alice, config.gen_hash, [bob])

        tx = await announce(signed_tx)
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

        signed_bonded = bonded.sign_transaction_with_cosignatories(alice, config.gen_hash)

        lock = models.LockFundsTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            mosaic=models.Mosaic(config.mosaic_id, _10),
            duration=60,
            signed_transaction=signed_bonded,
        )

        signed_lock = lock.sign_with(alice, config.gen_hash)

        tx = await announce(signed_lock)
        self.assertEqual(isinstance(tx, models.LockFundsTransaction), True)

        tx = await announce_partial(signed_bonded)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

        with client.AccountHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            reply = http.aggregate_bonded_transactions(bob)
            self.assertEqual(isinstance(reply[0], models.Transaction), True)
            self.assertEqual(isinstance(reply[0], models.AggregateTransaction), True)
            self.assertEqual(isinstance(reply[0], models.AggregateBondedTransaction), True)

            signed_cosig = models.CosignatureTransaction.create(reply[0]).sign_with(bob)

        tx = await announce_cosignature(signed_cosig)
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

        signed_tx = tx.sign_transaction_with_cosignatories(multisig, config.gen_hash, [alice, bob])

        tx = await announce(signed_tx)
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

        signed_tx = tx.sign_transaction_with_cosignatories(alice, config.gen_hash, [bob])

        tx = await announce(signed_tx)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

    async def test_multisig_account_info(self):
        alice = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))
        bob = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))
        multisig = self.t2.pop()

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

        signed_tx = tx.sign_transaction_with_cosignatories(multisig, config.gen_hash, [alice, bob])

        tx = await announce(signed_tx)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

        with client.AccountHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_multisig_account_info(multisig.address)
            self.assertEqual(isinstance(info, models.MultisigAccountInfo), True)

    async def test_multisig_account_graph_info(self):
        alice = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))
        bob = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))
        mike = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))
        multisig = self.t2.pop()
        multisig2 = self.t2.pop()

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

        signed_tx = tx.sign_transaction_with_cosignatories(multisig, config.gen_hash, [alice, bob])

        tx = await announce(signed_tx)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

        change_to_multisig = models.ModifyMultisigAccountTransaction.create(
            deadline=models.Deadline.create(),
            min_approval_delta=2,
            min_removal_delta=1,
            modifications=[
                models.MultisigCosignatoryModification.create(mike, models.MultisigCosignatoryModificationType.ADD),
                models.MultisigCosignatoryModification.create(multisig, models.MultisigCosignatoryModificationType.ADD),
            ],
            network_type=config.network_type,
        )

        tx = models.AggregateTransaction.create_complete(
            deadline=models.Deadline.create(),
            inner_transactions=[change_to_multisig.to_aggregate(multisig2)],
            network_type=config.network_type,
        )

        signed_tx = tx.sign_transaction_with_cosignatories(multisig2, config.gen_hash, [alice, bob, mike])

        tx = await announce(signed_tx)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

        with client.AccountHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_multisig_account_graph_info(multisig.address)
            self.assertEqual(isinstance(info, models.MultisigAccountGraphInfo), True)

    async def test_account_names(self):
        alice = self.t5.pop()

        namespace_name = 'foo' + hexlify(os.urandom(4)).decode('utf-8') + '.bar'
        n1, n2 = await helper.create_namespace(alice, namespace_name)

        # Link address alias
        tx = models.AddressAliasTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            max_fee=1,
            action_type=models.AliasActionType.LINK,
            namespace_id=n2.namespace_id,
            address=alice.address
        )

        signed_tx = tx.sign_with(alice, config.gen_hash)

        tx = await announce(signed_tx)
        self.assertEqual(isinstance(tx, models.AddressAliasTransaction), True)
        self.assertEqual(tx.action_type, models.AliasActionType.LINK)
        self.assertEqual(tx.address, alice.address)

        with client.AccountHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_account_names([alice.address])
            self.assertEqual(len(info), 1)
            self.assertEqual(isinstance(info[0], models.AccountNames), True)
            self.assertEqual(len(info[0].names), 1)
            self.assertEqual(info[0].names[0], namespace_name)

    async def test_account_transactions(self):
        alice = self.t1.pop()

        with client.AccountHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.transactions(alice)
            self.assertEqual(len(info), 1)
            self.assertEqual(len(info[0].mosaics), 1)
            self.assertEqual(info[0].mosaics[0], models.Mosaic(config.mosaic_id, _1))
            self.assertEqual(info[0].signer.public_key, config.tester.public_key.upper())

    async def test_incoming_transactions(self):
        alice = self.t1.pop()

        with client.AccountHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.incoming_transactions(alice)
            self.assertEqual(len(info), 1)
            self.assertEqual(len(info[0].mosaics), 1)
            self.assertEqual(info[0].mosaics[0], models.Mosaic(config.mosaic_id, _1))
            self.assertEqual(info[0].signer.public_key, config.tester.public_key.upper())

    async def test_outgoing_transactions(self):
        alice = self.t2.pop()
        bob = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))

        await send_funds(alice, bob, _1, quiet=True)

        with client.AccountHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.outgoing_transactions(alice)
            self.assertEqual(len(info), 1)
            self.assertEqual(len(info[0].mosaics), 1)
            self.assertEqual(info[0].mosaics[0], models.Mosaic(config.mosaic_id, _1))
            self.assertEqual(info[0].recipient, bob.address)

    async def test_account_properties(self):
        alice = self.t2.pop()
        bob = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))
        pete = self.t2.pop()

        # ALLOW_ADDRESS
        tx = models.ModifyAccountPropertyAddressTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            property_type=models.PropertyType.ALLOW_ADDRESS,
            modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, bob.address)]
        )

        signed_tx = tx.sign_with(alice, config.gen_hash)

        tx = await announce(signed_tx)

        # ALLOW_MOSAIC
        tx = models.ModifyAccountPropertyMosaicTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            property_type=models.PropertyType.ALLOW_MOSAIC,
            modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, config.mosaic_id)]
        )

        signed_tx = tx.sign_with(alice, config.gen_hash)

        tx = await announce(signed_tx)

        # BLOCK_ADDRESS
        tx = models.ModifyAccountPropertyAddressTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            property_type=models.PropertyType.BLOCK_ADDRESS,
            modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, bob.address)]
        )

        signed_tx = tx.sign_with(pete, config.gen_hash)

        tx = await announce(signed_tx)

        # BLOCK_MOSAIC
        tx = models.ModifyAccountPropertyMosaicTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            property_type=models.PropertyType.BLOCK_MOSAIC,
            modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, config.mosaic_id)]
        )

        signed_tx = tx.sign_with(pete, config.gen_hash)

        tx = await announce(signed_tx)

        # BLOCK_TRANSACTION
        tx = models.ModifyAccountPropertyEntityTypeTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            property_type=models.PropertyType.BLOCK_TRANSACTION,
            modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, models.TransactionType.AGGREGATE_COMPLETE)]
        )

        signed_tx = tx.sign_with(pete, config.gen_hash)

        tx = await announce(signed_tx)

        with client.AccountHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_account_properties(alice.address)
            self.assertEqual(len(info.properties), 3)
            self.assertEqual(info.properties[0].property_type, models.PropertyType.ALLOW_ADDRESS)
            self.assertEqual(len(info.properties[0].values), 1)
            self.assertEqual(info.properties[0].values[0], bob.address)
            self.assertEqual(info.properties[1].property_type, models.PropertyType.ALLOW_MOSAIC)
            self.assertEqual(len(info.properties[1].values), 1)
            self.assertEqual(info.properties[1].values[0], config.mosaic_id)
            self.assertEqual(info.properties[2].property_type, models.PropertyType.BLOCK_TRANSACTION)
            self.assertEqual(len(info.properties[2].values), 0)

            info = http.get_account_properties(pete.address)
            self.assertEqual(len(info.properties), 3)
            self.assertEqual(info.properties[0].property_type, models.PropertyType.BLOCK_ADDRESS)
            self.assertEqual(len(info.properties[0].values), 1)
            self.assertEqual(info.properties[0].values[0], bob.address)
            self.assertEqual(info.properties[1].property_type, models.PropertyType.BLOCK_MOSAIC)
            self.assertEqual(len(info.properties[1].values), 1)
            self.assertEqual(info.properties[1].values[0], config.mosaic_id)
            self.assertEqual(info.properties[2].property_type, models.PropertyType.BLOCK_TRANSACTION)
            self.assertEqual(len(info.properties[2].values), 1)
            self.assertEqual(info.properties[2].values[0], models.TransactionType.AGGREGATE_COMPLETE)

            info = http.get_accounts_properties([alice.address, pete.address])
            self.assertEqual(len(info), 2)

            for i in info:
                if (i.address == alice.address):
                    self.assertEqual(len(i.properties), 3)
                    self.assertEqual(i.properties[0].property_type, models.PropertyType.ALLOW_ADDRESS)
                    self.assertEqual(len(i.properties[0].values), 1)
                    self.assertEqual(i.properties[0].values[0], bob.address)
                    self.assertEqual(i.properties[1].property_type, models.PropertyType.ALLOW_MOSAIC)
                    self.assertEqual(len(i.properties[1].values), 1)
                    self.assertEqual(i.properties[1].values[0], config.mosaic_id)
                    self.assertEqual(i.properties[2].property_type, models.PropertyType.BLOCK_TRANSACTION)
                    self.assertEqual(len(i.properties[2].values), 0)
                    self.assertEqual(len(i.properties), 3)
                elif (i.address == pete.address):
                    self.assertEqual(i.properties[0].property_type, models.PropertyType.BLOCK_ADDRESS)
                    self.assertEqual(len(i.properties[0].values), 1)
                    self.assertEqual(i.properties[0].values[0], bob.address)
                    self.assertEqual(i.properties[1].property_type, models.PropertyType.BLOCK_MOSAIC)
                    self.assertEqual(len(i.properties[1].values), 1)
                    self.assertEqual(i.properties[1].values[0], config.mosaic_id)
                    self.assertEqual(i.properties[2].property_type, models.PropertyType.BLOCK_TRANSACTION)
                    self.assertEqual(len(i.properties[2].values), 1)
                    self.assertEqual(i.properties[2].values[0], models.TransactionType.AGGREGATE_COMPLETE)
                else:
                    raise Exception(f'Unknown address{i.address.address}')

    async def test_aggregate_bonded_transactions(self):
        alice = self.t2.pop()

        # TODO: Add bonded transaction
        with client.AccountHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.aggregate_bonded_transactions(alice)
            self.assertEqual(len(info), 0)

    async def test_unconfirmed_transactions(self):
        alice = self.t2.pop()

        # TODO: Add unconfirmed transaction
        with client.AccountHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.unconfirmed_transactions(alice)
            self.assertEqual(len(info), 0)

    async def test_get_account_info(self):
        with client.AccountHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_account_info(config.tester.address)
            self.assertEqual(info.public_key, config.tester.public_key.upper()),

    async def test_get_accountis_info(self):
        with client.AccountHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_accounts_info([config.tester.address])
            self.assertEqual(len(info), 1)
            self.assertEqual(info[0].public_key, config.tester.public_key.upper())

    def test_get_merkle_by_hash_in_block(self):
        with client.BlockchainHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            reply = http.get_block_transactions(1)
            tx_hash = reply[0].transaction_info.hash

            info = http.get_merkle_by_hash_in_block(1, tx_hash)
            self.assertEqual(isinstance(info, models.MerkleProofInfo), True)
            self.assertEqual(len(info.merkle_path) > 0, True)
            self.assertEqual(isinstance(info.merkle_path[0], models.MerklePathItem), True)

    def test_get_blocks_by_height_with_limit(self):
        with client.BlockchainHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_blocks_by_height_with_limit(25, 25)
            self.assertEqual(len(info), 25)
            self.assertEqual(isinstance(info[0], models.BlockInfo), True)

    def test_get_block_by_height(self):
        with client.BlockchainHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_block_by_height(25)
            self.assertEqual(isinstance(info, models.BlockInfo), True)

    def test_get_block_transactions(self):
        with client.BlockchainHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_block_transactions(1)
            self.assertEqual(len(info) > 0, True)
            self.assertEqual(isinstance(info[0], models.Transaction), True)
            self.assertEqual(info[0].signer.public_key, config.nemesis.public_key.upper())

    def test_get_block_receipts(self):
        with client.BlockchainHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_block_receipts(25)
            self.assertEqual(isinstance(info, models.Statements), True)
            self.assertEqual(len(info.transaction_statements), 1)
            self.assertEqual(isinstance(info.transaction_statements[0], models.TransactionStatement), True)
            self.assertEqual(len(info.transaction_statements[0].receipts) > 0, True)
            self.assertEqual(isinstance(info.transaction_statements[0].receipts[0], models.BalanceChangeReceipt), True)

    def test_get_diagnostic_storage(self):
        with client.BlockchainHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_diagnostic_storage()
            self.assertEqual(isinstance(info, models.BlockchainStorageInfo), True)

    def test_get_diagnostic_server(self):
        with client.BlockchainHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_diagnostic_server()
            self.assertEqual(isinstance(info, models.BlockchainServerInfo), True)

    def test_get_blockchain_height(self):
        with client.BlockchainHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_blockchain_height()
            self.assertEqual(isinstance(info, int), True)
            self.assertEqual(info >= 1, True)

    def test_get_blockchain_score(self):
        with client.BlockchainHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_blockchain_score()
            self.assertEqual(isinstance(info, models.BlockchainScore), True)

    def test_get_config(self):
        with client.ConfigHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_config(1)
            self.assertEqual(isinstance(info, models.CatapultConfig), True)

    def test_get_upgrade(self):
        with client.ConfigHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_upgrade(1)
            self.assertEqual(isinstance(info, models.CatapultUpgrade), True)

    async def test_new_block(self):
        async with client.Listener(f'{config.ENDPOINT}/ws', network_type=config.network_type) as listener:
            await listener.new_block()

            async for m in listener:
                self.assertEqual(m.channel_name, 'block')
                self.assertEqual(isinstance(m.message, models.BlockInfo), True)
                self.assertEqual(m.message.height >= 1, True)
                break

    async def test_modify_address_metadata_transaction(self):
        alice = self.t2.pop()

        metadata_key = 'foo' + hexlify(os.urandom(4)).decode('ascii')

        for metadata_modification_type in [models.MetadataModificationType.ADD, models.MetadataModificationType.REMOVE]:
            tx = models.ModifyAccountMetadataTransaction.create(
                deadline=models.Deadline.create(),
                network_type=config.network_type,
                metadata_type=models.MetadataType.ADDRESS,
                metadata_id=alice.address,
                modifications=[
                    models.MetadataModification(metadata_modification_type, models.Field(metadata_key, 'bar')),
                    models.MetadataModification(metadata_modification_type, models.Field(metadata_key + '2', 'bar')),
                ],
            )

            signed_tx = tx.sign_with(alice, config.gen_hash)

            tx = await announce(signed_tx)
            self.assertEqual(isinstance(tx, models.ModifyAccountMetadataTransaction), True)
            self.assertEqual(tx.metadata_id, alice.address)
            self.assertEqual(len(tx.modifications) > 0, True)
            self.assertEqual(tx.modifications[0].field.key, metadata_key)
            self.assertEqual(tx.modifications[0].field.value, 'bar')

    async def test_modify_mosaic_metadata_transaction(self):
        alice = self.t4.pop()

        mosaic_id = await helper.create_mosaic(alice, 1)
        metadata_key = 'foo' + hexlify(os.urandom(4)).decode('ascii')

        for metadata_modification_type in [models.MetadataModificationType.ADD, models.MetadataModificationType.REMOVE]:
            tx = models.ModifyMosaicMetadataTransaction.create(
                deadline=models.Deadline.create(),
                network_type=config.network_type,
                metadata_type=models.MetadataType.MOSAIC,
                metadata_id=mosaic_id,
                modifications=[
                    models.MetadataModification(metadata_modification_type, models.Field(metadata_key, 'bar')),
                    models.MetadataModification(metadata_modification_type, models.Field(metadata_key + '2', 'bar')),
                ],
            )

            signed_tx = tx.sign_with(alice, config.gen_hash)

            tx = await announce(signed_tx)
            self.assertEqual(isinstance(tx, models.ModifyMosaicMetadataTransaction), True)
            self.assertEqual(tx.metadata_id, mosaic_id)
            self.assertEqual(len(tx.modifications) > 0, True)
            self.assertEqual(tx.modifications[0].field.key, metadata_key)
            self.assertEqual(tx.modifications[0].field.value, 'bar')

    async def test_modify_namespace_metadata_transaction(self):
        alice = self.t5.pop()

        namespace = 'foo' + hexlify(os.urandom(4)).decode('utf-8') + ".bar"
        await helper.create_namespace(alice, namespace)

        metadata_key = 'foo' + hexlify(os.urandom(4)).decode('ascii')

        for metadata_modification_type in [models.MetadataModificationType.ADD, models.MetadataModificationType.REMOVE]:
            tx = models.ModifyNamespaceMetadataTransaction.create(
                deadline=models.Deadline.create(),
                network_type=config.network_type,
                metadata_type=models.MetadataType.NAMESPACE,
                metadata_id=models.NamespaceId(namespace),
                modifications=[
                    models.MetadataModification(metadata_modification_type, models.Field(metadata_key, 'bar')),
                    models.MetadataModification(metadata_modification_type, models.Field(metadata_key + '2', 'bar')),
                ],
            )

            signed_tx = tx.sign_with(alice, config.gen_hash)

            tx = await announce(signed_tx)
            self.assertEqual(isinstance(tx, models.ModifyNamespaceMetadataTransaction), True)
            self.assertEqual(tx.metadata_id, models.NamespaceId(namespace))
            self.assertEqual(len(tx.modifications) > 0, True)
            self.assertEqual(tx.modifications[0].field.key, metadata_key)
            self.assertEqual(tx.modifications[0].field.value, 'bar')

    async def test_account_metadata(self):
        alice = self.t2.pop()

        self.modifications = [
            models.MetadataModification(models.MetadataModificationType.ADD, models.Field('foo', 'bar')),
            models.MetadataModification(models.MetadataModificationType.ADD, models.Field('foo2', 'bar')),
        ]

        tx = models.ModifyAccountMetadataTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            metadata_type=models.MetadataType.ADDRESS,
            metadata_id=alice.address,
            modifications=self.modifications,
        )

        signed_tx = tx.sign_with(alice, config.gen_hash)

        tx = await announce(signed_tx)

        with client.MetadataHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            reply = http.get_account_metadata(alice)
            self.assertEqual(isinstance(reply, models.AddressMetadataInfo), True)
            self.assertEqual(len(reply.metadata.flds), 2)
            self.assertEqual(reply.metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply.metadata.flds[1], self.modifications[1].field)

            reply = http.get_metadata(alice.address.plain())
            self.assertEqual(isinstance(reply, models.MetadataInfo), True)
            self.assertEqual(isinstance(reply.metadata, models.AddressMetadata), True)
            self.assertEqual(len(reply.metadata.flds), 2)
            self.assertEqual(reply.metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply.metadata.flds[1], self.modifications[1].field)

            reply = http.get_metadatas([alice.address.plain()])
            self.assertEqual(len(reply) > 0, True)
            self.assertEqual(isinstance(reply[0], models.MetadataInfo), True)
            self.assertEqual(isinstance(reply[0].metadata, models.AddressMetadata), True)
            self.assertEqual(len(reply[0].metadata.flds), 2)
            self.assertEqual(reply[0].metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply[0].metadata.flds[1], self.modifications[1].field)

    async def test_mosaic_metadata(self):
        alice = self.t4.pop()

        mosaic_id = await helper.create_mosaic(alice, 1)

        self.modifications = [
            models.MetadataModification(models.MetadataModificationType.ADD, models.Field('foo', 'bar')),
            models.MetadataModification(models.MetadataModificationType.ADD, models.Field('foo2', 'bar')),
        ]

        tx = models.ModifyMosaicMetadataTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            metadata_type=models.MetadataType.MOSAIC,
            metadata_id=mosaic_id,
            modifications=self.modifications,
        )

        signed_tx = tx.sign_with(alice, config.gen_hash)

        tx = await announce(signed_tx)

        with client.MetadataHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            reply = http.get_mosaic_metadata(mosaic_id)
            self.assertEqual(isinstance(reply, models.MosaicMetadataInfo), True)
            self.assertEqual(len(reply.metadata.flds), 2)
            self.assertEqual(reply.metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply.metadata.flds[1], self.modifications[1].field)

            reply = http.get_metadata(mosaic_id.get_id())
            self.assertEqual(isinstance(reply, models.MetadataInfo), True)
            self.assertEqual(isinstance(reply.metadata, models.MosaicMetadata), True)
            self.assertEqual(len(reply.metadata.flds), 2)
            self.assertEqual(reply.metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply.metadata.flds[1], self.modifications[1].field)

            reply = http.get_metadatas([mosaic_id.get_id()])
            self.assertEqual(len(reply) > 0, True)
            self.assertEqual(isinstance(reply[0], models.MetadataInfo), True)
            self.assertEqual(isinstance(reply[0].metadata, models.MosaicMetadata), True)
            self.assertEqual(len(reply[0].metadata.flds), 2)
            self.assertEqual(reply[0].metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply[0].metadata.flds[1], self.modifications[1].field)

    async def test_namespace_metadata(self):
        alice = self.t5.pop()

        self.namespace = 'foo' + hexlify(os.urandom(4)).decode('utf-8') + ".bar"
        await helper.create_namespace(alice, self.namespace)

        self.modifications = [
            models.MetadataModification(models.MetadataModificationType.ADD, models.Field('foo', 'bar')),
            models.MetadataModification(models.MetadataModificationType.ADD, models.Field('foo2', 'bar')),
        ]

        tx = models.ModifyNamespaceMetadataTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            metadata_type=models.MetadataType.NAMESPACE,
            metadata_id=models.NamespaceId(self.namespace),
            modifications=self.modifications,
        )

        signed_tx = tx.sign_with(alice, config.gen_hash)

        tx = await announce(signed_tx)

        with client.MetadataHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            reply = http.get_namespace_metadata(models.NamespaceId(self.namespace))
            self.assertEqual(isinstance(reply, models.NamespaceMetadataInfo), True)
            self.assertEqual(len(reply.metadata.flds), 2)
            self.assertEqual(reply.metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply.metadata.flds[1], self.modifications[1].field)

            reply = http.get_metadata(models.NamespaceId(self.namespace).get_id())
            self.assertEqual(isinstance(reply, models.MetadataInfo), True)
            self.assertEqual(isinstance(reply.metadata, models.NamespaceMetadata), True)
            self.assertEqual(len(reply.metadata.flds), 2)
            self.assertEqual(reply.metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply.metadata.flds[1], self.modifications[1].field)

            reply = http.get_metadatas([models.NamespaceId(self.namespace).get_id()])
            self.assertEqual(len(reply) > 0, True)
            self.assertEqual(isinstance(reply[0], models.MetadataInfo), True)
            self.assertEqual(isinstance(reply[0].metadata, models.NamespaceMetadata), True)
            self.assertEqual(len(reply[0].metadata.flds), 2)
            self.assertEqual(reply[0].metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply[0].metadata.flds[1], self.modifications[1].field)

    def test_get_mosaic(self):
        with client.MosaicHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_mosaic(config.mosaic_id)
            self.assertEqual(isinstance(info, models.MosaicInfo), True)

    def test_get_mosaics(self):
        with client.MosaicHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_mosaics([config.mosaic_id])
            self.assertEqual(len(info), 1)
            self.assertEqual(isinstance(info[0], models.MosaicInfo), True)

    def test_get_mosaic_names(self):
        with client.MosaicHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_mosaic_names([config.mosaic_id])
            self.assertEqual(len(info), 1),
            self.assertEqual(isinstance(info[0], models.MosaicName), True)
            self.assertEqual(info[0].names[0], 'prx.xpx')

    def test_get_namespace(self):
        with client.NamespaceHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_namespace(models.NamespaceId('prx.xpx'))
            self.assertEqual(isinstance(info, models.NamespaceInfo), True)
            self.assertEqual(info.owner.public_key, config.nemesis.public_key.upper())

    def test_get_namespaces_from_account(self):
        with client.NamespaceHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_namespaces_from_account(config.nemesis.address)
            self.assertEqual(len(info) > 0, True)
            self.assertEqual(isinstance(info[0], models.NamespaceInfo), True)

    def test_get_namespaces_from_accounts(self):
        with client.NamespaceHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_namespaces_from_accounts([config.nemesis.address])
            self.assertEqual(len(info) > 0, True)
            self.assertEqual(isinstance(info[0], models.NamespaceInfo), True)

    def test_get_namespaces_name(self):
        with client.NamespaceHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_namespaces_name([models.NamespaceId('prx.xpx')])
            self.assertEqual(len(info), 1)
            self.assertEqual(info[0].name, 'prx.xpx')

    def test_get_network_type(self):
        with client.NetworkHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_network_type()
            self.assertEqual(isinstance(info, models.NetworkType), True)

    def test_get_node_info(self):
        with client.NodeHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_node_info()
            self.assertEqual(isinstance(info, models.NodeInfo), True)

    def test_get_node_time(self):
        with client.NodeHTTP(config.ENDPOINT, network_type=config.network_type) as http:
            info = http.get_node_time()
            self.assertEqual(isinstance(info, models.NodeTime), True)
