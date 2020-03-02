import datetime
import random

from xpxchain import util
from xpxchain import models
from tests import harness


def psuedo_entropy(size: int) -> bytes:
    return bytes([random.randint(0, 255) for _ in range(size)])


@harness.transaction_test_case({
    'type': models.AccountLinkTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.LINK_ACCOUNT,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'remote_account_key': 'a5f82ec8ebb341427b6785c8111906cd0df18838fb11b51ce0e18b5e79dff630',
        'link_action': models.LinkAction.LINK,
    },
    'dto': {
        'transaction': {
            'version': 2415919106,
            'type': 16716,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'remoteAccountKey': 'a5f82ec8ebb341427b6785c8111906cd0df18838fb11b51ce0e18b5e79dff630',
            'action': 0,
        },
    },
    'catbuffer': '9b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000904c410000000000000000683d8c8b15000000a5f82ec8ebb341427b6785c8111906cd0df18838fb11b51ce0e18b5e79dff63000',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '9b000000da8b880f04f6fc6216b1760d2130ab44455b815b0fb8f2c70533cece3c8aa5605326120fdc25f635a4aa8d507b029c0e861872338b89fbdb5cbf3e917d1c2f0e1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955020000904c410000000000000000683d8c8b15000000a5f82ec8ebb341427b6785c8111906cd0df18838fb11b51ce0e18b5e79dff63000',
            'hash': 'bc9be54535d29f46654c65b5d3238359c1304bf3e1c3b8e51b936e105d4c60ee',
        },
        'embedded': '4b0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955020000904c41a5f82ec8ebb341427b6785c8111906cd0df18838fb11b51ce0e18b5e79dff63000',
    },
})
class TestAccountLinkTransaction(harness.TestCase):

    def test_create(self):
        self.assertEqual(self.model, self.type.create(
            deadline=self.data['deadline'],
            remote_account_key=self.data['remote_account_key'],
            link_action=self.data['link_action'],
            network_type=self.data['network_type'],
        ))


@harness.model_test_case({
    'type': models.AccountPropertyModification,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'modification_type': models.PropertyModificationType.ADD,
        'value': models.Address('SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG'),
    },
    'dto': {
        'type': 0,
        'value': 'SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG',
    },
})
class TestAccountPropertyModificationAddress(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.AccountPropertyModification,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'modification_type': models.PropertyModificationType.ADD,
        'value': models.MosaicId.create_from_hex('941299b2b7e1291c'),
    },
    'dto': {
        'type': 0,
        'value': [3084986652, 2484246962],
    },
})
class TestAccountPropertyModificationMosaic(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.AccountPropertyModification,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'modification_type': models.PropertyModificationType.ADD,
        'value': models.TransactionType.LOCK,
    },
    'dto': {
        'type': 0,
        'value': 0x4148,
    },
    'eq': False,
})
class TestAccountPropertyModificationTransaction(harness.TestCase):
    pass


class TestAccountPropertyTransaction(harness.TestCase):

    def setUp(self):
        self.type = models.AccountPropertyTransaction
        self.network_type = models.NetworkType.MIJIN_TEST
        self.deadline = models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57))
        self.modification_type = models.PropertyModificationType.ADD
        self.address = models.Address('SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG')
        self.mosaic = models.MosaicId.create_from_hex('6c699a1517bea955')
        self.entity_type = models.TransactionType.LOCK

    def test_create_address_property_modification_transaction(self):
        modifications = [
            models.AccountPropertyModification(self.modification_type, self.address)
        ]
        model = self.type.create_address_property_modification_transaction(
            deadline=self.deadline,
            property_type=models.PropertyType.ALLOW_ADDRESS,
            modifications=modifications,
            network_type=self.network_type,
        )
        catbuffer = util.hexlify(model.to_catbuffer(self.network_type, fee_strategy=util.FeeCalculationStrategy.ZERO))
        self.assertEqual(catbuffer, '960000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100009050410000000000000000683d8c8b15000000010100902891202271567a65166877a647d8a5ffd3bbe630ab925e46')

    def test_create_mosaic_property_modification_transaction(self):
        modifications = [
            models.AccountPropertyModification(self.modification_type, self.mosaic)
        ]
        model = self.type.create_mosaic_property_modification_transaction(
            deadline=self.deadline,
            property_type=models.PropertyType.ALLOW_MOSAIC,
            modifications=modifications,
            network_type=self.network_type,
        )
        catbuffer = util.hexlify(model.to_catbuffer(self.network_type, fee_strategy=util.FeeCalculationStrategy.ZERO))
        self.maxDiff = 2048
        self.assertEqual(catbuffer, '850000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100009050420000000000000000683d8c8b1500000002010055a9be17159a696c')

    def test_create_entity_type_property_modification_transaction(self):
        modifications = [
            models.AccountPropertyModification(self.modification_type, self.entity_type)
        ]
        model = self.type.create_entity_type_property_modification_transaction(
            deadline=self.deadline,
            property_type=models.PropertyType.ALLOW_TRANSACTION,
            modifications=modifications,
            network_type=self.network_type,
        )
        catbuffer = util.hexlify(model.to_catbuffer(self.network_type, fee_strategy=util.FeeCalculationStrategy.ZERO))
        self.maxDiff = 2048
        self.assertEqual(catbuffer, '7f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100009050430000000000000000683d8c8b150000000401004841')

    def test_create_address_filter(self):
        model = models.AccountPropertyModification(self.modification_type, self.address)
        self.assertEqual(model, self.type.create_address_filter(
            self.modification_type,
            self.address
        ))

    def test_create_mosaic_filter(self):
        model = models.AccountPropertyModification(self.modification_type, self.mosaic)
        self.assertEqual(model, self.type.create_mosaic_filter(
            self.modification_type,
            self.mosaic
        ))

    def test_create_entity_type_filter(self):
        model = models.AccountPropertyModification(self.modification_type, self.entity_type)
        self.assertEqual(model, self.type.create_entity_type_filter(
            self.modification_type,
            self.entity_type
        ))


