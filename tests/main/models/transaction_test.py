import datetime
import random

from nem2 import util
from nem2 import models
from tests import harness


def psuedo_entropy(size: int) -> bytes:
    return bytes([random.randint(0, 255) for _ in range(size)])


# TODO(ahuszagh) Switch to a data-driven test.
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
        pass
        # TODO(ahuszagh) Confirm...
        # dto = self.transaction.to_dto()
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


@harness.model_test_case({
    'type': models.AggregateTransactionCosignature,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'signature': '5780c8df9d46ba2bcf029dcc5d3bf55fe1cb5be7abcf30387c4637ddedfc2152703ca0ad95f21bb9b942f3cc52fcfc2064c7b84cf60d1a9e69195f1943156c07',
        'signer': models.PublicAccount(models.Address('SDWGJE7XOYRX5RQMMLWF4TE7U5Y2HUYBRDVX2OJE'), 'a5f82ec8ebb341427b6785c8111906cd0df18838fb11b51ce0e18b5e79dff630'),
    },
    'dto': {
        'signature': '5780c8df9d46ba2bcf029dcc5d3bf55fe1cb5be7abcf30387c4637ddedfc2152703ca0ad95f21bb9b942f3cc52fcfc2064c7b84cf60d1a9e69195f1943156c07',
        'signer': 'a5f82ec8ebb341427b6785c8111906cd0df18838fb11b51ce0e18b5e79dff630',
    },
    'catbuffer': b'\xa5\xf8.\xc8\xeb\xb3AB{g\x85\xc8\x11\x19\x06\xcd\r\xf1\x888\xfb\x11\xb5\x1c\xe0\xe1\x8b^y\xdf\xf60W\x80\xc8\xdf\x9dF\xba+\xcf\x02\x9d\xcc];\xf5_\xe1\xcb[\xe7\xab\xcf08|F7\xdd\xed\xfc!Rp<\xa0\xad\x95\xf2\x1b\xb9\xb9B\xf3\xccR\xfc\xfc d\xc7\xb8L\xf6\r\x1a\x9ei\x19_\x19C\x15l\x07',
})
class TestAggregateTransactionCosignature(harness.TestCase):

    def test_invalid_signature(self):
        with self.assertRaises(ValueError):
            self.type(signature='', signer=self.data['signer'])


@harness.model_test_case({
    'type': models.AggregateTransactionInfo,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'height': 18160,
        'index': 0,
        'id': "5a0069d83f17cf0001777e56",
        'aggregate_hash': "3d28c804edd07d5a728e5c5ffec01ab07afa5766ae6997b38526d36015a4d006",
        'aggregate_id': "5a0069d83f17cf0001777e55",
    },
    'dto': {
        "height": [18160, 0],
        "aggregateHash": "3d28c804edd07d5a728e5c5ffec01ab07afa5766ae6997b38526d36015a4d006",
        "aggregateId": "5a0069d83f17cf0001777e55",
        "index": 0,
        "id": "5a0069d83f17cf0001777e56"
    },
})
class TestAggregateTransactionInfo(harness.TestCase):
    pass


class TestAliasTransaction(harness.TestCase):
    pass        # TODO(ahuszagh) Implement


@harness.model_test_case({
    'type': models.CosignatureSignedTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'parent_hash': '671653c94e2254f2a23efedb15d67c38332aed1fbd24b063c0a8e675582b6a96',
        'signature': '939673209a13ff82397578d22cc96eb8516a6760c894d9b7535e3a1e068007b9255cfa9a914c97142a7ae18533e381c846b69d2ae0d60d1dc8a55ad120e2b606',
        'signer': '7681ed5023141d9cdcf184e5a7b60b7d466739918ed5da30f7e71ea7b86eff2d',
    },
    'dto': {
        'parentHash': '671653c94e2254f2a23efedb15d67c38332aed1fbd24b063c0a8e675582b6a96',
        'signature': '939673209a13ff82397578d22cc96eb8516a6760c894d9b7535e3a1e068007b9255cfa9a914c97142a7ae18533e381c846b69d2ae0d60d1dc8a55ad120e2b606',
        'signer': '7681ed5023141d9cdcf184e5a7b60b7d466739918ed5da30f7e71ea7b86eff2d',
    },
})
class TestCosignatureSignedTransaction(harness.TestCase):
    pass


# TODO(ahuszagh)
#   Add cosignature_transaction


