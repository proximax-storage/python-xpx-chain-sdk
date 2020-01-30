from xpxchain import models
from tests import harness


@harness.model_test_case({
    'type': models.Mosaic,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'id': models.MosaicId(5),
        'amount': 1000,
    },
    'dto': {
        'id': [5, 0],
        'amount': [1000, 0],
    },
    'catbuffer': b'\x05\x00\x00\x00\x00\x00\x00\x00\xe8\x03\x00\x00\x00\x00\x00\x00',
})
class TestMosaic(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.MosaicId,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'id': 5,
    },
    'extras': {
        'nonce': models.MosaicNonce(b'\x00\x00\x00\x00'),
        'public_key': '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246',
    },
})
class TestMosaicId(harness.TestCase):

    def test_int(self):
        self.assertEqual(int(self.model), 5)

    def test_index(self):
        self.assertEqual(hex(self.model), "0x5")

    def test_format(self):
        value = self.type(13)
        self.assertEqual(f'{value:x}', 'd')
        self.assertEqual(f'{value:X}', 'D')

    def test_create_from_nonce(self):
        owner = models.PublicAccount.create_from_public_key(self.extras['public_key'], self.network_type)
        value = self.type.create_from_nonce(self.extras['nonce'], owner)
        self.assertEqual(value.id, 0x2FF7D64F483BC0A6)


@harness.model_test_case({
    'type': models.MosaicInfo,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'meta_id': '5cc07cbc3a48065f47d6df80',
        'mosaic_id': models.MosaicId.create_from_hex('6c699a1517bea955'),
        'supply': 8999999998000000,
        'height': 1,
        'owner': models.PublicAccount.create_from_public_key('a04335f99d9ee3787528a16c7a302f80d511e9cf71d97d95c2182e0ea75a1ef9', models.NetworkType.MIJIN_TEST),
        'revision': 1,
        'properties': models.MosaicProperties(0x2, 6, 0),
    },
    'dto': {
        'meta': {
            'id': '5cc07cbc3a48065f47d6df80',
        },
        'mosaic': {
            'mosaicId': [398371157, 1818860053],
            'supply': [3403414400, 2095475],
            'height': [1, 0],
            'owner': 'a04335f99d9ee3787528a16c7a302f80d511e9cf71d97d95c2182e0ea75a1ef9',
            'revision': 1,
            'properties': [{'id': 0, 'value': [2, 0]}, {'id': 1, 'value': [6, 0]}, {'id': 2, 'value': [0, 0]}],
        },
    },
})
class TestMosaicInfo(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.MosaicName,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'mosaic_id': models.MosaicId(0xd525ad41d95fcf29),
        'names': ['xem'],
    },
    'dto': {
        'mosaicId': [0xd95fcf29, 0xd525ad41],
        'names': ['xem'],
    },
})
class TestMosaicName(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.MosaicNonce,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'nonce': b'\x12\x34\x56\x78',
    },
    'dto': 0x78563412,
    'catbuffer': b'\x12\x34\x56\x78',
    'extras': {
        'nonce': models.MosaicNonce(b'\x12\x34\x56\x78'),
        'public_key': '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246',
    },
})
class TestMosaicNonce(harness.TestCase):

    def test_rich_init(self):
        self.assertEqual(self.model, self.type('12345678'))
        with self.assertRaises(ValueError):
            self.type('12')
        with self.assertRaises(ValueError):
            self.type(b'\x12')
        with self.assertRaises(TypeError):
            self.type(None)

    def test_int(self):
        self.assertEqual(int(self.model), 0x78563412)

    def test_create_random(self):
        def fake_entropy(size: int):
            return b'4' * size

        self.assertEqual(self.type.create_random(fake_entropy).nonce, b'4444')
        self.type.create_random()

    def test_create_from_hex(self):
        self.assertEqual(self.model, self.type.create_from_hex('12345678'))

    def test_create_from_int(self):
        self.assertEqual(self.type.create_from_int(5).nonce, b'\x05\x00\x00\x00')
        self.assertEqual(self.type.create_from_int(325).nonce, b'E\x01\x00\x00')