@harness.transaction_test_case({
    'type': models.AddressAliasTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.ADDRESS_ALIAS,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'action_type': models.AliasActionType.LINK,
        'namespace_id': models.NamespaceId(0x88B64C3BE2F47144),
        'address': models.Address('SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54'),
    },
    'catbuffer': '9c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000904e420000000000000000683d8c8b15000000004471f4e23b4cb68890fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '9c000000e07eee928115f9ab626cb15a2024172923e7dac8e06dc84fcc958d7ce2b8b083a9c3514a83439f5526fda3eb511ba276d648d7f94f3ad640ed3729e5143012051b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955010000904e420000000000000000683d8c8b15000000004471f4e23b4cb68890fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
            'hash': '9faf9cf9929dfd914ffe95d3212fca46f0b61ac567deea790cc1c8b863fadc59',
        },
        'embedded': '4c0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955010000904e42004471f4e23b4cb68890fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
    },
})
class TestAddressAliasTransaction(harness.TestCase):

    def test_create(self):
        self.assertEqual(self.model, self.type.create(
            deadline=self.data['deadline'],
            action_type=self.data['action_type'],
            namespace_id=self.data['namespace_id'],
            address=self.data['address'],
            network_type=self.data['network_type'],
        ))


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
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
    },
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

    def test_create_for_address(self):
        network_type = models.NetworkType.MIJIN_TEST
        type = models.AliasTransaction
        model = type.create_for_address(
            deadline=models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
            action_type=models.AliasActionType.LINK,
            namespace_id=models.NamespaceId(0x88B64C3BE2F47144),
            address=models.Address('SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54'),
            network_type=network_type,
        )
        catbuffer = '9c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000904e420000000000000000683d8c8b15000000004471f4e23b4cb68890fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc'
        self.maxDiff = 2048
        self.assertEqual(catbuffer, util.hexlify(model.to_catbuffer(network_type, fee_strategy=util.FeeCalculationStrategy.ZERO)))

    def test_create_for_mosaic(self):
        network_type = models.NetworkType.MIJIN_TEST
        type = models.AliasTransaction
        model = type.create_for_mosaic(
            deadline=models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
            action_type=models.AliasActionType.LINK,
            namespace_id=models.NamespaceId(0x88B64C3BE2F47144),
            mosaic_id=models.MosaicId(0x2FF7D64F483BC0A6),
            network_type=network_type,
        )
        catbuffer = '8b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000904e430000000000000000683d8c8b15000000004471f4e23b4cb688a6c03b484fd6f72f'
        self.maxDiff = 2048
        self.assertEqual(catbuffer, util.hexlify(model.to_catbuffer(network_type, fee_strategy=util.FeeCalculationStrategy.ZERO)))


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
})
class TestDeadline(harness.TestCase):

    def test_create(self):
        with self.assertRaises(ValueError):
            self.type.create(-1)
        with self.assertRaises(ValueError):
            self.type.create(25, models.ChronoUnit.HOURS)

        self.type.create(23, models.ChronoUnit.HOURS)