@harness.enum_test_case({
    'type': models.ChronoUnit,
    'enums': [
        models.ChronoUnit.MICROSECONDS,
        models.ChronoUnit.MILLISECONDS,
        models.ChronoUnit.SECONDS,
        models.ChronoUnit.MINUTES,
        models.ChronoUnit.HOURS,
    ],
    'values': [
        0,
        1,
        2,
        3,
        4,
    ],
    'descriptions': [
        'Microseconds.',
        'Milliseconds.',
        'Seconds.',
        'Minutes.',
        'Hours.',
    ],
    'custom': [
        {
            'name': 'test_to_timedelta',
            'callback': lambda self, x: str(x.to_timedelta(1)),
            'results': ['0:00:00.000001', '0:00:00.001000', '0:00:01', '0:01:00', '1:00:00'],
        },
    ],
})
class TestChronoUnit(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.Deadline,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'deadline': datetime.datetime(2019, 3, 8, 0, 18, 57),
    },
    'dto': [1552004337, 0],
    'catbuffer': b'\xf1\xb4\x81\\\x00\x00\x00\x00',
})
class TestDeadline(harness.TestCase):

    def test_create(self):
        with self.assertRaises(ValueError):
            self.type.create(-1)
        with self.assertRaises(ValueError):
            self.type.create(25, models.ChronoUnit.HOURS)

        self.type.create(23, models.ChronoUnit.HOURS)


@harness.enum_test_case({
    'type': models.HashType,
    'enums': [
        models.HashType.SHA3_256,
        models.HashType.KECCAK_256,
        models.HashType.HASH_160,
        models.HashType.HASH_256,
    ],
    'values': [
        0,
        1,
        2,
        3,
    ],
    'descriptions': [
        'SHA3-256 (default).',
        'Keccak-256 (ETH compatibility).',
        'SHA3-256 to RIPEMD-160 (BTC compatibility).',
        'SHA3-256 to SHA3-256 (BTC compatibility).',
    ],
    'dto': [
        0,
        1,
        2,
        3,
    ],
    'catbuffer': [
        b'\x00',
        b'\x01',
        b'\x02',
        b'\x03',
    ],
    'custom': [
        {
            'name': 'test_validate40',
            'callback': lambda self, x: x.validate(util.hexlify(psuedo_entropy(20))),
            'results': [False, False, True, False],
        },
        {
            'name': 'test_validate64',
            'callback': lambda self, x: x.validate(util.hexlify(psuedo_entropy(32))),
            'results': [True, True, False, True],
        },
        {
            'name': 'test_hash_length',
            'callback': lambda self, x: x.hash_length(),
            'results': [64, 64, 40, 64],
        },
    ],
})
class TestHashType(harness.TestCase):

    def test_invalid_digits(self):
        data = 'GqewCJhTUHlVOoQhRZIVHkbExIZjcmzNYDXErhZrYmhanFNagXPthmEapPPyGrlr'
        self.assertFalse(self.enums[0].validate(data))


class TestInnnerTransaction(harness.TestCase):

    def test_catbuffer_size_shared(self):
        self.assertEqual(models.InnerTransaction.catbuffer_size_shared(), 40)

    def test_from_catbuffer(self):
        transactions = [
            (models.TransactionType.ADDRESS_ALIAS, '4a0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e42004471f4e23b4cb68890fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc'),
            (models.TransactionType.MOSAIC_ALIAS, '390000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e43004471f4e23b4cb688a6c03b484fd6f72f'),
            (models.TransactionType.SECRET_PROOF, '6b0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501905242009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'),
            (models.TransactionType.TRANSFER, '600000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550390544190fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0c000148656c6c6f20776f726c64210500000000000000e803000000000000'),
        ]

        for type, payload in transactions:
            transaction = models.InnerTransaction.from_catbuffer(payload)
            self.assertEqual(transaction.type, type)


# TODO(ahuszagh) Implement...
class TestLockFundsTransaction(harness.TestCase):
    pass


class TestMessage(harness.TestCase):

    def test_create(self):
        with self.assertRaises(NotImplementedError):
            models.Message.create(b'Hello world!')

    def test_dto(self):
        dto = {'payload': util.hexlify(b'Hello world!'), 'type': 0}
        with self.assertRaises(NotImplementedError):
            models.Message.from_dto(dto, models.NetworkType.MIJIN_TEST)


@harness.enum_test_case({
    'type': models.MessageType,
    'enums': [
        models.MessageType.PLAIN,
    ],
    'values': [
        0,
    ],
    'descriptions': [
        "Plain message.",
    ],
    'dto': [
        0,
    ],
    'catbuffer': [
        b'\x00',
    ],
})
class TestMessageType(harness.TestCase):
    pass


# TODO(ahuszagh) Implement...
class TestModifyMultisigAccountTransaction(harness.TestCase):
    pass


