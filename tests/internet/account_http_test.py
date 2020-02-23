from xpxchain import client
from xpxchain import models
from xpxchain import util
from tests import harness
from tests import config
from tests import responses
from tests.helper import listen, listen_bonded, send_funds, prepare
import os
import typing
import asyncio
from binascii import hexlify

_1 = config.divisibility * 1
_10 = _1 * 10
_100 = _1 * 100
_1000 = _1 * 1000


class TestAccountHttp(harness.TestCase):

    t1: typing.Sequence[models.Account]
    t2: typing.Sequence[models.Account]
    t3: typing.Sequence[models.Account]
    t4: typing.Sequence[models.Account]
    hashes: typing.Sequence[str] = []

    @classmethod
    def setUpClass(cls):
        
        cls.t1 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(2)]
        cls.t2 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(8)]
        cls.t3 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(0)]
        cls.t4 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(1)]

        loop = asyncio.get_event_loop()
        cls.hashes = loop.run_until_complete(prepare(
            [send_funds(config.tester, account, _1) for account in cls.t1]
            + [send_funds(config.tester, account, _10) for account in cls.t2]
            + [send_funds(config.tester, account, _100) for account in cls.t3]
            + [send_funds(config.tester, account, _1000) for account in cls.t4]
        ))

    # TESTS

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

        signed_tx = tx.sign_transaction_with_cosignatories(multisig, config.gen_hash, [alice, bob], fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(multisig)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

        with client.AccountHTTP(config.ENDPOINT) as http:
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

        signed_tx = tx.sign_transaction_with_cosignatories(multisig, config.gen_hash, [alice, bob], fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(multisig)
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

        signed_tx = tx.sign_transaction_with_cosignatories(multisig2, config.gen_hash, [alice, bob, mike], fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(multisig2)
        self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

        with client.AccountHTTP(config.ENDPOINT) as http:
            info = http.get_multisig_account_graph_info(multisig.address)
            self.assertEqual(isinstance(info, models.MultisigAccountGraphInfo), True)

    async def test_account_names(self):
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

        namespace_name = namespace_name + ".bar"

        # Link address alias
        tx = models.AddressAliasTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            max_fee=1,
            action_type=models.AliasActionType.LINK,
            namespace_id=models.NamespaceId(namespace_name),
            address=alice.address
        )

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)
        self.assertEqual(isinstance(tx, models.AddressAliasTransaction), True)
        self.assertEqual(tx.action_type, models.AliasActionType.LINK)
        self.assertEqual(tx.address, alice.address)

        with client.AccountHTTP(config.ENDPOINT) as http:
            info = http.get_account_names([alice.address])
            self.assertEqual(len(info), 1)
            self.assertEqual(isinstance(info[0], models.AccountNames), True)
            self.assertEqual(len(info[0].names), 1)
            self.assertEqual(info[0].names[0], namespace_name)

    async def test_account_transactions(self):
        alice = self.t1.pop()

        with client.AccountHTTP(config.ENDPOINT) as http:
            info = http.transactions(alice)
            self.assertEqual(len(info), 1)
            self.assertEqual(len(info[0].mosaics), 1)
            self.assertEqual(info[0].mosaics[0], models.Mosaic(config.mosaic_id, _1))
            self.assertEqual(info[0].signer.public_key, config.tester.public_key.upper())

    async def test_incoming_transactions(self):
        alice = self.t1.pop()
        
        with client.AccountHTTP(config.ENDPOINT) as http:
            info = http.incoming_transactions(alice)
            self.assertEqual(len(info), 1)
            self.assertEqual(len(info[0].mosaics), 1)
            self.assertEqual(info[0].mosaics[0], models.Mosaic(config.mosaic_id, _1))
            self.assertEqual(info[0].signer.public_key, config.tester.public_key.upper())

    async def test_outgoing_transactions(self):
        alice = self.t2.pop()         
        bob = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))

        await send_funds(alice, bob, _1)
        
        with client.AccountHTTP(config.ENDPOINT) as http:
            info = http.outgoing_transactions(alice)
            self.assertEqual(len(info), 1)
            self.assertEqual(len(info[0].mosaics), 1)
            self.assertEqual(info[0].mosaics[0], models.Mosaic(config.mosaic_id, _1))
            self.assertEqual(info[0].recipient, bob.address)

    async def test_account_properties(self):
        alice = self.t2.pop()
        bob = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))
        mike = models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32))
        pete = self.t2.pop()

        # ALLOW_ADDRESS
        tx = models.ModifyAccountPropertyAddressTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            property_type=models.PropertyType.ALLOW_ADDRESS,
            modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, bob.address)]
        )

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)

        # ALLOW_MOSAIC
        tx = models.ModifyAccountPropertyMosaicTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            property_type=models.PropertyType.ALLOW_MOSAIC,
            modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, config.mosaic_id)]
        )

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)

        # BLOCK_ADDRESS
        tx = models.ModifyAccountPropertyAddressTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            property_type=models.PropertyType.BLOCK_ADDRESS,
            modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, bob.address)]
        )

        signed_tx = tx.sign_with(pete, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(pete)

        # BLOCK_MOSAIC
        tx = models.ModifyAccountPropertyMosaicTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            property_type=models.PropertyType.BLOCK_MOSAIC,
            modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, config.mosaic_id)]
        )

        signed_tx = tx.sign_with(pete, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(pete)

        # BLOCK_TRANSACTION
        tx = models.ModifyAccountPropertyEntityTypeTransaction.create(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            property_type=models.PropertyType.BLOCK_TRANSACTION,
            modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, models.TransactionType.AGGREGATE_COMPLETE)]
        )

        signed_tx = tx.sign_with(pete, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(pete)

        with client.AccountHTTP(config.ENDPOINT) as http:
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
        with client.AccountHTTP(config.ENDPOINT) as http:
            info = http.aggregate_bonded_transactions(alice)
            self.assertEqual(len(info), 0)
        
    async def test_unconfirmed_transactions(self):
        alice = self.t2.pop()

        # TODO: Add unconfirmed transaction
        with client.AccountHTTP(config.ENDPOINT) as http:
            info = http.unconfirmed_transactions(alice)
            self.assertEqual(len(info), 0)
        
    async def test_get_account_info(self):
        with client.AccountHTTP(config.ENDPOINT) as http:
            info = http.get_account_info(config.tester.address)
            self.assertEqual(info.public_key, config.tester.public_key.upper()),
    
    async def test_get_accountis_info(self):
        with client.AccountHTTP(config.ENDPOINT) as http:
            info = http.get_accounts_info([config.tester.address])
            self.assertEqual(len(info), 1)
            self.assertEqual(info[0].public_key, config.tester.public_key.upper())
