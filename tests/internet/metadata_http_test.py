from nem2 import client
from nem2 import models
from nem2 import util
from tests import harness
from tests import config
from tests import responses
import os
from binascii import hexlify


class TestMetadataHttp(harness.TestCase):
    def __init__(self, task) -> None:
        super().__init__(task)

        if (task == 'test_account_metadata'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, 100000000)

            self.modifications = [
                models.MetadataModification(models.MetadataModificationType.ADD, models.Field('foo', 'bar')),
                models.MetadataModification(models.MetadataModificationType.ADD, models.Field('foo2', 'bar')),
            ]

            tx = models.ModifyAccountMetadataTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                metadata_type=models.MetadataType.ADDRESS,
                metadata_id=self.alice.address,
                modifications=self.modifications,
            )

            signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.alice)

        elif (task == 'test_mosaic_metadata'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, 1000000000)

            self.mosaic_id = self.create_mosaic(self.alice, 1)

            self.modifications = [
                models.MetadataModification(models.MetadataModificationType.ADD, models.Field('foo', 'bar')),
                models.MetadataModification(models.MetadataModificationType.ADD, models.Field('foo2', 'bar')),
            ]

            tx = models.ModifyMosaicMetadataTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                metadata_type=models.MetadataType.MOSAIC,
                metadata_id=self.mosaic_id,
                modifications=self.modifications,
            )

            signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.alice)

        elif (task == 'test_namespace_metadata'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, 2000000000)

            self.namespace = 'foo' + hexlify(os.urandom(4)).decode('utf-8') + ".bar"
            self.create_namespace(self.alice, self.namespace)

            self.modifications = [
                models.MetadataModification(models.MetadataModificationType.ADD, models.Field('foo', 'bar')),
                models.MetadataModification(models.MetadataModificationType.ADD, models.Field('foo2', 'bar')),
            ]

            tx = models.ModifyNamespaceMetadataTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                metadata_type=models.MetadataType.NAMESPACE,
                metadata_id=models.NamespaceId(self.namespace),
                modifications=self.modifications,
            )

            signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.alice)

        elif (task == 'test_modify_address_metadata_transaction'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, 100000000)

        elif (task == 'test_modify_mosaic_metadata_transaction'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, 1000000000)
            self.mosaic_id = self.create_mosaic(self.alice, 1)

        elif (task == 'test_modify_namespace_metadata_transaction'):
            self.alice = models.Account.generate_new_account(models.NetworkType.MIJIN_TEST, entropy=lambda x: os.urandom(32))
            self.send_funds(config.nemesis, self.alice, 1000000000)
            self.namespace = 'foo' + hexlify(os.urandom(4)).decode('utf-8') + ".bar"
            self.create_namespace(self.alice, self.namespace)

    async def listen(self, account):
        async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
            await listener.confirmed(account.address)
            await listener.status(account.address)

            async for m in listener:
                if (m.channel_name == 'status'):
                    raise Exception(m.message)
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
        # self.assertEqual(tx.mosaics[0].id, config.mosaic_id)
        # self.assertEqual(tx.mosaics[0].amount, amount)

        return tx

    def create_namespace(self, account, namespace):
        namespace = namespace.split(".")

        # Create namespace
        tx = models.RegisterNamespaceTransaction.create_root_namespace(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            namespace_name=namespace[0],
            duration=60
        )

        signed_tx = tx.sign_with(account, config.gen_hash)

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = self.listen(account)
        self.assertEqual(isinstance(tx, models.RegisterNamespaceTransaction), True)
        self.assertEqual(tx.namespace_name, namespace[0])

        if (len(namespace) > 1):
            # Create sub namespace
            tx = models.RegisterNamespaceTransaction.create_sub_namespace(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                namespace_name=namespace[1],
                parent_namespace=namespace[0]
            )

            signed_tx = tx.sign_with(account, config.gen_hash)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(account)
            self.assertEqual(isinstance(tx, models.RegisterNamespaceTransaction), True)
            self.assertEqual(tx.namespace_name, namespace[1])

    def create_mosaic(self, account, nonce):
        # Create mosaic
        nonce = models.MosaicNonce(nonce)
        mosaic_id = models.MosaicId.create_from_nonce(nonce, account)

        tx = models.MosaicDefinitionTransaction.create(
            deadline=models.Deadline.create(),
            network_type=models.NetworkType.MIJIN_TEST,
            nonce=nonce,
            mosaic_id=mosaic_id,
            mosaic_properties=models.MosaicProperties(0x3, 3),
        )

        signed_tx = tx.sign_with(account, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

        with client.TransactionHTTP(responses.ENDPOINT) as http:
            http.announce(signed_tx)

        tx = self.listen(account)
        self.assertEqual(isinstance(tx, models.MosaicDefinitionTransaction), True)
        self.assertEqual(tx.mosaic_id, mosaic_id)

        return mosaic_id

    # TESTS
    def test_modify_address_metadata_transaction(self):
        metadata_key = 'foo' + hexlify(os.urandom(4)).decode('ascii')

        for metadata_modification_type in [models.MetadataModificationType.ADD, models.MetadataModificationType.REMOVE]:
            tx = models.ModifyAccountMetadataTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                metadata_type=models.MetadataType.ADDRESS,
                metadata_id=self.alice.address,
                modifications=[
                    models.MetadataModification(metadata_modification_type, models.Field(metadata_key, 'bar')),
                    models.MetadataModification(metadata_modification_type, models.Field(metadata_key + '2', 'bar')),
                ],
            )

            signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.alice)
            self.assertEqual(isinstance(tx, models.ModifyAccountMetadataTransaction), True)
            self.assertEqual(tx.metadata_id, self.alice.address)
            self.assertEqual(len(tx.modifications) > 0, True)
            self.assertEqual(tx.modifications[0].field.key, metadata_key)
            self.assertEqual(tx.modifications[0].field.value, 'bar')

    def test_modify_mosaic_metadata_transaction(self):
        metadata_key = 'foo' + hexlify(os.urandom(4)).decode('ascii')

        for metadata_modification_type in [models.MetadataModificationType.ADD, models.MetadataModificationType.REMOVE]:
            tx = models.ModifyMosaicMetadataTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                metadata_type=models.MetadataType.MOSAIC,
                metadata_id=self.mosaic_id,
                modifications=[
                    models.MetadataModification(metadata_modification_type, models.Field(metadata_key, 'bar')),
                    models.MetadataModification(metadata_modification_type, models.Field(metadata_key + '2', 'bar')),
                ],
            )

            signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.alice)
            self.assertEqual(isinstance(tx, models.ModifyMosaicMetadataTransaction), True)
            self.assertEqual(tx.metadata_id, self.mosaic_id)
            self.assertEqual(len(tx.modifications) > 0, True)
            self.assertEqual(tx.modifications[0].field.key, metadata_key)
            self.assertEqual(tx.modifications[0].field.value, 'bar')

    def test_modify_namespace_metadata_transaction(self):
        metadata_key = 'foo' + hexlify(os.urandom(4)).decode('ascii')

        for metadata_modification_type in [models.MetadataModificationType.ADD, models.MetadataModificationType.REMOVE]:
            tx = models.ModifyNamespaceMetadataTransaction.create(
                deadline=models.Deadline.create(),
                network_type=models.NetworkType.MIJIN_TEST,
                metadata_type=models.MetadataType.NAMESPACE,
                metadata_id=models.NamespaceId(self.namespace),
                modifications=[
                    models.MetadataModification(metadata_modification_type, models.Field(metadata_key, 'bar')),
                    models.MetadataModification(metadata_modification_type, models.Field(metadata_key + '2', 'bar')),
                ],
            )

            signed_tx = tx.sign_with(self.alice, config.gen_hash, fee_strategy=util.FeeCalculationStrategy.MEDIUM)

            with client.TransactionHTTP(responses.ENDPOINT) as http:
                http.announce(signed_tx)

            tx = self.listen(self.alice)
            self.assertEqual(isinstance(tx, models.ModifyNamespaceMetadataTransaction), True)
            self.assertEqual(tx.metadata_id, models.NamespaceId(self.namespace))
            self.assertEqual(len(tx.modifications) > 0, True)
            self.assertEqual(tx.modifications[0].field.key, metadata_key)
            self.assertEqual(tx.modifications[0].field.value, 'bar')

    def test_account_metadata(self):
        with client.MetadataHTTP(responses.ENDPOINT) as http:
            reply = http.get_account_metadata(self.alice)
            self.assertEqual(isinstance(reply, models.AddressMetadataInfo), True)
            self.assertEqual(len(reply.metadata.flds), 2)
            self.assertEqual(reply.metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply.metadata.flds[1], self.modifications[1].field)

        with client.MetadataHTTP(responses.ENDPOINT) as http:
            reply = http.get_metadata(self.alice.address.plain())
            self.assertEqual(isinstance(reply, models.MetadataInfo), True)
            self.assertEqual(isinstance(reply.metadata, models.AddressMetadata), True)
            self.assertEqual(len(reply.metadata.flds), 2)
            self.assertEqual(reply.metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply.metadata.flds[1], self.modifications[1].field)

        with client.MetadataHTTP(responses.ENDPOINT) as http:
            reply = http.get_metadatas([self.alice.address.plain()])
            self.assertEqual(len(reply) > 0, True)
            self.assertEqual(isinstance(reply[0], models.MetadataInfo), True)
            self.assertEqual(isinstance(reply[0].metadata, models.AddressMetadata), True)
            self.assertEqual(len(reply[0].metadata.flds), 2)
            self.assertEqual(reply[0].metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply[0].metadata.flds[1], self.modifications[1].field)

    def test_mosaic_metadata(self):
        with client.MetadataHTTP(responses.ENDPOINT) as http:
            reply = http.get_mosaic_metadata(self.mosaic_id)
            self.assertEqual(isinstance(reply, models.MosaicMetadataInfo), True)
            self.assertEqual(len(reply.metadata.flds), 2)
            self.assertEqual(reply.metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply.metadata.flds[1], self.modifications[1].field)

        with client.MetadataHTTP(responses.ENDPOINT) as http:
            reply = http.get_metadata(self.mosaic_id.get_id())
            self.assertEqual(isinstance(reply, models.MetadataInfo), True)
            self.assertEqual(isinstance(reply.metadata, models.MosaicMetadata), True)
            self.assertEqual(len(reply.metadata.flds), 2)
            self.assertEqual(reply.metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply.metadata.flds[1], self.modifications[1].field)

        with client.MetadataHTTP(responses.ENDPOINT) as http:
            reply = http.get_metadatas([self.mosaic_id.get_id()])
            self.assertEqual(len(reply) > 0, True)
            self.assertEqual(isinstance(reply[0], models.MetadataInfo), True)
            self.assertEqual(isinstance(reply[0].metadata, models.MosaicMetadata), True)
            self.assertEqual(len(reply[0].metadata.flds), 2)
            self.assertEqual(reply[0].metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply[0].metadata.flds[1], self.modifications[1].field)

    def test_namespace_metadata(self):
        with client.MetadataHTTP(responses.ENDPOINT) as http:
            reply = http.get_namespace_metadata(models.NamespaceId(self.namespace))
            self.assertEqual(isinstance(reply, models.NamespaceMetadataInfo), True)
            self.assertEqual(len(reply.metadata.flds), 2)
            self.assertEqual(reply.metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply.metadata.flds[1], self.modifications[1].field)

        with client.MetadataHTTP(responses.ENDPOINT) as http:
            reply = http.get_metadata(models.NamespaceId(self.namespace).get_id())
            self.assertEqual(isinstance(reply, models.MetadataInfo), True)
            self.assertEqual(isinstance(reply.metadata, models.NamespaceMetadata), True)
            self.assertEqual(len(reply.metadata.flds), 2)
            self.assertEqual(reply.metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply.metadata.flds[1], self.modifications[1].field)

        with client.MetadataHTTP(responses.ENDPOINT) as http:
            reply = http.get_metadatas([models.NamespaceId(self.namespace).get_id()])
            self.assertEqual(len(reply) > 0, True)
            self.assertEqual(isinstance(reply[0], models.MetadataInfo), True)
            self.assertEqual(isinstance(reply[0].metadata, models.NamespaceMetadata), True)
            self.assertEqual(len(reply[0].metadata.flds), 2)
            self.assertEqual(reply[0].metadata.flds[0], self.modifications[0].field)
            self.assertEqual(reply[0].metadata.flds[1], self.modifications[1].field)