@harness.transaction_test_case({
    'type': models.MosaicAliasTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.MOSAIC_ALIAS,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'action_type': models.AliasActionType.LINK,
        'namespace_id': models.NamespaceId(0x88B64C3BE2F47144),
        'mosaic_id': models.MosaicId(0x2FF7D64F483BC0A6),
    },
    # TODO(ahuszagh) Add DTO...
    'catbuffer': '8900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001904e430000000000000000f1b4815c00000000004471f4e23b4cb688a6c03b484fd6f72f',
    'extras': {
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '890000004643c4a57eccb783217473cf11bd6642e754d8362a552266fc6e332f523550b3e4431f468c942a1c43748b12f16112b63c282fa48a674a3cb66df33ec8ad100f1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e430000000000000000f1b4815c00000000004471f4e23b4cb688a6c03b484fd6f72f',
            'hash': 'fc62407dec7110eb74eb9f210676411f7a3fb3829ac6e002567883e34c4f2a3b',
        },
        'embedded': '390000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e43004471f4e23b4cb688a6c03b484fd6f72f',
    },
})
class TestMosaicAliasTransaction(harness.TestCase):

    def test_create(self):
        self.assertEqual(self.model, self.type.create(
            deadline=self.data['deadline'],
            action_type=self.data['action_type'],
            namespace_id=self.data['namespace_id'],
            mosaic_id=self.data['mosaic_id'],
            network_type=self.data['network_type'],
        ))


@harness.transaction_test_case({
    'type': models.MosaicDefinitionTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.MOSAIC_DEFINITION,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'nonce': models.MosaicNonce(1),
        'mosaic_id': models.MosaicId.from_hex('6c699a1517bea955'),
        'mosaic_properties': models.MosaicProperties(0x3, 3),
    },
    'dto': {
        'transaction': {
            'version': 36867,
            'type': 16717,
            'maxFee': [0, 0],
            'deadline': [1552004337, 0],
            'mosaicNonce': 1,
            'mosaicId': [398371157, 1818860053],
            'properties': [
                {'id': 0, 'value': [3, 0]},
                {'id': 1, 'value': [3, 0]},
            ],
        },
    },
    'catbuffer': '8700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003904d410000000000000000f1b4815c000000000100000055a9be17159a696c000303',
    'extras': {
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '87000000f2f64a644a3e4bf33905eace1b629ccc0676c06f3971bb4049cea9685f566cb6dc1f3428884398992b8e56e5bad0efa99026e9860c3fdc98d2bd3898ac6eea071b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895503904d410000000000000000f1b4815c000000000100000055a9be17159a696c000303',
            'hash': '30d4a9f3ae51e5d47abf9db5adb98a7def25837e565745a07a35201cc652eefa',
        },
        'embedded': '370000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895503904d410100000055a9be17159a696c000303',
    },
})
class TestMosaicDefinitionTransaction(harness.TestCase):

    def test_create(self):
        self.assertEqual(self.model, self.type.create(
            deadline=self.data['deadline'],
            nonce=self.data['nonce'],
            mosaic_id=self.data['mosaic_id'],
            mosaic_properties=self.data['mosaic_properties'],
            network_type=self.data['network_type'],
        ))


@harness.transaction_test_case({
    'type': models.MosaicSupplyChangeTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.MOSAIC_SUPPLY_CHANGE,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'mosaic_id': models.MosaicId.from_hex('941299b2b7e1291c'),
        'direction': models.MosaicSupplyType.INCREASE,
        'delta': 15000000,
    },
    'dto': {
        'transaction': {
            'version': 36866,
            'type': 16973,
            'maxFee': [0, 0],
            'deadline': [1552004337, 0],
            'mosaicId': [3084986652, 2484246962],
            'direction': 1,
            'delta': [15000000, 0],
        },
    },
    'catbuffer': '8900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002904d420000000000000000f1b4815c000000001c29e1b7b299129401c0e1e40000000000',
    'extras': {
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '8900000037b75c5e5dd09c55b04c1b77b58be976cf234b3c1668a0fb502586664716b8d1bbe263f43fafd9288f19d3d11d32a164d7e2ada4f1a5889238c721c3748de00d1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895502904d420000000000000000f1b4815c000000001c29e1b7b299129401c0e1e40000000000',
            'hash': '8ed5521912d32097e4f9b172fab4200966a99c72910b839bff934e0c3ac219e0',
        },
        'embedded': '390000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895502904d421c29e1b7b299129401c0e1e40000000000',
    },
})
class TestMosaicSupplyChangeTransaction(harness.TestCase):

    def test_create(self):
        self.assertEqual(self.model, self.type.create(
            deadline=self.data['deadline'],
            mosaic_id=self.data['mosaic_id'],
            direction=self.data['direction'],
            delta=self.data['delta'],
            network_type=self.data['network_type'],
        ))


@harness.model_test_case({
    'type': models.MultisigCosignatoryModification,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'type': models.MultisigCosignatoryModificationType.ADD,
        'cosignatory_public_account': models.PublicAccount.create_from_public_key('1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955', models.NetworkType.MIJIN_TEST),
    },
    'dto': {
        'type': 0,
        'cosignatoryPublicKey': '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
    },
    'catbuffer': '001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
})
class TestMultisigCosignatoryModification(harness.TestCase):
    pass


