import datetime
import random

from nem2 import util
from nem2 import models
from tests import harness


def psuedo_entropy(size: int) -> bytes:
    return bytes([random.randint(0, 255) for _ in range(size)])


class TestAddressAliasTransaction(harness.TestCase):

    def setUp(self):
        self.deadline = models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57))
        self.action_type = models.AliasActionType.LINK
        self.namespace_id = models.NamespaceId(0x88B64C3BE2F47144)
        self.address = models.Address('SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54')
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transaction = models.AddressAliasTransaction.create(
            deadline=self.deadline,
            action_type=self.action_type,
            namespace_id=self.namespace_id,
            address=self.address,
            network_type=self.network_type,
        )
        private_key = "97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca"
        self.signer = models.Account.create_from_private_key(private_key, self.network_type)
        self.catbuffer = '9a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001904e420000000000000000f1b4815c00000000004471f4e23b4cb68890fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc'
        self.payload = '9a000000102e9c68fe9cbaa5d1d27ad35f9e386b42c265749be0e27182b8a9ebf18a0357332ef4ee350b648ea00437790c70471959b9334aea2e2e89356d52613fd385021b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e420000000000000000f1b4815c00000000004471f4e23b4cb68890fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc'
        self.hash = 'a45d14bae72e64ce94e3cb88927cce8d4048cf08a11ed13936af58efb614c0d4'
        self.embedded = '4a0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e42004471f4e23b4cb68890fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc'

    def test_init(self):
        self.assertEqual(self.transaction.deadline, self.deadline)
        self.assertEqual(self.transaction.action_type, self.action_type)
        self.assertEqual(self.transaction.namespace_id, self.namespace_id)
        self.assertEqual(self.transaction.address, self.address)
        self.assertEqual(self.transaction.network_type, self.network_type)

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.transaction.__dict__

    def test_catbuffer(self):
        catbuffer = self.transaction.to_catbuffer()
        self.assertEqual(self.catbuffer, util.hexlify(catbuffer))
        self.assertEqual(self.transaction, models.Transaction.from_catbuffer(catbuffer))

    def test_dto(self):
        # TODO(ahuszagh) Confirm...
        dto = self.transaction.to_dto()
        # TODO(ahuszagh)
        #   Is this right?
        #   Restore when I get a message on slack.
        #   https://nem2.slack.com/archives/CEZKUE4KB/p1553097806138700?thread_ts=1553095634.133900&cid=CEZKUE4KB
        # self.assertEqual(self.dto, dto)
        # self.assertEqual(self.transaction, models.Transaction.from_dto(dto))

    def test_sign_with(self):
        signed_transaction = self.transaction.sign_with(self.signer)
        self.assertEqual(signed_transaction.payload, self.payload)
        self.assertEqual(signed_transaction.hash, self.hash)
        self.assertEqual(signed_transaction.signer, self.signer.public_key)
        self.assertEqual(signed_transaction.type, models.TransactionType.ADDRESS_ALIAS)
        self.assertEqual(signed_transaction.network_type, self.signer.network_type)

    def test_to_aggregate(self):
        inner = self.transaction.to_aggregate(self.signer.public_account)
        catbuffer = inner.to_catbuffer()
        self.assertEqual(self.embedded, util.hexlify(catbuffer))

        with self.assertRaises(TypeError):
            inner.__dict__

    def test_dataclasses(self):
        self.assertEqual(self.transaction, self.transaction.replace())
        self.assertIsInstance(self.transaction.asdict(), dict)
        self.assertIsInstance(self.transaction.astuple(), tuple)
        self.assertIsInstance(self.transaction.fields(), tuple)