class TestHashLockTransaction(harness.TestCase):

    def test_create(self):
        def create(cls):
            return cls.create(
                deadline=models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
                mosaic=models.Mosaic(models.MosaicId.create_from_hex('941299b2b7e1291c'), 1000),
                duration=1000,
                signed_transaction=models.SignedTransaction.create_from_announced(
                    '8ed5521912d32097e4f9b172fab4200966a99c72910b839bff934e0c3ac219e0',
                    models.TransactionType.AGGREGATE_BONDED,
                    models.NetworkType.MIJIN_TEST,
                ),
                network_type=models.NetworkType.MIJIN_TEST,
            )

        self.assertEqual(create(models.HashLockTransaction), create(models.LockFundsTransaction))


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
        self.assertEqual(models.InnerTransaction.catbuffer_size_shared(), 42)

    def test_create_from_catbuffer(self):
        transactions = [
            # TODO: get new catbuffers
            # (models.TransactionType.ADDRESS_ALIAS, '4a0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955010000904e42004471f4e23b4cb68890fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc'),
            # (models.TransactionType.MOSAIC_ALIAS, '390000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501904e43004471f4e23b4cb688a6c03b484fd6f72f'),
            # (models.TransactionType.SECRET_PROOF, '6b0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501905242009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'),
            # (models.TransactionType.TRANSFER, '600000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550390544190fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0c000148656c6c6f20776f726c64210500000000000000e803000000000000'),
        ]

        for type, payload in transactions:
            transaction = models.InnerTransaction.create_from_catbuffer(payload)
            self.assertEqual(transaction.type, type)


@harness.enum_test_case({
    'type': models.LinkAction,
    'enums': [
        models.LinkAction.LINK,
        models.LinkAction.UNLINK,
    ],
    'values': [
        0,
        1,
    ],
    'descriptions': [
        'Link an account.',
        'Unlink an account.',
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
class TestLinkAction(harness.TestCase):
    pass


@harness.transaction_test_case({
    'type': models.LockFundsTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.LOCK,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'mosaic': models.Mosaic(models.MosaicId.create_from_hex('941299b2b7e1291c'), 1000),
        'duration': 1000,
        'signed_transaction': models.SignedTransaction.create_from_announced(
            '8ed5521912d32097e4f9b172fab4200966a99c72910b839bff934e0c3ac219e0',
            models.TransactionType.AGGREGATE_BONDED,
            models.NetworkType.MIJIN_TEST,
        ),
    },
    'dto': {
        'transaction': {
            'version': 2415919105,
            'type': 16712,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'hash': '8ed5521912d32097e4f9b172fab4200966a99c72910b839bff934e0c3ac219e0',
            'mosaicId': [3084986652, 2484246962],
            'amount': [1000, 0],
            'duration': [1000, 0],
        },
    },
    'catbuffer': 'b20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100009048410000000000000000683d8c8b150000001c29e1b7b2991294e803000000000000e8030000000000008ed5521912d32097e4f9b172fab4200966a99c72910b839bff934e0c3ac219e0',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': 'b2000000c56516dfd24967dbaa36793c5cff169ad4ed558f609a4facbc9de8b096a84899b43bced1afbfdf040e476ff748b0f92607c6e3df2de0dc74bd25c1706056dd061b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550100009048410000000000000000683d8c8b150000001c29e1b7b2991294e803000000000000e8030000000000008ed5521912d32097e4f9b172fab4200966a99c72910b839bff934e0c3ac219e0',
            'hash': 'b94fb91607af9c902087084b176cdaa01de818132bad386ee76f80a61e7dff9e',
        },
        'embedded': '620000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550100009048411c29e1b7b2991294e803000000000000e8030000000000008ed5521912d32097e4f9b172fab4200966a99c72910b839bff934e0c3ac219e0',
    },
})
class TestLockFundsTransaction(harness.TestCase):

    def test_create(self):
        self.maxDiff = 2048
        self.assertEqual(self.model, self.type.create(
            deadline=self.data['deadline'],
            mosaic=self.data['mosaic'],
            duration=self.data['duration'],
            signed_transaction=self.data['signed_transaction'],
            network_type=self.data['network_type'],
        ))


class TestMessage(harness.TestCase):

    def test_create(self):
        with self.assertRaises(NotImplementedError):
            models.Message.create(b'Hello world!')

    def test_dto(self):
        dto = {'payload': util.hexlify(b'Hello world!'), 'type': 0}
        with self.assertRaises(NotImplementedError):
            models.Message.create_from_dto(dto, models.NetworkType.MIJIN_TEST)


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


@harness.transaction_test_case({
    'type': models.ModifyAccountPropertyAddressTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.MODIFY_ACCOUNT_PROPERTY_ADDRESS,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'property_type': models.PropertyType.ALLOW_ADDRESS,
        'modifications': [
            models.AccountPropertyModification(
                modification_type=models.PropertyModificationType.ADD,
                value=models.Address('SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG'),
            ),
        ],
    },
    'dto': {
        'transaction': {
            'version': 2415919105,
            'type': 16720,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'propertyType': 1,
            'modifications': [
                {
                    'type': 0,
                    'value': 'SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG',
                },
            ],
        },
    },
    'catbuffer': '960000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100009050410000000000000000683d8c8b15000000010100902891202271567a65166877a647d8a5ffd3bbe630ab925e46',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '960000005e178076936e4abdf9a73c822bf090ae64c16f1372a7faf60065f623507cc619a9aef07a9c4c2c52e5022ac1c410523a10a9373c059e986d570d5b6664ff8a071b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550100009050410000000000000000683d8c8b15000000010100902891202271567a65166877a647d8a5ffd3bbe630ab925e46',
            'hash': '69c310ab9d454ad7e0a8f69cb53456d80204a9d76c4d4c67b1e622bcd923593f',
        },
        'embedded': '460000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955010000905041010100902891202271567a65166877a647d8a5ffd3bbe630ab925e46',
    },
})
class TestModifyAccountPropertyAddressTransaction(harness.TestCase):

    def test_create(self):
        self.assertEqual(self.model, self.type.create(
            deadline=self.data['deadline'],
            property_type=self.data['property_type'],
            modifications=self.data['modifications'],
            network_type=self.data['network_type'],
        ))