@harness.enum_test_case({
    'type': models.MultisigCosignatoryModificationType,
    'enums': [
        models.MultisigCosignatoryModificationType.ADD,
        models.MultisigCosignatoryModificationType.REMOVE,
    ],
    'values': [
        0,
        1,
    ],
    'descriptions': [
        'Add cosignatory.',
        'Remove cosignatory.',
    ],
    'dto': [
        0,
        1,
    ],
    'catbuffer': [
        b'\x00',
        b'\x01',
    ],
})
class TestMultisigCosignatoryModificationType(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.PlainMessage,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'payload': b'Hello world!',
    },
    'catbuffer': b'Hello world!',
    'dto': {
        'type': 0,
        'payload': '48656c6c6f20776f726c6421',
    },
})
class TestPlainMessage(harness.TestCase):
    pass


@harness.transaction_test_case({
    'type': models.RegisterNamespaceTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.REGISTER_NAMESPACE,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'namespace_type': models.NamespaceType.ROOT_NAMESPACE,
        'duration': 100,
        'parent_id': None,
        'namespace_name': models.NamespaceName.create_from_name('sample'),
    },
    'dto': {
        'transaction': {
            'version': 36866,
            'type': 16718,
            'maxFee': [0, 0],
            'deadline': [1552004337, 0],
            'namespaceType': 0,
            'duration': [100, 0],
            'namespaceId': [0xe2f47144, 0x88b64c3b],
            'name': 'sample',
        },
    },
    'catbuffer': '9000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002904e410000000000000000f1b4815c000000000064000000000000004471f4e23b4cb6880673616d706c65',
    'extras': {
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '90000000a2d9473cfd2e823e3ff5c621082348a8d45f5fc7f1d12d315f69a4be3f10ea784d17f09c717e4a4a3791a9cb2922e067c966585eba2bbff396ef82610bd8dd071b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895502904e410000000000000000f1b4815c000000000064000000000000004471f4e23b4cb6880673616d706c65',
            'hash': '6ae78838ea31df82c4f81bef5047d420da2ee1de5645a128d9525740c0d75377',
        },
        'embedded': '400000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895502904e410064000000000000004471f4e23b4cb6880673616d706c65',
    },
})
class TestRegisterNamespaceTransactionRoot(harness.TestCase):

    def test_rich_init(self):
        # Test valid root namespace
        kwds = self.data.copy()
        self.assertEqual(self.model, self.type(**kwds))

        # Test invalid root namespace
        kwds['parent_id'] = models.NamespaceId(0)
        with self.assertRaises(ValueError):
            self.type(**kwds)

        del kwds['duration']
        del kwds['parent_id']
        with self.assertRaises(ValueError):
            self.type(**kwds)

    def test_properties(self):
        self.assertEqual(self.model.namespace_name.namespace_id, self.model.namespace_id)
        self.assertEqual(self.model.namespace_name.name, self.model.name)

    def test_create_root_namespace(self):
        self.assertEqual(self.model, self.type.create_root_namespace(
            deadline=self.data['deadline'],
            namespace_name=self.data['namespace_name'].name,
            duration=self.data['duration'],
            network_type=self.data['network_type'],
        ))


@harness.transaction_test_case({
    'type': models.RegisterNamespaceTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.REGISTER_NAMESPACE,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'namespace_type': models.NamespaceType.SUB_NAMESPACE,
        'parent_id': models.NamespaceId(0x88b64c3be2f47144),
        'namespace_name': models.NamespaceName.create_from_name('sample.sub'),
    },
    'dto': {
        'transaction': {
            'version': 36866,
            'type': 16718,
            'maxFee': [0, 0],
            'deadline': [1552004337, 0],
            'namespaceType': 1,
            'parentId': [0xe2f47144, 0x88b64c3b],
            'namespaceId': [0x5a71acc9, 0xfa942971],
            'name': 'sub',
        },
    },
    'catbuffer': '8d00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002904e410000000000000000f1b4815c00000000014471f4e23b4cb688c9ac715a712994fa03737562',
    'extras': {
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '8d000000e0ab014652acd0c677b5a340f0ab5e78679eb697c37984f4b8d4df2d45b7c207ab0e424b8fade9cf511e0e7c649041c4aa22065b71461a14985a763474c32e0f1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895502904e410000000000000000f1b4815c00000000014471f4e23b4cb688c9ac715a712994fa03737562',
            'hash': '5918c390aad2c50ed4fec0a193163372449d8d8b80a78e451399e94204cac40b',
        },
        'embedded': '3d0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895502904e41014471f4e23b4cb688c9ac715a712994fa03737562',
        'parent_namespace': 'sample',
    },
})
class TestRegisterNamespaceTransactionSub(harness.TestCase):

    def test_rich_init(self):
        # Test valid sub namespace
        kwds = self.data.copy()
        self.assertEqual(self.model, self.type(**kwds))

        # Test invalid subnamespace
        kwds['duration'] = 100
        with self.assertRaises(ValueError):
            self.type(**kwds)

        del kwds['duration']
        del kwds['parent_id']
        with self.assertRaises(ValueError):
            self.type(**kwds)

    def test_create_sub_namespace(self):
        self.assertEqual(self.model, self.type.create_sub_namespace(
            deadline=self.data['deadline'],
            namespace_name=self.data['namespace_name'].name,
            parent_namespace=self.data['parent_id'],
            network_type=self.data['network_type'],
        ))

    def test_create_sub_namespace_from_name(self):
        self.assertEqual(self.model, self.type.create_sub_namespace(
            deadline=self.data['deadline'],
            namespace_name=self.data['namespace_name'].name,
            parent_namespace=self.extras['parent_namespace'],
            network_type=self.data['network_type'],
        ))


