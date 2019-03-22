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
        #nonce = models.MosaicNonce(b'\x00\x00\x00\x00')
        #public_key = '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246'
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
        "The levy is an absolute fee",
        "The levy is calculated from",
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


class TestMosaicProperties(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.properties = models.MosaicProperties.create(
            supply_mutable=True,
            transferable=True,
            levy_mutable=False,
            divisibility=1,
            duration=100,
        )
        self.dto = [[3, 0], [1, 0], [100, 0]]
        self.catbuffer = b'\x01\x03\x01\x02d\x00\x00\x00\x00\x00\x00\x00'

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.properties.__dict__

    def test_properties(self):
        self.assertEqual(self.properties.flags, 3)
        self.assertEqual(self.properties.supply_mutable, True)
        self.assertEqual(self.properties.transferable, True)
        self.assertEqual(self.properties.levy_mutable, False)
        self.assertEqual(self.properties.divisibility, 1)
        self.assertEqual(self.properties.duration, 100)

    def test_create(self):
        properties = models.MosaicProperties.create()
        self.assertEqual(properties.flags, 2)
        self.assertEqual(properties.divisibility, 0)
        self.assertEqual(properties.duration, 0)

    def test_repr(self):
        self.assertEqual(repr(self.properties), "MosaicProperties(flags=3, divisibility=1, duration=100)")

    def test_str(self):
        self.assertEqual(str(self.properties), repr(self.properties))

    def test_eq(self):
        p1 = models.MosaicProperties.create(divisibility=2)
        p2 = models.MosaicProperties.create(divisibility=2)
        p3 = models.MosaicProperties.create()

        self.assertTrue(p1 == p1)
        self.assertTrue(p1 == p2)
        self.assertFalse(p1 == p3)
        self.assertTrue(p2 == p2)
        self.assertFalse(p2 == p3)
        self.assertTrue(p3 == p3)

    def test_to_dto(self):
        self.assertEqual(self.properties.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.properties, models.MosaicProperties.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.properties.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.properties, models.MosaicProperties.from_catbuffer(self.catbuffer, self.network_type))

    def test_dataclasses(self):
        self.assertEqual(self.properties, self.properties.replace())
        self.assertIsInstance(self.properties.asdict(), dict)
        self.assertIsInstance(self.properties.astuple(), tuple)
        self.assertIsInstance(self.properties.fields(), tuple)


class TestMosaicSupplyType(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.decrease = models.MosaicSupplyType.DECREASE
        self.increase = models.MosaicSupplyType.INCREASE
        self.dto = 0
        self.catbuffer = b'\x00'

    def test_values(self):
        self.assertEqual(self.decrease, 0)
        self.assertEqual(self.increase, 1)

    def test_description(self):
        self.assertEqual(self.decrease.description(), "Decrease mosaic supply.")
        self.assertEqual(self.increase.description(), "Increase mosaic supply.")

    def test_to_dto(self):
        self.assertEqual(self.decrease.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.decrease, models.MosaicSupplyType.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.decrease.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.decrease, models.MosaicSupplyType.from_catbuffer(self.catbuffer, self.network_type))


class TestNetworkCurrencyMosaic(harness.TestCase):

    def setUp(self):
        self.mosaic = models.NetworkCurrencyMosaic(1)

    def test_init(self):
        self.assertEqual(self.mosaic.id.id, 0x85BBEA6CC462B244)
        self.assertEqual(self.mosaic.amount, 1)

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.mosaic.__dict__

    def test_class_variables(self):
        cls = models.NetworkCurrencyMosaic
        self.assertEqual(cls.NAMESPACE_ID, models.NamespaceId(0x85BBEA6CC462B244))
        self.assertEqual(cls.DIVISIBILITY, 6)
        self.assertEqual(cls.INITIAL_SUPPLY, 8999999998)
        self.assertEqual(cls.TRANSFERABLE, True)
        self.assertEqual(cls.SUPPLY_MUTABLE, False)
        self.assertEqual(cls.LEVY_MUTABLE, False)

    def test_create_relative(self):
        value = models.NetworkCurrencyMosaic.create_relative(1)
        self.assertEqual(value.amount, 1000000)

    def test_create_absolute(self):
        value = models.NetworkCurrencyMosaic.create_absolute(1)
        self.assertEqual(value.amount, 1)

    def test_dataclasses(self):
        self.assertEqual(self.mosaic, self.mosaic.replace())
        self.assertIsInstance(self.mosaic.asdict(), dict)
        self.assertIsInstance(self.mosaic.astuple(), tuple)
        self.assertIsInstance(self.mosaic.fields(), tuple)


class TestNetworkHarvestMosaic(harness.TestCase):

    def setUp(self):
        self.mosaic = models.NetworkHarvestMosaic(1)

    def test_init(self):
        self.assertEqual(self.mosaic.id.id, 0x941299B2B7E1291C)
        self.assertEqual(self.mosaic.amount, 1)

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.mosaic.__dict__

    def test_class_variables(self):
        cls = models.NetworkHarvestMosaic
        self.assertEqual(cls.NAMESPACE_ID, models.NamespaceId(0x941299B2B7E1291C))
        self.assertEqual(cls.DIVISIBILITY, 3)
        self.assertEqual(cls.INITIAL_SUPPLY, 15000000)
        self.assertEqual(cls.TRANSFERABLE, True)
        self.assertEqual(cls.SUPPLY_MUTABLE, True)
        self.assertEqual(cls.LEVY_MUTABLE, False)

    def test_create_relative(self):
        value = models.NetworkHarvestMosaic.create_relative(1)
        self.assertEqual(value.amount, 1000)

    def test_create_absolute(self):
        value = models.NetworkHarvestMosaic.create_absolute(1)
        self.assertEqual(value.amount, 1)

    def test_dataclasses(self):
        self.assertEqual(self.mosaic, self.mosaic.replace())
        self.assertIsInstance(self.mosaic.asdict(), dict)
        self.assertIsInstance(self.mosaic.astuple(), tuple)
        self.assertIsInstance(self.mosaic.fields(), tuple)