@harness.transaction_test_case({
    'type': models.ModifyAccountPropertyEntityTypeTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.MODIFY_ACCOUNT_PROPERTY_ENTITY_TYPE,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'property_type': models.PropertyType.ALLOW_TRANSACTION,
        'modifications': [
            models.AccountPropertyModification(
                modification_type=models.PropertyModificationType.ADD,
                value=models.TransactionType.LOCK,
            ),
        ],
    },
    'dto': {
        'transaction': {
            'version': 2415919105,
            'type': 17232,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'propertyType': 4,
            'modifications': [
                {
                    'type': 0,
                    'value': 16712,
                },
            ],
        },
    },
    'catbuffer': '7f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100009050430000000000000000683d8c8b150000000401004841',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '7f000000043c126fd11a98ba436ba6d2500fabeadf24cd3cf4cad00a1b9f51ba9c1980800fe659256567e34674fc9a124dd967c15d935ac4b8bdbeed12179241780218011b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550100009050430000000000000000683d8c8b150000000401004841',
            'hash': 'fdc718d5c55823800624c7c5e13382c1128803af4ff3a9dcbc383d83f658825f',
        },
        'embedded': '2f0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550100009050430401004841',
    },
})
class TestModifyAccountPropertyEntityTypeTransaction(harness.TestCase):

    def test_create(self):
        self.assertEqual(self.model, self.type.create(
            deadline=self.data['deadline'],
            property_type=self.data['property_type'],
            modifications=self.data['modifications'],
            network_type=self.data['network_type'],
        ))


@harness.transaction_test_case({
    'type': models.ModifyAccountPropertyMosaicTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.MODIFY_ACCOUNT_PROPERTY_MOSAIC,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'property_type': models.PropertyType.ALLOW_MOSAIC,
        'modifications': [
            models.AccountPropertyModification(
                modification_type=models.PropertyModificationType.ADD,
                value=models.MosaicId.create_from_hex('6c699a1517bea955'),
            ),
        ],
    },
    'dto': {
        'transaction': {
            'version': 2415919105,
            'type': 16976,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'propertyType': 2,
            'modifications': [
                {
                    'type': 0,
                    'value': [398371157, 1818860053],
                },
            ],
        },
    },
    'catbuffer': '850000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100009050420000000000000000683d8c8b1500000002010055a9be17159a696c',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '85000000109cb27774f3b6d8156341410fe6d87c61b738ee157fffe4e1c5911b2f61e6e54563ee84016cee52cb15860bed2ac4add750f2b1b995334d5fb8c2b8453b52011b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550100009050420000000000000000683d8c8b1500000002010055a9be17159a696c',
            'hash': 'f63dbaf924c4009885bceba70c28f42d9544bcd415f3f9f57f0bde5d075e07a1',
        },
        'embedded': '350000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501000090504202010055a9be17159a696c',
    },
})
class TestModifyAccountPropertyMosaicTransaction(harness.TestCase):

    def test_create(self):
        self.assertEqual(self.model, self.type.create(
            deadline=self.data['deadline'],
            property_type=self.data['property_type'],
            modifications=self.data['modifications'],
            network_type=self.data['network_type'],
        ))