@harness.transaction_test_case({
    'type': models.SecretLockTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.SECRET_LOCK,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'mosaic': models.Mosaic(models.MosaicId(5), 1000),
        'duration': 100,
        'hash_type': models.HashType.SHA3_256,
        'secret': '9b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e',
        'recipient': models.Address('SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54'),
    },
    'dto': {
        'transaction': {
            'version': 36865,
            'type': 16722,
            'maxFee': [0, 0],
            'deadline': [1552004337, 0],
            'mosaicId': [5, 0],
            'amount': [1000, 0],
            'duration': [100, 0],
            'hashAlgorithm': 0,
            'secret': '9b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e',
            'recipient': '90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
        },
    },
    'catbuffer': 'ca000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000019052410000000000000000f1b4815c000000000500000000000000e8030000000000006400000000000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
    'extras': {
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': 'ca0000007c466426460932877777a0ecac6d0fb691a21fea28a5ec00e85d75c2c5527b84b817ff0a6afe3816d69d73d5f0e05ae18f447633862dc1fc109f1097732588081b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052410000000000000000f1b4815c000000000500000000000000e8030000000000006400000000000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
            'hash': '3345a5f879c5043bd965d0df6060aaeb5ba7b35a102e19a93c2013fe32a371ca',
        },
        'embedded': '7a0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052410500000000000000e8030000000000006400000000000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
    },
})
class TestSecretLockTransaction(harness.TestCase):

    def test_secret(self):
        with self.assertRaises(ValueError):
            kwds = self.data.copy()
            kwds['secret'] = kwds['secret'][:40]
            self.type(**kwds)

    def test_create(self):
        self.assertEqual(self.model, self.type.create(
            deadline=self.data['deadline'],
            mosaic=self.data['mosaic'],
            duration=self.data['duration'],
            hash_type=self.data['hash_type'],
            secret=self.data['secret'],
            recipient=self.data['recipient'],
            network_type=self.data['network_type'],
        ))


@harness.transaction_test_case({
    'type': models.SecretProofTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.SECRET_PROOF,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'hash_type': models.HashType.SHA3_256,
        'secret': '9b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e',
        'proof': 'b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
    },
    'dto': {
        'transaction': {
            'version': 36865,
            'type': 16978,
            'maxFee': [0, 0],
            'deadline': [1552004337, 0],
            'hashAlgorithm': 0,
            'secret': '9b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e',
            'proof': 'b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
        },
    },
    'catbuffer': 'bb000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
    'extras': {
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
            'hash': 'd8949c87755cfd2c003fec4e1bd4aadb00b3f4838fc5ce7ffeded9385805fcdd',
        },
        'embedded': '6b0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501905242009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
    },
})
class TestSecretProofTransaction(harness.TestCase):

    def test_secret(self):
        with self.assertRaises(ValueError):
            kwds = self.data.copy()
            kwds['secret'] = kwds['secret'][:40]
            self.type(**kwds)

    def test_create(self):
        self.assertEqual(self.model, self.type.create(
            deadline=self.data['deadline'],
            hash_type=self.data['hash_type'],
            secret=self.data['secret'],
            proof=self.data['proof'],
            network_type=self.data['network_type'],
        ))


@harness.model_test_case({
    'type': models.SignedTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'payload': 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
        'hash': 'd8949c87755cfd2c003fec4e1bd4aadb00b3f4838fc5ce7ffeded9385805fcdd',
        'signer': '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
        'type': models.TransactionType.SECRET_PROOF,
        'network_type': models.NetworkType.MIJIN_TEST,
    },
})
class TestSignedTransaction(harness.TestCase):

    def test_hash(self):
        with self.assertRaises(ValueError):
            kwds = self.data.copy()
            kwds['hash'] = kwds['hash'][:32]
            self.type(**kwds)

    def test_signer(self):
        with self.assertRaises(ValueError):
            kwds = self.data.copy()
            kwds['signer'] = kwds['signer'][:32]
            self.type(**kwds)


