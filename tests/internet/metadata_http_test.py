from xpxchain import client
from xpxchain import models
from xpxchain import util
from tests import harness
from tests import config
from tests import responses
import os
from binascii import hexlify
from tests.helper import listen, listen_bonded, send_funds, prepare
import asyncio
import typing

_1 = config.divisibility * 1
_10 = _1 * 10
_100 = _1 * 100
_1000 = _1 * 1000

async def create_namespace(account, namespace):
    namespace = namespace.split(".")

    tx = models.RegisterNamespaceTransaction.create_root_namespace(
        deadline=models.Deadline.create(),
        network_type=config.network_type,
        namespace_name=namespace[0],
        duration=60
    )

    signed_tx = tx.sign_with(account, config.gen_hash)

    with client.TransactionHTTP(config.ENDPOINT) as http:
        http.announce(signed_tx)

    tx = await listen(account)

    if (len(namespace) > 1):
        # Create sub namespace
        tx = models.RegisterNamespaceTransaction.create_sub_namespace(
            deadline=models.Deadline.create(),
            network_type=config.network_type,
            namespace_name=namespace[1],
            parent_namespace=namespace[0]
        )

        signed_tx = tx.sign_with(account, config.gen_hash)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(account)

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

    signed_tx = tx.sign_with(account, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

    with client.TransactionHTTP(config.ENDPOINT) as http:
        http.announce(signed_tx)

    tx = await listen(account)

    return mosaic_id


class TestMetadataHttp(harness.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.t1 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(0)]
        cls.t2 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(2)]
        cls.t3 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(0)]
        cls.t4 = [models.Account.generate_new_account(config.network_type, entropy=lambda x: os.urandom(32)) for i in range(4)]

        loop = asyncio.get_event_loop()
        cls.hashes = loop.run_until_complete(prepare(
            [send_funds(config.tester, account, _1) for account in cls.t1]
            + [send_funds(config.tester, account, _10) for account in cls.t2]
            + [send_funds(config.tester, account, _100) for account in cls.t3]
            + [send_funds(config.tester, account, _1000) for account in cls.t4]
        ))

    # TESTS
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

            signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(config.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = await listen(alice)
            self.assertEqual(isinstance(tx, models.ModifyAccountMetadataTransaction), True)
            self.assertEqual(tx.metadata_id, alice.address)
            self.assertEqual(len(tx.modifications) > 0, True)
            self.assertEqual(tx.modifications[0].field.key, metadata_key)
            self.assertEqual(tx.modifications[0].field.value, 'bar')

    async def test_modify_mosaic_metadata_transaction(self):
        alice = self.t4.pop()

        mosaic_id = await create_mosaic(alice, 1)
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

            signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(config.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = await listen(alice)
            self.assertEqual(isinstance(tx, models.ModifyMosaicMetadataTransaction), True)
            self.assertEqual(tx.metadata_id, mosaic_id)
            self.assertEqual(len(tx.modifications) > 0, True)
            self.assertEqual(tx.modifications[0].field.key, metadata_key)
            self.assertEqual(tx.modifications[0].field.value, 'bar')

    async def test_modify_namespace_metadata_transaction(self):
        alice = self.t4.pop()

        namespace = 'foo' + hexlify(os.urandom(4)).decode('utf-8') + ".bar"
        await create_namespace(alice, namespace)

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

            signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(config.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = await listen(alice)
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

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)
        
        with client.MetadataHTTP(config.ENDPOINT) as http:
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

        mosaic_id = await create_mosaic(alice, 1)

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

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)

        with client.MetadataHTTP(config.ENDPOINT) as http:
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
        alice = self.t4.pop()

        self.namespace = 'foo' + hexlify(os.urandom(4)).decode('utf-8') + ".bar"
        await create_namespace(alice, self.namespace)

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

        signed_tx = tx.sign_with(alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(config.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = await listen(alice)
        
        with client.MetadataHTTP(config.ENDPOINT) as http:
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