@harness.transaction_test_case({
    'type': models.ModifyMultisigAccountTransaction,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'network_type': models.NetworkType.MIJIN_TEST,
        'version': models.TransactionVersion.MODIFY_MULTISIG_ACCOUNT,
        'deadline': models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57)),
        'max_fee': 0,
        'signature': None,
        'signer': None,
        'transaction_info': None,
        'min_approval_delta': 0,
        'min_removal_delta': 1,
        'modifications': [
            models.MultisigCosignatoryModification(
                type=models.MultisigCosignatoryModificationType.ADD,
                cosignatory_public_account=models.PublicAccount.create_from_public_key('1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955', models.NetworkType.MIJIN_TEST),
            ),
        ],
    },
    'dto': {
        'transaction': {
            'version': 2415919107,
            'type': 16725,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'minApprovalDelta': 0,
            'minRemovalDelta': 1,
            'modifications': [
                {
                    'cosignatoryPublicKey': '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
                    'type': 0
                }
            ],
        },
    },
    'catbuffer': '9e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300009055410000000000000000683d8c8b15000000010001001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '9e000000b7485514d9e93ae38e03401d3d3c73456b7377d0057a0683fa01bb8df245e2663dd73eed66d3b9e4e94a6359edd3a86acf952ca23ced55e62360bbcf379e04081b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550300009055410000000000000000683d8c8b15000000010001001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
            'hash': '2f85e03940b0be7eaab92ba20f76d64d1eb465da7dcd747f9fa03b9ed326cb75',
        },
        'embedded': '4e0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955030000905541010001001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
    },
})
class TestModifyMultisigAccountTransaction(harness.TestCase):

    def test_create(self):
        self.assertEqual(self.model, self.type.create(
            deadline=self.data['deadline'],
            min_approval_delta=self.data['min_approval_delta'],
            min_removal_delta=self.data['min_removal_delta'],
            modifications=self.data['modifications'],
            network_type=self.data['network_type'],
        ))


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
    'catbuffer': '8b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000904e430000000000000000683d8c8b15000000004471f4e23b4cb688a6c03b484fd6f72f',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '8b000000c5128f327f36a2ed1aa3bfdf6fe175271545f2421526a745d0ebdbc419b22106a19e61326b4874c11ed34355a4b4ef8483e0a37218138413f54402c2dfda6b0e1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955010000904e430000000000000000683d8c8b15000000004471f4e23b4cb688a6c03b484fd6f72f',
            'hash': '34ea259da822d386e11cdba4d8a6dbe3e176f9e14440a6b75ae4126d54970354',
        },
        'embedded': '3b0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955010000904e43004471f4e23b4cb688a6c03b484fd6f72f',
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
        'mosaic_id': models.MosaicId.create_from_hex('6c699a1517bea955'),
        'mosaic_properties': models.MosaicProperties(0x3, 3),
    },
    'dto': {
        'transaction': {
            'version': 2415919107,
            'type': 16717,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'mosaicNonce': 1,
            'mosaicId': [398371157, 1818860053],
            'properties': [
                {'id': 0, 'value': [3, 0]},
                {'id': 1, 'value': [3, 0]},
            ],
        },
    },
    'catbuffer': '89000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000030000904d410000000000000000683d8c8b150000000100000055a9be17159a696c000303',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '8900000033650e24defd3b0b3f2bd971550429d7b831f0f41fb62cc88c4e19dc85d01fa6cd925129b57119103893c443b672a0e4470518dbc0e2695a1d70f30cc4e007091b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955030000904d410000000000000000683d8c8b150000000100000055a9be17159a696c000303',
            'hash': 'cb42ff5ff260c79901442eb90092095025e3e540b7fadc8ef2cb25aff448e052',
        },
        'embedded': '390000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955030000904d410100000055a9be17159a696c000303',
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
        'mosaic_id': models.MosaicId.create_from_hex('941299b2b7e1291c'),
        'direction': models.MosaicSupplyType.INCREASE,
        'delta': 15000000,
    },
    'dto': {
        'transaction': {
            'version': 2415919106,
            'type': 16973,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'mosaicId': [3084986652, 2484246962],
            'direction': 1,
            'delta': [15000000, 0],
        },
    },
    'catbuffer': '8b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000904d420000000000000000683d8c8b150000001c29e1b7b299129401c0e1e40000000000',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '8b0000009546bd4b208cac19785f938f8a107c748a4b8e19ec9989f1784c0cd7ec14347c6862014c59c082688bfdecc8f904cce7251c1b1b774201fdd12809aef90d310f1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955020000904d420000000000000000683d8c8b150000001c29e1b7b299129401c0e1e40000000000',
            'hash': 'c54d8c1b184d9e22909972c43706588c750606d5b79cbff6b79e2bc37e5c70ca',
        },
        'embedded': '3b0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955020000904d421c29e1b7b299129401c0e1e40000000000',
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
    'catbuffer': '0048656c6c6f20776f726c6421',
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
        'namespace_name': 'sample',
        'namespace_id': models.NamespaceId('sample'),
    },
    'dto': {
        'transaction': {
            'version': 2415919106,
            'type': 16718,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'namespaceType': 0,
            'duration': [100, 0],
            'namespaceId': [0xe2f47144, 0x88b64c3b],
            'name': 'sample',
        },
    },
    'catbuffer': '92000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000904e410000000000000000683d8c8b150000000064000000000000004471f4e23b4cb6880673616d706c65',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '92000000407622ce5efcc201aa494975cdcace45688a24fdb671c5511ad1013773b056856e297a05da8cf272232edfb2ac1d709fea66724025689cf9df1c459fef57920c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955020000904e410000000000000000683d8c8b150000000064000000000000004471f4e23b4cb6880673616d706c65',
            'hash': '52fd74c5c1ef28d0fd9312ad7fcd62f195330bef0e8432808c421bd7a4bc8793',
        },
        'embedded': '420000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955020000904e410064000000000000004471f4e23b4cb6880673616d706c65',
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

    def test_create_root_namespace(self):
        self.assertEqual(self.model, self.type.create_root_namespace(
            deadline=self.data['deadline'],
            namespace_name=self.data['namespace_name'],
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
        'namespace_name': 'sub',
        'namespace_id': models.NamespaceId('sample.sub'),
    },
    'dto': {
        'transaction': {
            'version': 2415919106,
            'type': 16718,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'namespaceType': 1,
            'parentId': [0xe2f47144, 0x88b64c3b],
            'namespaceId': [0x5a71acc9, 0xfa942971],
            'name': 'sub',
        },
    },
    'catbuffer': '8f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000904e410000000000000000683d8c8b15000000014471f4e23b4cb688c9ac715a712994fa03737562',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': '8f0000006b886b248c931fcc9d1a349e54bd41bd3a0677a9b09f5d152f21c0d2c82e6dbf7480e6a6d7234b5d60ddda570ca718874afe71ac7d2f92a8b38b548f9545710a1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955020000904e410000000000000000683d8c8b15000000014471f4e23b4cb688c9ac715a712994fa03737562',
            'hash': '3c27e49964c69703aff53e70bf2d8a8390771e1eedc2cdeeb034212aaed5fe54',
        },
        'embedded': '3f0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955020000904e41014471f4e23b4cb688c9ac715a712994fa03737562',
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
            namespace_name=self.data['namespace_name'],
            parent_namespace=self.data['parent_id'],
            network_type=self.data['network_type'],
        ))

    def test_create_sub_namespace_from_name(self):
        self.assertEqual(self.model, self.type.create_sub_namespace(
            deadline=self.data['deadline'],
            namespace_name=self.data['namespace_name'],
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
            'version': 2415919105,
            'type': 16722,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'mosaicId': [5, 0],
            'amount': [1000, 0],
            'duration': [100, 0],
            'hashAlgorithm': 0,
            'secret': '9b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e',
            'recipient': '90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
        },
    },
    'catbuffer': 'cc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100009052410000000000000000683d8c8b150000000500000000000000e8030000000000006400000000000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': 'cc000000c75de9648e8bef81e6ae8095a407a2061accd0076cec921dce8a1ee41d9fa507880b976528adbcbce2217ff49b93624613cc5bb02eb415d18d5a0a7e9b4292021b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550100009052410000000000000000683d8c8b150000000500000000000000e8030000000000006400000000000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
            'hash': '925c09511eba1c9dec4a15dcdf964dab61e4ec021d66830215691356938d6a4a',
        },
        'embedded': '7c0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550100009052410500000000000000e8030000000000006400000000000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
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
        'recipient': models.Address('SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54'),
        'secret': '9b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e',
        'proof': 'b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
    },
    'dto': {
        'transaction': {
            'version': 2415919105,
            'type': 16978,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'hashAlgorithm': 0,
            'recipient': '90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
            'secret': '9b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e',
            'proof': 'b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
        },
    },
    'catbuffer': 'd60000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100009052420000000000000000683d8c8b15000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': 'd60000009c5f59e64b1fd7e3cd81b4d16e04070b472f613e4a8ba9edabdb861725cbffe1d5e840be735b983eb7da48fc12e1a804c60f571b19ea7573962a9ae212ca4b051b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550100009052420000000000000000683d8c8b15000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
            'hash': 'b3f679ae1f2a951abee94d78d08f45d3b53fd889e0a93ac7a9e4eb7b0b8a23f7',
        },
        'embedded': '860000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955010000905242009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
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
            recipient=self.data['recipient'],
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
        hash = '4bd2226e5b1a5d532538d59ade61b354aa3d5eef94c340f248f8c9ee0580d851'
        transaction = 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.assertEqual(hash, models.Transaction.transaction_hash(transaction, gen_hash='7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'))

    def test_catbuffer_size_shared(self):
        self.assertEqual(models.Transaction.catbuffer_size_shared(), 122)

    def test_create_from_catbuffer(self):
        transactions = [
            (models.TransactionType.ADDRESS_ALIAS, '9c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000904e420000000000000000683d8c8b15000000004471f4e23b4cb68890fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc'),
            (models.TransactionType.MOSAIC_ALIAS, '8b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000904e430000000000000000683d8c8b15000000004471f4e23b4cb688a6c03b484fd6f72f'),
            (models.TransactionType.SECRET_LOCK, 'cc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100009052410000000000000000683d8c8b150000000500000000000000e8030000000000006400000000000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc'),
            (models.TransactionType.SECRET_PROOF, 'd60000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100009052420000000000000000683d8c8b15000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'),
            (models.TransactionType.TRANSFER, 'b30000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300009054410000000000000000683d8c8b1500000090fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0d00010048656c6c6f20776f726c64210500000000000000e803000000000000'),
        ]

        for type, payload in transactions:
            transaction = models.Transaction.create_from_catbuffer(payload)
            self.assertEqual(transaction.type, type)

    def test_create_from_dto(self):
        transactions = [
            # TODO(ahuszagh) Add ADDRESS_ALIAS
            (models.TransactionType.LINK_ACCOUNT, {
                'transaction': {
                    'version': 2415919106,
                    'type': 16716,
                    'maxFee': [0, 0],
                    'deadline': [2341223784, 21],
                    'remoteAccountKey': 'a5f82ec8ebb341427b6785c8111906cd0df18838fb11b51ce0e18b5e79dff630',
                    'action': 0,
                },
            }),
            (models.TransactionType.LOCK, {
                'transaction': {
                    'version': 2415919105,
                    'type': 16712,
                    'maxFee': [0, 0],
                    'deadline': [2341223784, 21],
                    'hash': '8ed5521912d32097e4f9b172fab4200966a99c72910b839bff934e0c3ac219e0',
                    'mosaicId': [3084986652, 2484246962],
                    'amount': [1000, 0],
                    'duration': [1000, 0],
                },
            }),
            (models.TransactionType.MODIFY_ACCOUNT_PROPERTY_ADDRESS, {
                'transaction': {
                    'version': 2415919105,
                    'type': 16720,
                    'maxFee': [0, 0],
                    'deadline': [2341223784, 21],
                    'propertyType': 1,
                    'modifications': [
                        {
                            'type': 0,
                            'value': 'SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG',
                        },
                    ],
                },
            }),
            (models.TransactionType.MODIFY_ACCOUNT_PROPERTY_ENTITY_TYPE, {
                'transaction': {
                    'version': 2415919105,
                    'type': 17232,
                    'maxFee': [0, 0],
                    'deadline': [2341223784, 21],
                    'propertyType': 4,
                    'modifications': [
                        {
                            'type': 0,
                            'value': 16712,
                        },
                    ],
                },
            }),
            (models.TransactionType.MODIFY_ACCOUNT_PROPERTY_MOSAIC, {
                'transaction': {
                    'version': 2415919105,
                    'type': 16976,
                    'maxFee': [0, 0],
                    'deadline': [2341223784, 21],
                    'propertyType': 2,
                    'modifications': [
                        {
                            'type': 0,
                            'value': [398371157, 1818860053],
                        },
                    ],
                },
            }),
            (models.TransactionType.MODIFY_MULTISIG_ACCOUNT, {
                'transaction': {
                    'version': 2415919107,
                    'type': 16725,
                    'maxFee': [0, 0],
                    'deadline': [2341223784, 21],
                    'minApprovalDelta': 0,
                    'minRemovalDelta': 1,
                    'modifications': [
                        {
                            'cosignatoryPublicKey': '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
                            'type': 0
                        }
                    ],
                },
            }),
            # TODO(ahuszagh) Add MOSAIC_ALIAS
            (models.TransactionType.MOSAIC_DEFINITION, {
                'transaction': {
                    'version': 2415919107,
                    'type': 16717,
                    'maxFee': [0, 0],
                    'deadline': [2341223784, 21],
                    'mosaicNonce': 1,
                    'mosaicId': [398371157, 1818860053],
                    'properties': [
                        {'id': 0, 'value': [3, 0]},
                        {'id': 1, 'value': [3, 0]},
                    ],
                },
            }),
            (models.TransactionType.MOSAIC_SUPPLY_CHANGE, {
                'transaction': {
                    'version': 2415919106,
                    'type': 16973,
                    'maxFee': [0, 0],
                    'deadline': [2341223784, 21],
                    'mosaicId': [3084986652, 2484246962],
                    'direction': 1,
                    'delta': [15000000, 0],
                },
            }),
            (models.TransactionType.REGISTER_NAMESPACE, {
                'transaction': {
                    'version': 2415919106,
                    'type': 16718,
                    'maxFee': [0, 0],
                    'deadline': [2341223784, 21],
                    'namespaceType': 0,
                    'duration': [100, 0],
                    'namespaceId': [0xe2f47144, 0x88b64c3b],
                    'name': 'sample',
                },
            }),
            (models.TransactionType.SECRET_LOCK, {
                'transaction': {
                    'version': 2415919105,
                    'type': 16722,
                    'maxFee': [0, 0],
                    'deadline': [2341223784, 21],
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
                    'version': 2415919105,
                    'type': 16978,
                    'maxFee': [0, 0],
                    'deadline': [2341223784, 21],
                    'hashAlgorithm': 0,
                    'secret': '9b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e',
                    'proof': 'b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
                    'recipient': '90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
                },
            }),
            (models.TransactionType.TRANSFER, {
                'transaction': {
                    'version': 2415919107,
                    'type': 16724,
                    'maxFee': [0, 0],
                    'deadline': [2341223784, 21],
                    'recipient': '914bfa5f372d55b38400000000000000000000000000000000',
                    'mosaics': [{'amount': [1000, 0], 'id': [5, 0]}],
                    'message': {'type': 0, 'payload': '48656c6c6f20776f726c6421'}
                },
            }),
        ]

        for type, dto in transactions:
            transaction = models.Transaction.create_from_dto(dto)
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
        'deadline': models.Deadline.create_from_timestamp(1),
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