@harness.model_test_case({
    'type': models.SyncAnnounce,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'payload': 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
        'hash': 'd8949c87755cfd2c003fec4e1bd4aadb00b3f4838fc5ce7ffeded9385805fcdd',
        'address': 'SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG',
    },
    'dto': {
        'payload': 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
        'hash': 'd8949c87755cfd2c003fec4e1bd4aadb00b3f4838fc5ce7ffeded9385805fcdd',
        'address': 'SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG',
    },
    'extras': {
        'type': models.TransactionType.SECRET_PROOF,
        'public_key': '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
    }
})
class TestSyncAnnounce(harness.TestCase):

    def test_hash(self):
        with self.assertRaises(ValueError):
            kwds = self.data.copy()
            kwds['hash'] = kwds['hash'][:32]
            self.type(**kwds)

    def test_create(self):
        signed_transaction = models.SignedTransaction(
            payload=self.data['payload'],
            hash=self.data['hash'],
            signer=self.extras['public_key'],
            type=self.extras['type'],
            network_type=self.network_type,
        )
        self.assertEqual(self.model, self.type.create(signed_transaction))


class TestTransaction(harness.TestCase):

    def test_transaction_hash(self):
        hash = 'd8949c87755cfd2c003fec4e1bd4aadb00b3f4838fc5ce7ffeded9385805fcdd'
        transaction = 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.assertEqual(hash, models.Transaction.transaction_hash(transaction))

    def test_catbuffer_size_shared(self):
        self.assertEqual(models.Transaction.catbuffer_size_shared(), 120)

    def test_from_catbuffer(self):
        transactions = [
            (models.TransactionType.ADDRESS_ALIAS, '9a000000102e9c68fe9cbaa5d1d27ad35f9e386b42c265749be0e27182b8a9ebf18a0357332ef4ee350b648ea00437790c70471959b9334aea2e2e89356d52613fd385021b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e420000000000000000f1b4815c00000000004471f4e23b4cb68890fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc'),
            (models.TransactionType.MOSAIC_ALIAS, '890000004643c4a57eccb783217473cf11bd6642e754d8362a552266fc6e332f523550b3e4431f468c942a1c43748b12f16112b63c282fa48a674a3cb66df33ec8ad100f1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e430000000000000000f1b4815c00000000004471f4e23b4cb688a6c03b484fd6f72f'),
            (models.TransactionType.SECRET_LOCK, 'ca000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000019052410000000000000000f1b4815c000000000500000000000000e8030000000000006400000000000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc'),
            (models.TransactionType.SECRET_PROOF, 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'),
            (models.TransactionType.TRANSFER, 'b0000000edbf8094c382ddb1c2341ea861ad979eee4b576b1050bfb5b306cf07d6b378e7c58761a7e5980c09f65b15b5b8caea5d631f9e533c04d33b71961e5ad7b27e0f1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955039054410000000000000000f1b4815c0000000090fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0c000148656c6c6f20776f726c64210500000000000000e803000000000000'),
        ]

        for type, payload in transactions:
            transaction = models.Transaction.from_catbuffer(payload)
            self.assertEqual(transaction.type, type)

    def test_from_dto(self):
        transactions = [
            # TODO(ahuszagh) Add more transactions here...
            (models.TransactionType.SECRET_LOCK, {
                'transaction': {
                    'version': 36865,
                    'type': 16722,
                    'maxFee': [0, 0],
                    'deadline': [1552004337, 0],
                    'mosaicId': [5, 0],
                    'amount': [1000, 0],
                    'duration': [100, 0],
                    'hashAlgorithm': 0,
                    'secret': '9b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e',
                    'recipient': '90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
                },
            }),
            (models.TransactionType.SECRET_PROOF, {
                'transaction': {
                    'version': 36865,
                    'type': 16978,
                    'maxFee': [0, 0],
                    'deadline': [1552004337, 0],
                    'hashAlgorithm': 0,
                    'secret': '9b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e',
                    'proof': 'b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
                },
            }),
            (models.TransactionType.TRANSFER, {
                'transaction': {
                    'version': 36867,
                    'type': 16724,
                    'maxFee': [0, 0],
                    'deadline': [1552004337, 0],
                    'recipient': '914bfa5f372d55b38400000000000000000000000000000000',
                    'mosaics': [{'amount': [1000, 0], 'id': [5, 0]}],
                    'message': {'type': 0, 'payload': '48656c6c6f20776f726c6421'}
                },
            }),
        ]

        for type, dto in transactions:
            transaction = models.Transaction.from_dto(dto)
            self.assertEqual(transaction.type, type)

    # TODO(ahuszagh) Need to test the hooks.
    # Implement...
    #   has_missing_signatures


@harness.model_test_case({
    'type': models.TransactionAnnounceResponse,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'message': 'Hello world!',
    },
    'dto': {
        'message': 'Hello world!',
    },
})
class TestTransactionAnnounceResponse(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.TransactionInfo,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'height': 1,
        'index': 0,
        'id': '5c7c06ff5cc1fe000176fa12',
        'hash': 'b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5',
        'merkle_component_hash': 'b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5',
    },
    'dto': {
        'height': [1, 0],
        'index': 0,
        'id': '5c7c06ff5cc1fe000176fa12',
        'hash': 'b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5',
        'merkleComponentHash': 'b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5',
    },
})
class TestTransactionInfo(harness.TestCase):

    def test_init_args(self):
        self.type(1, 0, '5c7c06ff5cc1fe000176fa12')
        self.type(1, 0, '5c7c06ff5cc1fe000176fa12', None)
        self.type(1, 0, '5c7c06ff5cc1fe000176fa12', None, None)

    def test_is_unconfirmed(self):
        self.assertFalse(self.model.is_unconfirmed())
        unconfirmed = self.model.replace(height=0, hash=None, merkle_component_hash=None)
        self.assertTrue(unconfirmed.is_unconfirmed())

    def test_is_confirmed(self):
        self.assertTrue(self.model.is_confirmed())
        unconfirmed = self.model.replace(height=0)
        self.assertFalse(unconfirmed.is_confirmed())

    def test_has_missing_signatures(self):
        self.assertFalse(self.model.has_missing_signatures())
        missing = self.model.replace(height=0, merkle_component_hash='6a970a2e522bc32ed50590251c62fb6c9f934cb57f1266b0db4ec963ff2de2fe')
        self.assertTrue(missing.has_missing_signatures())


