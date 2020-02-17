from xpxchain import client
from xpxchain import models
from xpxchain import util
from tests import harness
from tests import config
from tests import responses
import os
from binascii import hexlify


class Error(Exception):
    pass


@harness.http_test_case({
    'clients': (client.AccountHTTP, client.AsyncAccountHTTP),
    'tests': [
        {
            # /account/{accountId}
            'name': 'test_get_account_info',
            'params': [config.nemesis.address],
            'method': 'get_account_info',
            'validation': [
                lambda x: (x.public_key, config.nemesis.public_key.upper()),
            ]
        },
        {
            # /account
            'name': 'test_get_accounts_info',
            'params': [[config.nemesis.address]],
            'method': 'get_accounts_info',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].public_key, config.nemesis.public_key.upper()),
            ]
        },
        {
            # /account/{publicKey}/transaction/unconfirmed
            'name': 'test_unconfirmed_transactions',
            'params': [config.nemesis],
            'method': 'unconfirmed_transactions',
            'validation': [
                lambda x: (len(x), 0),
            ],
        },
        {
            # /account/{publicKey}/transaction/partial
            'name': 'test_aggregate_bonded_transactions',
            'params': [config.nemesis],
            'method': 'aggregate_bonded_transactions',
            'validation': [
                lambda x: (len(x), 0),
            ],
        },
    ],
})
class TestAccountHttp(harness.TestCase):
    def __init__(self, task) -> None:
        super().__init__(task)

        if (task == 'test_account_transactions'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, 100000000)

        elif (task == 'test_incoming_transactions'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, 100000000)

        elif (task == 'test_outgoing_transactions'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.bob = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, 100000000)
            self.send_funds(self.alice, self.bob, 10000000)

        elif (task == 'test_multisig_account_info'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.bob = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.multisig = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))

            nemesis_to_bob = models.TransferTransaction.create(
                deadline=models.Deadline.create(),
                recipient=self.bob.address,
                mosaics=[models.Mosaic(config.mosaic_id, 10000000)],
                network_type=models.NetworkType.MIJIN_TEST,
            )

            nemesis_to_alice = models.TransferTransaction.create(
                deadline=models.Deadline.create(),
                recipient=self.alice.address,
                mosaics=[models.Mosaic(config.mosaic_id, 10000000)],
                network_type=models.NetworkType.MIJIN_TEST,
            )

            nemesis_to_multisig = models.TransferTransaction.create(
                deadline=models.Deadline.create(),
                recipient=self.multisig.address,
                mosaics=[models.Mosaic(config.mosaic_id, 10000000)],
                network_type=models.NetworkType.MIJIN_TEST,
            )

            tx = models.AggregateTransaction.create_complete(
                deadline=models.Deadline.create(),
                inner_transactions=[nemesis_to_alice.to_aggregate(config.nemesis), nemesis_to_bob.to_aggregate(config.nemesis), nemesis_to_multisig.to_aggregate(config.nemesis)],
                network_type=models.NetworkType.MIJIN_TEST,
            )

            signed_tx = tx.sign_transaction_with_cosignatories(config.nemesis, config. gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.alice)
            self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

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

        elif (task == 'test_multisig_account_graph_info'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.bob = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.mike = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.multisig = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.multisig2 = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))

            nemesis_to_bob = models.TransferTransaction.create(
                deadline=models.Deadline.create(),
                recipient=self.bob.address,
                mosaics=[models.Mosaic(config.mosaic_id, 100000000)],
                network_type=models.NetworkType.MIJIN_TEST,
            )

            nemesis_to_alice = models.TransferTransaction.create(
                deadline=models.Deadline.create(),
                recipient=self.alice.address,
                mosaics=[models.Mosaic(config.mosaic_id, 100000000)],
                network_type=models.NetworkType.MIJIN_TEST,
            )

            nemesis_to_mike = models.TransferTransaction.create(
                deadline=models.Deadline.create(),
                recipient=self.mike.address,
                mosaics=[models.Mosaic(config.mosaic_id, 100000000)],
                network_type=models.NetworkType.MIJIN_TEST,
            )

            nemesis_to_multisig = models.TransferTransaction.create(
                deadline=models.Deadline.create(),
                recipient=self.multisig.address,
                mosaics=[models.Mosaic(config.mosaic_id, 100000000)],
                network_type=models.NetworkType.MIJIN_TEST,
            )

            nemesis_to_multisig2 = models.TransferTransaction.create(
                deadline=models.Deadline.create(),
                recipient=self.multisig2.address,
                mosaics=[models.Mosaic(config.mosaic_id, 100000000)],
                network_type=models.NetworkType.MIJIN_TEST,
            )

            tx = models.AggregateTransaction.create_complete(
                deadline=models.Deadline.create(),
                inner_transactions=[
                    nemesis_to_alice.to_aggregate(config.nemesis),
                    nemesis_to_bob.to_aggregate(config.nemesis),
                    nemesis_to_mike.to_aggregate(config.nemesis),
                    nemesis_to_multisig.to_aggregate(config.nemesis),
                    nemesis_to_multisig2.to_aggregate(config.nemesis),
                ],
                network_type=models.NetworkType.MIJIN_TEST,
            )

            signed_tx = tx.sign_transaction_with_cosignatories(config.nemesis, config. gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.alice)
            self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

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

            change_to_multisig = models.ModifyMultisigAccountTransaction.create(
                deadline=models.Deadline.create(),
                min_approval_delta=2,
                min_removal_delta=1,
                modifications=[
                    models.MultisigCosignatoryModification.create(self.mike, models.MultisigCosignatoryModificationType.ADD),
                    models.MultisigCosignatoryModification.create(self.multisig, models.MultisigCosignatoryModificationType.ADD),
                ],
                network_type=models.NetworkType.MIJIN_TEST,
            )

            tx = models.AggregateTransaction.create_complete(
                deadline=models.Deadline.create(),
                inner_transactions=[change_to_multisig.to_aggregate(self.multisig2)],
                network_type=models.NetworkType.MIJIN_TEST,
            )

            signed_tx = tx.sign_transaction_with_cosignatories(self.multisig2, config.gen_hash, [self.alice, self.bob, self.mike], fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.multisig2)
            self.assertEqual(isinstance(tx, models.AggregateTransaction), True)

        elif (task == 'test_account_names'):
            self.mike = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.mike, 1000000000)
            namespace_name = 'foo' + hexlify(os.urandom(4)).decode('utf-8')

            # Create namespace
            tx = models.RegisterNamespaceTransaction.create_root_namespace(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                namespace_name=namespace_name,
                duration=60
            )

            signed_tx = tx.sign_with(self.mike, config. gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

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

            signed_tx = tx.sign_with(self.mike, config. gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.mike)
            self.assertEqual(isinstance(tx, models.RegisterNamespaceTransaction), True)
            self.assertEqual(tx.namespace_name, 'bar')

            self.mikes_namespace = namespace_name + ".bar"

            # Link address alias
            tx = models.AddressAliasTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                max_fee=1,
                action_type=models.AliasActionType.LINK,
                namespace_id=models.NamespaceId(self.mikes_namespace),
                address=self.mike.address
            )

            signed_tx = tx.sign_with(self.mike, config. gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.mike)
            self.assertEqual(isinstance(tx, models.AddressAliasTransaction), True)
            self.assertEqual(tx.action_type, models.AliasActionType.LINK)
            self.assertEqual(tx.address, self.mike.address)

        elif (task == 'test_account_properties'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.bob = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.mike = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, 100000000)
            self.send_funds(config.nemesis, self.bob, 100000000)

            # ALLOW_ADDRESS
            tx = models.ModifyAccountPropertyAddressTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                property_type=models.PropertyType.ALLOW_ADDRESS,
                modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, self.mike.address)]
            )

            signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.alice)

            # ALLOW_MOSAIC
            tx = models.ModifyAccountPropertyMosaicTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                property_type=models.PropertyType.ALLOW_MOSAIC,
                modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, config.mosaic_id)]
            )

            signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.alice)

            # BLOCK_ADDRESS
            tx = models.ModifyAccountPropertyAddressTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                property_type=models.PropertyType.BLOCK_ADDRESS,
                modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, self.mike.address)]
            )

            signed_tx = tx.sign_with(self.bob, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.bob)

            # BLOCK_MOSAIC
            tx = models.ModifyAccountPropertyMosaicTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                property_type=models.PropertyType.BLOCK_MOSAIC,
                modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, config.mosaic_id)]
            )

            signed_tx = tx.sign_with(self.bob, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.bob)

            # BLOCK_TRANSACTION
            tx = models.ModifyAccountPropertyEntityTypeTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                property_type=models.PropertyType.BLOCK_TRANSACTION,
                modifications=[models.AccountPropertyModification(models.PropertyModificationType.ADD, models.TransactionType.AGGREGATE_COMPLETE)]
            )

            signed_tx = tx.sign_with(self.bob, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.bob)

    async def listen(self, account):
        async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
            await listener.confirmed(account.address)
            await listener.status(account.address)

            async for m in listener:
                if (m.channel_name == 'status'):
                    raise Error(m.message)
                elif (m.channel_name == 'confirmedAdded'):
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

        return tx

    # TESTS

    def test_multisig_account_info(self):
        with client.AccountHTTP(responses.ENDPOINT) as http:
            info = http.get_multisig_account_info(self.multisig.address)
            self.assertEqual(isinstance(info, models.MultisigAccountInfo), True)

    def test_multisig_account_graph_info(self):
        with client.AccountHTTP(responses.ENDPOINT) as http:
            info = http.get_multisig_account_graph_info(self.multisig.address)
            self.assertEqual(isinstance(info, models.MultisigAccountGraphInfo), True)

    def test_account_names(self):
        with client.AccountHTTP(responses.ENDPOINT) as http:
            info = http.get_account_names([self.mike.address])
            self.assertEqual(len(info), 1)
            self.assertEqual(isinstance(info[0], models.AccountNames), True)
            self.assertEqual(len(info[0].names), 1)
            self.assertEqual(info[0].names[0], self.mikes_namespace)

    def test_account_transactions(self):
        with client.AccountHTTP(responses.ENDPOINT) as http:
            info = http.transactions(self.alice)
            self.assertEqual(len(info), 1)
            self.assertEqual(len(info[0].mosaics), 1)
            self.assertEqual(info[0].mosaics[0], models.Mosaic(config.mosaic_id, 100000000))
            self.assertEqual(info[0].signer.public_key, config.nemesis.public_key.upper())

    def test_incoming_transactions(self):
        with client.AccountHTTP(responses.ENDPOINT) as http:
            info = http.incoming_transactions(self.alice)
            self.assertEqual(len(info), 1)
            self.assertEqual(len(info[0].mosaics), 1)
            self.assertEqual(info[0].mosaics[0], models.Mosaic(config.mosaic_id, 100000000))
            self.assertEqual(info[0].signer.public_key, config.nemesis.public_key.upper())

    def test_outgoing_transactions(self):
        with client.AccountHTTP(responses.ENDPOINT) as http:
            info = http.outgoing_transactions(self.alice)
            self.assertEqual(len(info), 1)
            self.assertEqual(len(info[0].mosaics), 1)
            self.assertEqual(info[0].mosaics[0], models.Mosaic(config.mosaic_id, 10000000))
            self.assertEqual(info[0].recipient, self.bob.address)

    def test_account_properties(self):
        with client.AccountHTTP(responses.ENDPOINT) as http:
            info = http.get_account_properties(self.alice.address)
            self.assertEqual(len(info.properties), 3)
            self.assertEqual(info.properties[0].property_type, models.PropertyType.ALLOW_ADDRESS)
            self.assertEqual(len(info.properties[0].values), 1)
            self.assertEqual(info.properties[0].values[0], self.mike.address)
            self.assertEqual(info.properties[1].property_type, models.PropertyType.ALLOW_MOSAIC)
            self.assertEqual(len(info.properties[1].values), 1)
            self.assertEqual(info.properties[1].values[0], config.mosaic_id)
            self.assertEqual(info.properties[2].property_type, models.PropertyType.BLOCK_TRANSACTION)
            self.assertEqual(len(info.properties[2].values), 0)

        with client.AccountHTTP(responses.ENDPOINT) as http:
            info = http.get_account_properties(self.bob.address)
            self.assertEqual(len(info.properties), 3)
            self.assertEqual(info.properties[0].property_type, models.PropertyType.BLOCK_ADDRESS)
            self.assertEqual(len(info.properties[0].values), 1)
            self.assertEqual(info.properties[0].values[0], self.mike.address)
            self.assertEqual(info.properties[1].property_type, models.PropertyType.BLOCK_MOSAIC)
            self.assertEqual(len(info.properties[1].values), 1)
            self.assertEqual(info.properties[1].values[0], config.mosaic_id)
            self.assertEqual(info.properties[2].property_type, models.PropertyType.BLOCK_TRANSACTION)
            self.assertEqual(len(info.properties[2].values), 1)
            self.assertEqual(info.properties[2].values[0], models.TransactionType.AGGREGATE_COMPLETE)

        with client.AccountHTTP(responses.ENDPOINT) as http:
            info = http.get_accounts_properties([self.alice.address, self.bob.address])
            self.assertEqual(len(info), 2)

            for i in info:
                if (i.address == self.alice.address):
                    alice = i
                elif (i.address == self.bob.address):
                    bob = i
                else:
                    raise Exception(f'Unknown address{i.address.address}')

            self.assertEqual(len(alice.properties), 3)
            self.assertEqual(alice.properties[0].property_type, models.PropertyType.ALLOW_ADDRESS)
            self.assertEqual(len(alice.properties[0].values), 1)
            self.assertEqual(alice.properties[0].values[0], self.mike.address)
            self.assertEqual(alice.properties[1].property_type, models.PropertyType.ALLOW_MOSAIC)
            self.assertEqual(len(alice.properties[1].values), 1)
            self.assertEqual(alice.properties[1].values[0], config.mosaic_id)
            self.assertEqual(alice.properties[2].property_type, models.PropertyType.BLOCK_TRANSACTION)
            self.assertEqual(len(alice.properties[2].values), 0)
            self.assertEqual(len(alice.properties), 3)

            self.assertEqual(bob.properties[0].property_type, models.PropertyType.BLOCK_ADDRESS)
            self.assertEqual(len(bob.properties[0].values), 1)
            self.assertEqual(bob.properties[0].values[0], self.mike.address)
            self.assertEqual(bob.properties[1].property_type, models.PropertyType.BLOCK_MOSAIC)
            self.assertEqual(len(bob.properties[1].values), 1)
            self.assertEqual(bob.properties[1].values[0], config.mosaic_id)
            self.assertEqual(bob.properties[2].property_type, models.PropertyType.BLOCK_TRANSACTION)
            self.assertEqual(len(bob.properties[2].values), 1)
            self.assertEqual(bob.properties[2].values[0], models.TransactionType.AGGREGATE_COMPLETE)
