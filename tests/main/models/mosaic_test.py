from nem2 import models
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
    'dto': [5, 0],
    'catbuffer': b'\x05\x00\x00\x00\x00\x00\x00\x00',
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


class TestMosaicInfo(harness.TestCase):
    pass


class TestMosaicLevy(harness.TestCase):
    pass


@harness.enum_test_case({
    'type': models.MosaicLevyType,
    'enums': [
        models.MosaicLevyType.ABSOLUTE,
        models.MosaicLevyType.CALCULATED,
    ],
    'values': [
        1,
        2,
    ],
    'descriptions': [
        'The levy is an absolute fee',
        'The levy is calculated from',
    ],
    'dto': [
        1,
        2,
    ],
    'catbuffer': [
        b'\x01',
        b'\x02',
    ],
})
class TestMosaicLevyType(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.MosaicNonce,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'nonce': b'\x12\x34\x56\x78',
    },
    'dto': [0x12, 0x34, 0x56, 0x78],
    'catbuffer': b'\x12\x34\x56\x78',
    'extras': {
        'nonce': models.MosaicNonce(b'\x12\x34\x56\x78'),
        'public_key': '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246',
    },
})
class TestMosaicNonce(harness.TestCase):

    def test_int(self):
        self.assertEqual(int(self.model), 0x78563412)

    def test_index(self):
        self.assertEqual(hex(self.model), "0x78563412")

    def test_format(self):
        value = self.type(5)
        self.assertEqual(f'{value:x}', '5')
        self.assertEqual(f'{value:X}', '5')

        value = self.type(13)
        self.assertEqual(f'{value:x}', 'd')
        self.assertEqual(f'{value:X}', 'D')

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
    'dto': [[3, 0], [1, 0], [100, 0]],
    'catbuffer': b'\x01\x03\x01\x02d\x00\x00\x00\x00\x00\x00\x00',
})
class TestMosaicProperties(harness.TestCase):

    def test_properties(self):
        self.assertEqual(self.model.supply_mutable, True)
        self.assertEqual(self.model.transferable, True)
        self.assertEqual(self.model.levy_mutable, False)


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