@harness.model_test_case({
    'type': models.TransactionStatus,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'group': models.TransactionStatusGroup.CONFIRMED,
        'status': 'Success',
        'hash': 'b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5',
        'deadline': models.Deadline.from_timestamp(1),
        'height': 1,
    },
    'dto': {
        'group': 'confirmed',
        'status': 'Success',
        'hash': 'b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5',
        'deadline': [1, 0],
        'height': [1, 0],
    },
})
class TestTransactionStatus(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.TransactionStatusError,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'hash': 'b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5',
        'status': 'Success',
        'deadline': models.Deadline.from_timestamp(1),
    },
    'dto': {
        'hash': 'b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5',
        'status': 'Success',
        'deadline': [1, 0],
    },
})
class TestTransactionStatusError(harness.TestCase):
    pass


@harness.enum_test_case({
    'type': models.TransactionStatusGroup,
    'enums': [
        models.TransactionStatusGroup.FAILED,
        models.TransactionStatusGroup.UNCONFIRMED,
        models.TransactionStatusGroup.CONFIRMED,
    ],
    'values': [
        'failed',
        'unconfirmed',
        'confirmed',
    ],
    'descriptions': [
        'Transaction failed.',
        'Transaction not yet confirmed.',
        'Transaction confirmed.',
    ],
    'dto': [
        'failed',
        'unconfirmed',
        'confirmed',
    ],
})
class TestTransactionStatusGroup(harness.TestCase):
    pass


@harness.enum_test_case({
    'type': models.TransactionType,
    'enums': [
        models.TransactionType.TRANSFER,
        models.TransactionType.SECRET_PROOF,
    ],
    'values': [
        0x4154,
        0x4252,
    ],
    'descriptions': [
        'Transfer Transaction transaction type.',
        'Secret Proof transaction type.',
    ],
    'dto': [
        0x4154,
        0x4252,
    ],
    'catbuffer': [
        b'\x54\x41',
        b'\x52\x42',
    ],
})
class TestTransactionType(harness.TestCase):
    pass


@harness.enum_test_case({
    'type': models.TransactionVersion,
    'enums': [
        models.TransactionVersion.SECRET_PROOF,
        models.TransactionVersion.AGGREGATE_BONDED,
        models.TransactionVersion.TRANSFER,
    ],
    'values': [
        1,
        2,
        3,
    ],
    'descriptions': [
        'Transaction version 1.',
        'Transaction version 2.',
        'Transaction version 3.',
    ],
    'dto': [
        1,
        2,
        3,
    ],
    'catbuffer': [
        b'\x01',
        b'\x02',
        b'\x03',
    ],
})
class TestTransactionVersion(harness.TestCase):
    pass