class TestAggregateTransactionCosignature(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.signature = '5780c8df9d46ba2bcf029dcc5d3bf55fe1cb5be7abcf30387c4637ddedfc2152703ca0ad95f21bb9b942f3cc52fcfc2064c7b84cf60d1a9e69195f1943156c07'
        self.public_key = 'a5f82ec8ebb341427b6785c8111906cd0df18838fb11b51ce0e18b5e79dff630'
        self.signer = models.PublicAccount.create_from_public_key(self.public_key, self.network_type)
        self.cosignature = models.AggregateTransactionCosignature(self.signature, self.signer)
        self.dto = {
            'signature': self.signature,
            'signer': self.public_key,
        }
        self.catbuffer = (
            util.unhexlify(self.public_key)
            + util.unhexlify(self.signature)
        )

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.cosignature.__dict__

    def test_to_dto(self):
        self.assertEqual(self.cosignature.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.cosignature, models.AggregateTransactionCosignature.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.cosignature.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.cosignature, models.AggregateTransactionCosignature.from_catbuffer(self.catbuffer, self.network_type))

    def test_dataclasses(self):
        self.assertEqual(self.cosignature, self.cosignature.replace())
        self.assertIsInstance(self.cosignature.asdict(), dict)
        self.assertIsInstance(self.cosignature.astuple(), tuple)
        self.assertIsInstance(self.cosignature.fields(), tuple)


class TestAggregateTransactionInfo(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transaction_info = models.AggregateTransactionInfo(
            height=18160,
            index=0,
            id="5A0069D83F17CF0001777E56",
            aggregate_hash="3D28C804EDD07D5A728E5C5FFEC01AB07AFA5766AE6997B38526D36015A4D006",
            aggregate_id="5A0069D83F17CF0001777E55",
        )
        self.dto = {
            "height": [18160, 0],
            "aggregateHash": "3D28C804EDD07D5A728E5C5FFEC01AB07AFA5766AE6997B38526D36015A4D006",
            "aggregateId": "5A0069D83F17CF0001777E55",
            "index": 0,
            "id": "5A0069D83F17CF0001777E56"
        }

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.transaction_info.__dict__

    def test_to_dto(self):
        self.assertEqual(self.transaction_info.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.transaction_info, models.AggregateTransactionInfo.from_dto(self.dto, self.network_type))

    def test_dataclasses(self):
        self.assertEqual(self.transaction_info, self.transaction_info.replace())
        self.assertIsInstance(self.transaction_info.asdict(), dict)
        self.assertIsInstance(self.transaction_info.astuple(), tuple)
        self.assertIsInstance(self.transaction_info.fields(), tuple)


class TestAliasTransaction(harness.TestCase):
    pass        # TODO(ahuszagh) Implement


class TestCosignatureSignedTransaction(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.parent_hash = '671653C94E2254F2A23EFEDB15D67C38332AED1FBD24B063C0A8E675582B6A96'
        self.signature = '939673209A13FF82397578D22CC96EB8516A6760C894D9B7535E3A1E068007B9255CFA9A914C97142A7AE18533E381C846B69D2AE0D60D1DC8A55AD120E2B606'
        self.signer = '7681ED5023141D9CDCF184E5A7B60B7D466739918ED5DA30F7E71EA7B86EFF2D'
        self.cosignature = models.CosignatureSignedTransaction(self.parent_hash, self.signature, self.signer)
        self.dto = {
            'parentHash': self.parent_hash,
            'signature': self.signature,
            'signer': self.signer,
        }

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.cosignature.__dict__

    def test_to_dto(self):
        self.assertEqual(self.cosignature.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.cosignature, models.CosignatureSignedTransaction.from_dto(self.dto, self.network_type))

    def test_dataclasses(self):
        self.assertEqual(self.cosignature, self.cosignature.replace())
        self.assertIsInstance(self.cosignature.asdict(), dict)
        self.assertIsInstance(self.cosignature.astuple(), tuple)
        self.assertIsInstance(self.cosignature.fields(), tuple)


class TestDeadline(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.datetime = datetime.datetime(2019, 3, 8, 0, 18, 57)
        self.deadline = models.Deadline(self.datetime)
        self.dto = [1552004337, 0]
        self.catbuffer = b'\xf1\xb4\x81\\\x00\x00\x00\x00'

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.deadline.__dict__

    def test_create(self):
        with self.assertRaises(ValueError):
            models.Deadline.create(0)
        with self.assertRaises(ValueError):
            models.Deadline.create(-1)
        with self.assertRaises(ValueError):
            models.Deadline.create(24, models.ChronoUnit.HOURS)

        models.Deadline.create(2000, models.ChronoUnit.SECONDS)
        models.Deadline.create(200, models.ChronoUnit.MINUTES)
        models.Deadline.create(23, models.ChronoUnit.HOURS)

    def test_to_dto(self):
        self.assertEqual(self.deadline.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.deadline, models.Deadline.from_dto(self.dto, self.network_type))

    def test_dataclasses(self):
        self.assertEqual(self.deadline, self.deadline.replace())
        self.assertIsInstance(self.deadline.asdict(), dict)
        self.assertIsInstance(self.deadline.astuple(), tuple)
        self.assertIsInstance(self.deadline.fields(), tuple)


class TestHashType(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.digest_64 = (
            models.HashType.SHA3_256,
            models.HashType.KECCAK_256,
            models.HashType.HASH_256
        )
        self.digest_40 = (models.HashType.HASH_160,)
        self.hash = models.HashType.SHA3_256
        self.dto = 0
        self.catbuffer = b'\x00'

    def test_validate(self):
        hash_40 = util.hexlify(psuedo_entropy(20))
        hash_64 = util.hexlify(psuedo_entropy(32))

        for enum in self.digest_64:
            self.assertFalse(enum.validate(hash_40))
            self.assertTrue(enum.validate(hash_64))

        for enum in self.digest_40:
            self.assertTrue(enum.validate(hash_40))
            self.assertFalse(enum.validate(hash_64))

        hash_40 = hash_40[:-1] + 'x'
        hash_64 = hash_64[:-1] + 'x'

        for enum in self.digest_64:
            self.assertFalse(enum.validate(hash_40))
            self.assertFalse(enum.validate(hash_64))

        for enum in self.digest_40:
            self.assertFalse(enum.validate(hash_40))
            self.assertFalse(enum.validate(hash_64))

    def test_to_dto(self):
        self.assertEqual(self.hash.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.hash, models.HashType.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.hash.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.hash, models.HashType.from_catbuffer(self.catbuffer, self.network_type))


class TestInnnerTransaction(harness.TestCase):

    def test_catbuffer_size_shared(self):
        self.assertEqual(models.InnerTransaction.catbuffer_size_shared(), 40)

    def test_from_catbuffer(self):
        network_type = models.NetworkType.MIJIN_TEST
        private_key = "97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca"
        transactions = [
            (models.TransactionType.ADDRESS_ALIAS, '4a0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e42004471f4e23b4cb68890fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc'),
            (models.TransactionType.MOSAIC_ALIAS, '390000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e43004471f4e23b4cb688a6c03b484fd6f72f'),
            (models.TransactionType.SECRET_PROOF, '6b0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501905242009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'),
            (models.TransactionType.TRANSFER, '600000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550390544190fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0c000148656c6c6f20776f726c64210500000000000000e803000000000000'),
        ]

        for type, payload in transactions:
            transaction = models.InnerTransaction.from_catbuffer(payload)
            self.assertEqual(transaction.type, type)


class TestMessage(harness.TestCase):

    def test_create(self):
        with self.assertRaises(NotImplementedError):
            models.Message.create(b'Hello world!')

    def test_dto(self):
        dto = {'payload': util.hexlify(b'Hello world!'), 'type': 0}
        with self.assertRaises(NotImplementedError):
            models.Message.from_dto(dto, models.NetworkType.MIJIN_TEST)


class TestMessageType(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.plain = models.MessageType.PLAIN
        self.dto = 0
        self.catbuffer = b'\x00'

    def test_description(self):
        self.assertEqual(self.plain.description(), 'Plain message.')

    def test_to_dto(self):
        self.assertEqual(self.plain.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.plain, models.MessageType.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.plain.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.plain, models.MessageType.from_catbuffer(self.catbuffer, self.network_type))


class TestMosaicAliasTransaction(harness.TestCase):

    def setUp(self):
        self.deadline = models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57))
        self.action_type = models.AliasActionType.LINK
        self.namespace_id = models.NamespaceId(0x88B64C3BE2F47144)
        self.mosaic_id = models.MosaicId(0x2FF7D64F483BC0A6)
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transaction = models.MosaicAliasTransaction.create(
            deadline=self.deadline,
            action_type=self.action_type,
            namespace_id=self.namespace_id,
            mosaic_id=self.mosaic_id,
            network_type=self.network_type,
        )
        private_key = "97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca"
        self.signer = models.Account.create_from_private_key(private_key, self.network_type)
        self.catbuffer = '8900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001904e430000000000000000f1b4815c00000000004471f4e23b4cb688a6c03b484fd6f72f'
        self.payload = '890000004643c4a57eccb783217473cf11bd6642e754d8362a552266fc6e332f523550b3e4431f468c942a1c43748b12f16112b63c282fa48a674a3cb66df33ec8ad100f1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e430000000000000000f1b4815c00000000004471f4e23b4cb688a6c03b484fd6f72f'
        self.hash = 'fc62407dec7110eb74eb9f210676411f7a3fb3829ac6e002567883e34c4f2a3b'
        self.embedded = '390000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e43004471f4e23b4cb688a6c03b484fd6f72f'

    def test_init(self):
        self.assertEqual(self.transaction.deadline, self.deadline)
        self.assertEqual(self.transaction.action_type, self.action_type)
        self.assertEqual(self.transaction.namespace_id, self.namespace_id)
        self.assertEqual(self.transaction.mosaic_id, self.mosaic_id)
        self.assertEqual(self.transaction.network_type, self.network_type)

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.transaction.__dict__

    def test_catbuffer(self):
        catbuffer = self.transaction.to_catbuffer()
        self.assertEqual(self.catbuffer, util.hexlify(catbuffer))
        self.assertEqual(self.transaction, models.Transaction.from_catbuffer(catbuffer))

    def test_sign_with(self):
        signed_transaction = self.transaction.sign_with(self.signer)
        self.assertEqual(signed_transaction.payload, self.payload)
        self.assertEqual(signed_transaction.hash, self.hash)
        self.assertEqual(signed_transaction.signer, self.signer.public_key)
        self.assertEqual(signed_transaction.type, models.TransactionType.MOSAIC_ALIAS)
        self.assertEqual(signed_transaction.network_type, self.signer.network_type)

    def test_to_aggregate(self):
        inner = self.transaction.to_aggregate(self.signer.public_account)
        catbuffer = inner.to_catbuffer()
        self.assertEqual(self.embedded, util.hexlify(catbuffer))

        with self.assertRaises(TypeError):
            inner.__dict__

    def test_dataclasses(self):
        self.assertEqual(self.transaction, self.transaction.replace())
        self.assertIsInstance(self.transaction.asdict(), dict)
        self.assertIsInstance(self.transaction.astuple(), tuple)
        self.assertIsInstance(self.transaction.fields(), tuple)


class TestMultisigCosignatoryModificationType(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.add = models.MultisigCosignatoryModificationType.ADD
        self.remove = models.MultisigCosignatoryModificationType.REMOVE
        self.dto = 0
        self.catbuffer = b'\x00'

    def test_description(self):
        self.assertEqual(self.add.description(), 'Add cosignatory.')
        self.assertEqual(self.remove.description(), 'Remove cosignatory.')

    def test_to_dto(self):
        self.assertEqual(self.add.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.add, models.MultisigCosignatoryModificationType.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.add.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.add, models.MultisigCosignatoryModificationType.from_catbuffer(self.catbuffer, self.network_type))


class TestPlainMessage(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.message = models.PlainMessage(b'Hello world!')
        self.dto = {
            'type': 0,
            'payload': '48656c6c6f20776f726c6421',
        }
        self.catbuffer = b'Hello world!'

    def test_init(self):
        self.assertEqual(self.message.type, models.MessageType.PLAIN)
        self.assertEqual(self.message.payload, b'Hello world!')

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.message.__dict__

    def test_create(self):
        self.assertEqual(self.message.type, models.MessageType.PLAIN)
        self.assertEqual(self.message.payload, b'Hello world!')

    def test_to_dto(self):
        self.assertEqual(self.message.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.message, models.PlainMessage.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.message.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.message, models.PlainMessage.from_catbuffer(self.catbuffer, self.network_type))

    def test_dataclasses(self):
        self.assertEqual(self.message, self.message.replace())
        self.assertIsInstance(self.message.asdict(), dict)
        self.assertIsInstance(self.message.astuple(), tuple)
        self.assertIsInstance(self.message.fields(), tuple)


class TestSecretProofTransaction(harness.TestCase):

    def setUp(self):
        self.deadline = models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57))
        self.hash_type = models.HashType.SHA3_256
        self.proof = 'b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.secret = util.hashlib.sha3_256(util.unhexlify(self.proof)).hexdigest()
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transaction = models.SecretProofTransaction.create(
            deadline=self.deadline,
            hash_type=self.hash_type,
            secret=self.secret,
            proof=self.proof,
            network_type=self.network_type,
        )
        self.dto = {
            'transaction': {
                'version': 36865,
                'type': 16978,
                'fee': [0, 0],
                'deadline': [1552004337, 0],
                'hashAlgorithm': int(self.hash_type),
                'secret': self.secret,
                'proof': self.proof,
            },
        }
        private_key = "97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca"
        self.signer = models.Account.create_from_private_key(private_key, self.network_type)
        self.catbuffer = 'bb000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.payload = 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.hash = 'd8949c87755cfd2c003fec4e1bd4aadb00b3f4838fc5ce7ffeded9385805fcdd'
        self.embedded = '6b0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501905242009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'

    def test_init(self):
        self.assertEqual(self.transaction.deadline, self.deadline)
        self.assertEqual(self.transaction.hash_type, self.hash_type)
        self.assertEqual(self.transaction.secret, self.secret)
        self.assertEqual(self.transaction.proof, self.proof)
        self.assertEqual(self.transaction.network_type, self.network_type)

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.transaction.__dict__

    def test_catbuffer(self):
        catbuffer = self.transaction.to_catbuffer()
        self.assertEqual(self.catbuffer, util.hexlify(catbuffer))
        self.assertEqual(self.transaction, models.Transaction.from_catbuffer(catbuffer))

    def test_dto(self):
        self.assertEqual(self.dto, self.transaction.to_dto())
        self.assertEqual(self.transaction, models.Transaction.from_dto(self.dto))

    def test_sign_with(self):
        signed_transaction = self.transaction.sign_with(self.signer)
        self.assertEqual(signed_transaction.payload, self.payload)
        self.assertEqual(signed_transaction.hash, self.hash)
        self.assertEqual(signed_transaction.signer, self.signer.public_key)
        self.assertEqual(signed_transaction.type, models.TransactionType.SECRET_PROOF)
        self.assertEqual(signed_transaction.network_type, self.signer.network_type)

    def test_to_aggregate(self):
        inner = self.transaction.to_aggregate(self.signer.public_account)
        catbuffer = inner.to_catbuffer()
        self.assertEqual(self.embedded, util.hexlify(catbuffer))

        with self.assertRaises(TypeError):
            inner.__dict__

    def test_dataclasses(self):
        self.assertEqual(self.transaction, self.transaction.replace())
        self.assertIsInstance(self.transaction.asdict(), dict)
        self.assertIsInstance(self.transaction.astuple(), tuple)
        self.assertIsInstance(self.transaction.fields(), tuple)


class TestSignedTransaction(harness.TestCase):

    def setUp(self):
        self.payload = 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.hash = 'd8949c87755cfd2c003fec4e1bd4aadb00b3f4838fc5ce7ffeded9385805fcdd'
        self.signer = '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955'
        self.type = models.TransactionType.SECRET_PROOF
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transaction = models.SignedTransaction(self.payload, self.hash, self.signer, self.type, self.network_type)

    def test_init(self):
        self.assertEqual(self.transaction.payload, self.payload)
        self.assertEqual(self.transaction.hash, self.hash)
        self.assertEqual(self.transaction.signer, self.signer)
        self.assertEqual(self.transaction.type, self.type)
        self.assertEqual(self.transaction.network_type, self.network_type)

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.transaction.__dict__

    def test_dataclasses(self):
        self.assertEqual(self.transaction, self.transaction.replace())
        self.assertIsInstance(self.transaction.asdict(), dict)
        self.assertIsInstance(self.transaction.astuple(), tuple)
        self.assertIsInstance(self.transaction.fields(), tuple)


class TestSyncAnnounce(harness.TestCase):

    def setUp(self):
        self.payload = 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.hash = 'd8949c87755cfd2c003fec4e1bd4aadb00b3f4838fc5ce7ffeded9385805fcdd'
        self.address = 'SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG'
        self.network_type = models.NetworkType.MIJIN_TEST
        self.sync = models.SyncAnnounce(self.payload, self.hash, self.address)

    def test_init(self):
        self.assertEqual(self.sync.payload, self.payload)
        self.assertEqual(self.sync.hash, self.hash)
        self.assertEqual(self.sync.address, self.address)

    def test_create(self):
        signer = '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955'
        type = models.TransactionType.SECRET_PROOF
        transaction = models.SignedTransaction(self.payload, self.hash, signer, type, self.network_type)
        self.assertEqual(self.sync, models.SyncAnnounce.create(transaction))

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.sync.__dict__

    def test_dataclasses(self):
        self.assertEqual(self.sync, self.sync.replace())
        self.assertIsInstance(self.sync.asdict(), dict)
        self.assertIsInstance(self.sync.astuple(), tuple)
        self.assertIsInstance(self.sync.fields(), tuple)


class TestTransaction(harness.TestCase):

    def test_transaction_hash(self):
        hash = 'd8949c87755cfd2c003fec4e1bd4aadb00b3f4838fc5ce7ffeded9385805fcdd'
        transaction = 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.assertEqual(hash, models.Transaction.transaction_hash(transaction))

    def test_catbuffer_size_shared(self):
        self.assertEqual(models.Transaction.catbuffer_size_shared(), 120)

    def test_from_catbuffer(self):
        network_type = models.NetworkType.MIJIN_TEST
        private_key = "97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca"
        transactions = [
            (models.TransactionType.ADDRESS_ALIAS, '9a000000102e9c68fe9cbaa5d1d27ad35f9e386b42c265749be0e27182b8a9ebf18a0357332ef4ee350b648ea00437790c70471959b9334aea2e2e89356d52613fd385021b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e420000000000000000f1b4815c00000000004471f4e23b4cb68890fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc'),
            (models.TransactionType.MOSAIC_ALIAS, '890000004643c4a57eccb783217473cf11bd6642e754d8362a552266fc6e332f523550b3e4431f468c942a1c43748b12f16112b63c282fa48a674a3cb66df33ec8ad100f1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e430000000000000000f1b4815c00000000004471f4e23b4cb688a6c03b484fd6f72f'),
            (models.TransactionType.SECRET_PROOF, 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'),
            (models.TransactionType.TRANSFER, 'b0000000edbf8094c382ddb1c2341ea861ad979eee4b576b1050bfb5b306cf07d6b378e7c58761a7e5980c09f65b15b5b8caea5d631f9e533c04d33b71961e5ad7b27e0f1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955039054410000000000000000f1b4815c0000000090fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0c000148656c6c6f20776f726c64210500000000000000e803000000000000'),
        ]

        for type, payload in transactions:
            transaction = models.Transaction.from_catbuffer(payload)
            self.assertEqual(transaction.type, type)


    # TODO(ahuszagh) Need to test the hooks.
    # Implement...
    #   is_unconfirmed
    #   is_confirmed
    #   has_missing_signatures
    #   is_unannounced


class TestTransactionAnnounceResponse(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.response = models.TransactionAnnounceResponse('Hello world!')
        self.dto = {'message': 'Hello world!'}

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.response.__dict__

    def test_to_dto(self):
        self.assertEqual(self.response.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.response, models.TransactionAnnounceResponse.from_dto(self.dto, self.network_type))

    def test_dataclasses(self):
        self.assertEqual(self.response, self.response.replace())
        self.assertIsInstance(self.response.asdict(), dict)
        self.assertIsInstance(self.response.astuple(), tuple)
        self.assertIsInstance(self.response.fields(), tuple)


class TestTransactionInfo(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transaction_info = models.TransactionInfo(
            height=1,
            index=0,
            id="5C7C06FF5CC1FE000176FA12",
            hash="B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
            merkle_component_hash="B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
        )
        self.dto = {
            "height": [1, 0],
            "hash": "B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
            "merkleComponentHash": "B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
            "index": 0,
            "id": "5C7C06FF5CC1FE000176FA12"
        }

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.transaction_info.__dict__

    def test_init(self):
        models.TransactionInfo(1, 0, "5C7C06FF5CC1FE000176FA12")
        models.TransactionInfo(1, 0, "5C7C06FF5CC1FE000176FA12", None)
        models.TransactionInfo(1, 0, "5C7C06FF5CC1FE000176FA12", None, None)

    def test_to_dto(self):
        self.assertEqual(self.transaction_info.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.transaction_info, models.TransactionInfo.from_dto(self.dto, self.network_type))

    def test_dataclasses(self):
        self.assertEqual(self.transaction_info, self.transaction_info.replace())
        self.assertIsInstance(self.transaction_info.asdict(), dict)
        self.assertIsInstance(self.transaction_info.astuple(), tuple)
        self.assertIsInstance(self.transaction_info.fields(), tuple)


class TestTransactionStatus(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transaction_status = models.TransactionStatus(
            group=models.TransactionStatusGroup.CONFIRMED,
            status="Success",
            hash="B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
            deadline=models.Deadline.from_timestamp(1),
            height=1
        )
        self.dto = {
            "group": "confirmed",
            "status": "Success",
            "hash": "B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
            "deadline": [1, 0],
            "height": [1, 0]
        }

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.transaction_status.__dict__

    def test_to_dto(self):
        self.assertEqual(self.transaction_status.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.transaction_status, models.TransactionStatus.from_dto(self.dto, self.network_type))

    def test_dataclasses(self):
        self.assertEqual(self.transaction_status, self.transaction_status.replace())
        self.assertIsInstance(self.transaction_status.asdict(), dict)
        self.assertIsInstance(self.transaction_status.astuple(), tuple)
        self.assertIsInstance(self.transaction_status.fields(), tuple)


class TestTransactionStatusError(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.hash = "B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5"
        self.status = "Success"
        self.deadline = models.Deadline.from_timestamp(1)
        self.error = models.TransactionStatusError(self.hash, self.status, self.deadline)
        self.dto = {
            "hash": "B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
            "status": "Success",
            "deadline": [1, 0],
        }

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.error.__dict__

    def test_to_dto(self):
        self.assertEqual(self.error.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.error, models.TransactionStatusError.from_dto(self.dto, self.network_type))

    def test_dataclasses(self):
        self.assertEqual(self.error, self.error.replace())
        self.assertIsInstance(self.error.asdict(), dict)
        self.assertIsInstance(self.error.astuple(), tuple)
        self.assertIsInstance(self.error.fields(), tuple)


class TestTransactionStatusGroup(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.failed = models.TransactionStatusGroup.FAILED
        self.unconfirmed = models.TransactionStatusGroup.UNCONFIRMED
        self.confirmed = models.TransactionStatusGroup.CONFIRMED

    def test_description(self):
        self.assertEqual(self.failed.description(), 'Transaction failed.')

    def test_to_dto(self):
        self.assertEqual(self.failed.to_dto(self.network_type), "failed")
        self.assertEqual(self.unconfirmed.to_dto(self.network_type), "unconfirmed")
        self.assertEqual(self.confirmed.to_dto(self.network_type), "confirmed")

    def test_from_dto(self):
        self.assertEqual(self.failed, models.TransactionStatusGroup.from_dto("failed", self.network_type))


class TestTransactionType(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transfer = models.TransactionType.TRANSFER
        self.dto = 0x4154
        self.catbuffer = b'\x54\x41'

    def test_description(self):
        self.assertEqual(self.transfer.description(), "Transfer Transaction transaction type.")

    def test_to_dto(self):
        self.assertEqual(self.transfer.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.transfer, models.TransactionType.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.transfer.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.transfer, models.TransactionType.from_catbuffer(self.catbuffer, self.network_type))


class TestTransactionVersion(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transfer = models.TransactionVersion.TRANSFER
        self.dto = 3
        self.catbuffer = b'\x03'

    def test_to_dto(self):
        self.assertEqual(self.transfer.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.transfer, models.TransactionVersion.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.transfer.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.transfer, models.TransactionVersion.from_catbuffer(self.catbuffer, self.network_type))


class TestTransferTransaction(harness.TestCase):

    def setUp(self):
        self.deadline = models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57))
        self.address = models.Address('SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54')
        self.namespace_id = models.NamespaceId(0x84b3552d375ffa4b)
        self.mosaics = [models.Mosaic(models.MosaicId(5), 1000)]
        self.message = models.PlainMessage(b'Hello world!')
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transaction = models.TransferTransaction.create(
            deadline=self.deadline,
            recipient=self.address,
            mosaics=self.mosaics,
            message=self.message,
            network_type=self.network_type,
        )
        self.transaction_info = models.TransactionInfo(
            height=1,
            index=0,
            id="5C7C06FF5CC1FE000176FA12",
            hash="B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
            merkle_component_hash="B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
        )
        self.transaction_with_info = self.transaction.replace(
            transaction_info=self.transaction_info
        )
        self.transaction_namespace = self.transaction.replace(
            recipient=self.namespace_id
        )
        self.dto = {
            'transaction': {
                'version': 36867,
                'type': 16724,
                'fee': [0, 0],
                'deadline': [1552004337, 0],
                'recipient': '90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
                'mosaics': [{'amount': [1000, 0], 'id': [5, 0]}],
                'message': {'type': 0, 'payload': '48656c6c6f20776f726c6421'}
            },
        }
        self.dto_with_info = dict(
            meta={
                "height": [1, 0],
                "hash": "B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
                "merkleComponentHash": "B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
                "index": 0,
                "id": "5C7C06FF5CC1FE000176FA12"
            },
            **self.dto
        )
        self.dto_namespace = {
            'transaction': {
                'version': 36867,
                'type': 16724,
                'fee': [0, 0],
                'deadline': [1552004337, 0],
                'recipient': '914bfa5f372d55b38400000000000000000000000000000000',
                'mosaics': [{'amount': [1000, 0], 'id': [5, 0]}],
                'message': {'type': 0, 'payload': '48656c6c6f20776f726c6421'}
            },
        }
        private_key = "97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca"
        self.signer = models.Account.create_from_private_key(private_key, self.network_type)
        self.catbuffer = 'b0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000039054410000000000000000f1b4815c0000000090fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0c000148656c6c6f20776f726c64210500000000000000e803000000000000'
        self.payload = 'b0000000edbf8094c382ddb1c2341ea861ad979eee4b576b1050bfb5b306cf07d6b378e7c58761a7e5980c09f65b15b5b8caea5d631f9e533c04d33b71961e5ad7b27e0f1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955039054410000000000000000f1b4815c0000000090fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0c000148656c6c6f20776f726c64210500000000000000e803000000000000'
        self.hash = '8e5128947c53cd6a7fe537b3d038a9a804b8d1e7827704538c1c95bf0d01703e'
        self.embedded = '600000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550390544190fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0c000148656c6c6f20776f726c64210500000000000000e803000000000000'
        self.catbuffer_namespace = 'b0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000039054410000000000000000f1b4815c00000000914bfa5f372d55b384000000000000000000000000000000000c000148656c6c6f20776f726c64210500000000000000e803000000000000'

    def test_init(self):
        self.assertEqual(self.transaction.deadline, self.deadline)
        self.assertEqual(self.transaction.recipient, self.address)
        self.assertEqual(self.transaction.mosaics, self.mosaics)
        self.assertEqual(self.transaction.message, self.message)
        self.assertEqual(self.transaction.network_type, self.network_type)

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.transaction.__dict__

    def test_catbuffer(self):
        catbuffer = self.transaction.to_catbuffer()
        self.assertEqual(self.catbuffer, util.hexlify(catbuffer))
        self.assertEqual(self.transaction, models.Transaction.from_catbuffer(catbuffer))

        catbuffer = self.transaction_namespace.to_catbuffer()
        self.assertEqual(self.catbuffer_namespace, util.hexlify(catbuffer))
        self.assertEqual(self.transaction_namespace, models.Transaction.from_catbuffer(catbuffer))

    def test_dto(self):
        self.assertEqual(self.dto, self.transaction.to_dto())
        self.assertEqual(self.dto_with_info, self.transaction_with_info.to_dto())
        self.assertEqual(self.dto_namespace, self.transaction_namespace.to_dto())
        self.assertEqual(self.transaction, models.Transaction.from_dto(self.dto))
        self.assertEqual(self.transaction_with_info, models.Transaction.from_dto(self.dto_with_info))
        self.assertEqual(self.transaction_namespace, models.Transaction.from_dto(self.dto_namespace))

    def test_sign_with(self):
        signed_transaction = self.transaction.sign_with(self.signer)
        self.assertEqual(signed_transaction.payload, self.payload)
        self.assertEqual(signed_transaction.hash, self.hash)
        self.assertEqual(signed_transaction.signer, self.signer.public_key)
        self.assertEqual(signed_transaction.type, models.TransactionType.TRANSFER)
        self.assertEqual(signed_transaction.network_type, self.signer.network_type)

    def test_to_aggregate(self):
        inner = self.transaction.to_aggregate(self.signer.public_account)
        catbuffer = inner.to_catbuffer()
        self.assertEqual(self.embedded, util.hexlify(catbuffer))

        with self.assertRaises(TypeError):
            inner.__dict__

    def test_dataclasses(self):
        self.assertEqual(self.transaction, self.transaction.replace())
        self.assertIsInstance(self.transaction.asdict(), dict)
        self.assertIsInstance(self.transaction.astuple(), tuple)
        self.assertIsInstance(self.transaction.fields(), tuple)