# @harness.model_test_case({
#     'type': models.TransactionStatusError,
#     'network_type': models.NetworkType.MIJIN_TEST,
#     'data': {
#         'hash': 'b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5',
#         'status': 'Success',
#         'deadline': models.Deadline.create_from_timestamp(1),
#         'address': models.Address('SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54'),
#         'channel_name': 'status',
#     },
#     'dto': {
#         'hash': 'b2635223db45cfbb4e21cdfc359fe7f222a6e5f6000c99ca9e729db02e6661f5',
#         'status': 'Success',
#         'deadline': [1, 0],
#         'meta': {
#             'address': 'SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54',
#             'channelName': 'status',
#         },
#     },
# })
# class TestTransactionStatusError(harness.TestCase):
#     pass


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
        'Transfer transaction type.',
        'Secret proof transaction type.',
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
            'version': 2415919107,
            'type': 16724,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'recipient': '90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
            'mosaics': [{'amount': [1000, 0], 'id': [5, 0]}],
            'message': {'type': 0, 'payload': '48656c6c6f20776f726c6421'}
        },
    },
    'catbuffer': 'b30000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300009054410000000000000000683d8c8b1500000090fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0d00010048656c6c6f20776f726c64210500000000000000e803000000000000',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': 'b300000095073f43b815336fa8c3eed20ab1e8c70941c75fae30c0d2791e17200ff367e81ca867d9041334bfe8cfe22e8cbc0b2356e8b1ff4044b4502676862a51fa9d091b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550300009054410000000000000000683d8c8b1500000090fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0d00010048656c6c6f20776f726c64210500000000000000e803000000000000',
            'hash': 'b97c216f3888fd1b012c80e719fd680df77862ea24d03adb7945c85b1f0d1c77',
        },
        'embedded': '630000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895503000090544190fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc0d00010048656c6c6f20776f726c64210500000000000000e803000000000000',
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
            self.type.create_from_catbuffer(self.catbuffer, models.NetworkType.MIJIN)
        with self.assertRaises(ValueError):
            self.model.to_dto(models.NetworkType.MIJIN)
        with self.assertRaises(ValueError):
            self.type.create_from_dto(self.dto, models.NetworkType.MIJIN)
        with self.assertRaises(ValueError):
            self.type.create_from_catbuffer(b'', self.network_type)
        with self.assertRaises(ValueError):
            size = util.hexlify(util.u32_to_catbuffer(1 << 31))
            catbuffer = size + self.catbuffer[8:]
            self.type.create_from_catbuffer(catbuffer, self.network_type)


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
            'version': 2415919107,
            'type': 16724,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
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
            'version': 2415919107,
            'type': 16724,
            'maxFee': [0, 0],
            'deadline': [2341223784, 21],
            'recipient': '914bfa5f372d55b38400000000000000000000000000000000',
            'mosaics': [{'amount': [1000, 0], 'id': [5, 0]}],
            'message': {'type': 0, 'payload': '48656c6c6f20776f726c6421'}
        },
    },
    'catbuffer': 'b30000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300009054410000000000000000683d8c8b15000000914bfa5f372d55b384000000000000000000000000000000000d00010048656c6c6f20776f726c64210500000000000000e803000000000000',
    'extras': {
        'gen_hash': '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF',
        'fee_strategy': util.FeeCalculationStrategy.ZERO,
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
        'signed': {
            'payload': 'b30000003666a4d2f839d493b45efe2f47c44d2992339ec9a34a256835faeeb2d77f8614d7f861422af7f24965560bcab9d2906151ae8b05d13403108af5c73580be02051b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd589550300009054410000000000000000683d8c8b15000000914bfa5f372d55b384000000000000000000000000000000000d00010048656c6c6f20776f726c64210500000000000000e803000000000000',
            'hash': 'd77b52e9123dad70e9b239ae8b5c3445d1c42363dfca5a336461f9510ff5c7ca',
        },
        'embedded': '630000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955030000905441914bfa5f372d55b384000000000000000000000000000000000d00010048656c6c6f20776f726c64210500000000000000e803000000000000',
    },
})
class TestTransferTransactionWithNamespace(harness.TestCase):

    def test_is_unannounced(self):
        self.assertTrue(self.model.is_unannounced())