@harness.transaction_test_case({
    'type': models.TransferTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.TRANSFER,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'recipient': models.Address('SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54'),
        'mosaics': [models.Mosaic(models.MosaicId(5), 1000)],
        'message': models.PlainMessage(b'Hello world!'),
    },
    'dto': {
        'transaction': {
            'version': 36867,
            'type': 16724,
            'maxFee': [0, 0],
            'deadline': [1552004337, 0],
            'recipient': '90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
            'mosaics': [{'amount': [1000, 0], 'id': [5, 0]}],
            'message': {'type': 0, 'payload': '48656c6c6f20776f726c6421'}
        },
    },
    'catbuffer': 'b0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000039054410000000000000000f1b4815c0000000090fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0c000148656c6c6f20776f726c64210500000000000000e803000000000000',
    'extras': {
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': 'b0000000edbf8094c382ddb1c2341ea861ad979eee4b576b1050bfb5b306cf07d6b378e7c58761a7e5980c09f65b15b5b8caea5d631f9e533c04d33b71961e5ad7b27e0f1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955039054410000000000000000f1b4815c0000000090fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0c000148656c6c6f20776f726c64210500000000000000e803000000000000',
            'hash': '8e5128947c53cd6a7fe537b3d038a9a804b8d1e7827704538c1c95bf0d01703e',
        },
        'embedded': '600000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550390544190fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0c000148656c6c6f20776f726c64210500000000000000e803000000000000',
    },
})
class TestTransferTransaction(harness.TestCase):

    def test_create(self):
        self.assertEqual(self.model, self.type.create(
            deadline=self.data['deadline'],
            recipient=self.data['recipient'],
            mosaics=self.data['mosaics'],
            message=self.data['message'],
            network_type=self.data['network_type'],
        ))

    def test_invalid_network_type(self):
        with self.assertRaises(ValueError):
            self.model.to_catbuffer(models.NetworkType.MIJIN)
        with self.assertRaises(ValueError):
            self.type.from_catbuffer(self.catbuffer, models.NetworkType.MIJIN)
        with self.assertRaises(ValueError):
            self.model.to_dto(models.NetworkType.MIJIN)
        with self.assertRaises(ValueError):
            self.type.from_dto(self.dto, models.NetworkType.MIJIN)
        with self.assertRaises(ValueError):
            self.type.from_catbuffer(b'', self.network_type)
        with self.assertRaises(ValueError):
            size = util.hexlify(util.u32_to_catbuffer(1 << 31))
            catbuffer = size + self.catbuffer[8:]
            self.type.from_catbuffer(catbuffer, self.network_type)


@harness.transaction_test_case({
    'type': models.TransferTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.TRANSFER,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'recipient': models.Address('SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54'),
        'mosaics': [models.Mosaic(models.MosaicId(5), 1000)],
        'message': models.PlainMessage(b'Hello world!'),
        'transaction_info': models.TransactionInfo(
            height=1,
            index=0,
            id='5c7c06ff5cc1fe000176fa12',
            hash='b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5',
            merkle_component_hash='b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5',
        )
    },
    'dto': {
        'meta': {
            "height": [1, 0],
            "hash": "b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5",
            "merkleComponentHash": "b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5",
            "index": 0,
            "id": "5c7c06ff5cc1fe000176fa12"
        },
        'transaction': {
            'version': 36867,
            'type': 16724,
            'maxFee': [0, 0],
            'deadline': [1552004337, 0],
            'recipient': '90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
            'mosaics': [{'amount': [1000, 0], 'id': [5, 0]}],
            'message': {'type': 0, 'payload': '48656c6c6f20776f726c6421'}
        },
    },
    'to_aggregate': False,
    'sign_with': False,
})
class TestTransferTransactionWithInfo(harness.TestCase):

    def test_is_unconfirmed(self):
        self.assertFalse(self.model.is_unconfirmed())

    def test_is_confirmed(self):
        self.assertTrue(self.model.is_confirmed())

    def test_has_missing_signatures(self):
        self.assertFalse(self.model.has_missing_signatures())


@harness.transaction_test_case({
    'type': models.TransferTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.TRANSFER,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'recipient': models.NamespaceId(0x84b3552d375ffa4b),
        'mosaics': [models.Mosaic(models.MosaicId(5), 1000)],
        'message': models.PlainMessage(b'Hello world!'),
    },
    'dto': {
        'transaction': {
            'version': 36867,
            'type': 16724,
            'maxFee': [0, 0],
            'deadline': [1552004337, 0],
            'recipient': '914bfa5f372d55b38400000000000000000000000000000000',
            'mosaics': [{'amount': [1000, 0], 'id': [5, 0]}],
            'message': {'type': 0, 'payload': '48656c6c6f20776f726c6421'}
        },
    },
    'catbuffer': 'b0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000039054410000000000000000f1b4815c00000000914bfa5f372d55b384000000000000000000000000000000000c000148656c6c6f20776f726c64210500000000000000e803000000000000',
    'extras': {
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': 'b0000000d49313b969bd1c1ab1a686f43560a83f389eb03fde5afa4c41441c803c44563056e26457d36f42b1c3a80f9966370566c0f5c6bbd92c8093893719800fa8ec0f1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955039054410000000000000000f1b4815c00000000914bfa5f372d55b384000000000000000000000000000000000c000148656c6c6f20776f726c64210500000000000000e803000000000000',
            'hash': 'ea2de6084919d5472291ff20ce0598a64b5ca7dd8ea2f796433e94a992826f15',
        },
        'embedded': '600000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895503905441914bfa5f372d55b384000000000000000000000000000000000c000148656c6c6f20776f726c64210500000000000000e803000000000000',
    },
})
class TestTransferTransactionWithNamespace(harness.TestCase):

    def test_is_unannounced(self):
        self.assertTrue(self.model.is_unannounced())