@harness.model_test_case({
    'type': models.MosaicProperties,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'flags': 0x3,
        'divisibility': 1,
        'duration': 100,
    },
    'dto': [{'id': 0, 'value': [3, 0]}, {'id': 1, 'value': [1, 0]}, {'id': 2, 'value': [100, 0]}],
})
class TestMosaicProperties(harness.TestCase):

    def test_properties(self):
        self.assertEqual(self.model.supply_mutable, True)
        self.assertEqual(self.model.transferable, True)

    def test_create(self):
        self.assertEqual(self.type.create().flags, 0x2)
        self.assertEqual(self.type.create(supply_mutable=True).flags, 0x3)
        self.assertEqual(self.type.create(transferable=True).flags, 0x2)
        self.assertEqual(self.type.create(transferable=False).flags, 0x0)


@harness.enum_test_case({
    'type': models.MosaicSupplyType,
    'enums': [
        models.MosaicSupplyType.DECREASE,
        models.MosaicSupplyType.INCREASE,
    ],
    'values': [
        0,
        1,
    ],
    'descriptions': [
        'Decrease mosaic supply.',
        'Increase mosaic supply.',
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
class TestMosaicSupplyType(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.NetworkCurrencyMosaic,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'amount': 1,
    },
    'dto': {
        'amount': [1, 0],
        'id': [3294802500, 2243684972],
    },
    'catbuffer': b'D\xb2b\xc4l\xea\xbb\x85\x01\x00\x00\x00\x00\x00\x00\x00',
})
class TestNetworkCurrencyMosaic(harness.TestCase):

    def test_class_variables(self):
        self.assertEqual(self.type.NAMESPACE_ID, models.NamespaceId(0x85BBEA6CC462B244))
        self.assertEqual(self.type.DIVISIBILITY, 6)
        self.assertEqual(self.type.INITIAL_SUPPLY, 8999999998)
        self.assertEqual(self.type.TRANSFERABLE, True)
        self.assertEqual(self.type.SUPPLY_MUTABLE, False)
        self.assertEqual(self.type.LEVY_MUTABLE, False)

    def test_create_relative(self):
        self.assertEqual(self.type.create_relative(1).amount, 1000000)

    def test_create_absolute(self):
        self.assertEqual(self.type.create_absolute(1).amount, 1)

    def test_from_invalid_dto(self):
        with self.assertRaises(ValueError):
            self.type.create_from_dto({'amount': [1, 0], 'id': [0, 0]})

    def test_from_invalid_catbuffer(self):
        with self.assertRaises(ValueError):
            catbuffer = bytes(8) + self.catbuffer[8:]
            self.type.create_from_catbuffer(catbuffer)


@harness.model_test_case({
    'type': models.NetworkHarvestMosaic,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'amount': 1,
    },
    'dto': {
        'amount': [1, 0],
        'id': [3084986652, 2484246962],
    },
    'catbuffer': b'\x1c)\xe1\xb7\xb2\x99\x12\x94\x01\x00\x00\x00\x00\x00\x00\x00',
})
class TestNetworkHarvestMosaic(harness.TestCase):

    def test_class_variables(self):
        self.assertEqual(self.type.NAMESPACE_ID, models.NamespaceId(0x941299B2B7E1291C))
        self.assertEqual(self.type.DIVISIBILITY, 3)
        self.assertEqual(self.type.INITIAL_SUPPLY, 15000000)
        self.assertEqual(self.type.TRANSFERABLE, True)
        self.assertEqual(self.type.SUPPLY_MUTABLE, True)
        self.assertEqual(self.type.LEVY_MUTABLE, False)

    def test_create_relative(self):
        self.assertEqual(self.type.create_relative(1).amount, 1000)

    def test_create_absolute(self):
        self.assertEqual(self.type.create_absolute(1).amount, 1)

    def test_from_invalid_dto(self):
        with self.assertRaises(ValueError):
            self.type.create_from_dto({'amount': [1, 0], 'id': [0, 0]})

    def test_from_invalid_catbuffer(self):
        with self.assertRaises(ValueError):
            catbuffer = bytes(8) + self.catbuffer[8:]
            self.type.create_from_catbuffer(catbuffer)
