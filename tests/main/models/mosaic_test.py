from nem2 import models
from tests import harness


class TestMosaic(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.mosaic_id = models.MosaicId(5)
        self.mosaic = models.Mosaic(self.mosaic_id, 1000)
        self.dto = {'amount': [1000, 0], 'id': [5, 0]}
        self.catbuffer = b"\x05\x00\x00\x00\x00\x00\x00\x00\xe8\x03\x00\x00\x00\x00\x00\x00"

    def test_init(self):
        self.assertEqual(self.mosaic.id, self.mosaic_id)
        self.assertEqual(self.mosaic.amount, 1000)

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.mosaic.__dict__

    def test_properties(self):
        self.assertEqual(self.mosaic.id, models.MosaicId(5))
        self.assertEqual(self.mosaic.amount, 1000)

        with self.assertRaises(AttributeError):
            self.mosaic.id = models.MosaicId(10)
        with self.assertRaises(AttributeError):
            self.mosaic.id.id = 10
        with self.assertRaises(AttributeError):
            self.mosaic.amount = 10

    def test_repr(self):
        self.assertEqual(repr(self.mosaic), "Mosaic(id=MosaicId(id=5), amount=1000)")

    def test_str(self):
        self.assertEqual(str(self.mosaic), "Mosaic(id=MosaicId(id=5), amount=1000)")

    def test_eq(self):
        m1 = models.Mosaic(models.MosaicId(5), 1000)
        m2 = models.Mosaic(models.MosaicId(5), 1000)
        m3 = models.Mosaic(models.MosaicId(5), 500)
        m4 = models.Mosaic(models.MosaicId(10), 1000)

        self.assertTrue(m1 == m1)
        self.assertTrue(m1 == m2)
        self.assertFalse(m1 == m3)
        self.assertFalse(m1 == m4)
        self.assertTrue(m2 == m2)
        self.assertFalse(m2 == m3)
        self.assertFalse(m2 == m4)
        self.assertTrue(m3 == m3)
        self.assertFalse(m3 == m4)
        self.assertTrue(m4 == m4)

    def test_to_dto(self):
        self.assertEqual(self.mosaic.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.mosaic, models.Mosaic.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.mosaic.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.mosaic, models.Mosaic.from_catbuffer(self.catbuffer, self.network_type))


class TestMosaicId(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.mosaic_id = models.MosaicId(5)
        self.dto = [5, 0]
        self.catbuffer = b"\x05\x00\x00\x00\x00\x00\x00\x00"

    def test_init(self):
        self.assertEqual(self.mosaic_id.id, 5)

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.mosaic_id.__dict__

    def test_properties(self):
        self.assertEqual(self.mosaic_id.id, 5)

        with self.assertRaises(AttributeError):
            self.mosaic_id.id = 10

    def test_int(self):
        self.assertEqual(int(self.mosaic_id), 5)

    def test_index(self):
        self.assertEqual(hex(self.mosaic_id), "0x5")

    def test_format(self):
        value = models.MosaicId(13)
        self.assertEqual(f'{value:x}', 'd')
        self.assertEqual(f'{value:X}', 'D')

    def test_create_from_nonce(self):
        nonce = models.MosaicNonce(b'\x00\x00\x00\x00')
        public_key = '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246'
        owner = models.PublicAccount.create_from_public_key(public_key, self.network_type)
        value = models.MosaicId.create_from_nonce(nonce, owner)
        self.assertEqual(value.id, 0x2FF7D64F483BC0A6)

    def test_repr(self):
        self.assertEqual(repr(self.mosaic_id), "MosaicId(id=5)")

    def test_str(self):
        self.assertEqual(str(self.mosaic_id), repr(self.mosaic_id))

    def test_eq(self):
        id1 = models.MosaicId(5)
        id2 = models.MosaicId(5)
        id3 = models.MosaicId(8)

        self.assertTrue(id1 == id1)
        self.assertTrue(id1 == id2)
        self.assertFalse(id1 == id3)
        self.assertTrue(id2 == id2)
        self.assertFalse(id2 == id3)
        self.assertTrue(id3 == id3)

    def test_to_dto(self):
        self.assertEqual(self.mosaic_id.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.mosaic_id, models.MosaicId.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.mosaic_id.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.mosaic_id, models.MosaicId.from_catbuffer(self.catbuffer, self.network_type))


class TestMosaicInfo(harness.TestCase):
    pass


class TestMosaicLevy(harness.TestCase):
    pass


class TestMosaicLevyType(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.absolute = models.MosaicLevyType.ABSOLUTE
        self.calculated = models.MosaicLevyType.CALCULATED
        self.dto = 1
        self.catbuffer = b'\x01'

    def test_values(self):
        self.assertEqual(self.absolute, 1)
        self.assertEqual(self.calculated, 2)

    def test_description(self):
        self.assertTrue(self.absolute.description().startswith("The levy is an absolute fee."))
        self.assertTrue(self.calculated.description().startswith("The levy is calculated"))

    def test_to_dto(self):
        self.assertEqual(self.absolute.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.absolute, models.MosaicLevyType.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.absolute.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.absolute, models.MosaicLevyType.from_catbuffer(self.catbuffer, self.network_type))


class TestMosaicNonce(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.catbuffer = b'\x00\x00\x00\x00'
        self.nonce = models.MosaicNonce(self.catbuffer)
        self.dto = [0, 0, 0, 0]

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.nonce.__dict__

    def test_properties(self):
        self.assertEqual(self.nonce.nonce, self.catbuffer)
        with self.assertRaises(AttributeError):
            self.nonce.nonce = self.catbuffer

    def test_int(self):
        self.assertEqual(int(self.nonce), 0)

    def test_index(self):
        self.assertEqual(hex(self.nonce), "0x0")

    def test_format(self):
        value = models.MosaicNonce.create_from_int(5)
        self.assertEqual(f'{value:x}', '5')
        self.assertEqual(f'{value:X}', '5')

        value = models.MosaicNonce.create_from_int(13)
        self.assertEqual(f'{value:x}', 'd')
        self.assertEqual(f'{value:X}', 'D')

    def test_create_random(self):
        def fake_entropy(size: int):
            return b'4' * size

        self.assertEqual(models.MosaicNonce.create_random(fake_entropy).nonce, b'4444')
        models.MosaicNonce.create_random()

    def test_create_from_hex(self):
        data = '00000000'
        self.assertEqual(self.nonce, models.MosaicNonce.create_from_hex(data))

    def test_create_from_int(self):
        self.assertEqual(models.MosaicNonce.create_from_int(5).nonce, b'\x05\x00\x00\x00')
        self.assertEqual(models.MosaicNonce.create_from_int(325).nonce, b'E\x01\x00\x00')

    def test_repr(self):
        self.assertEqual(repr(self.nonce), "MosaicNonce(nonce=b'\\x00\\x00\\x00\\x00')")

    def test_str(self):
        self.assertEqual(str(self.nonce), repr(self.nonce))

    def test_eq(self):
        n1 = models.MosaicNonce.create_from_hex('01234567')
        n2 = models.MosaicNonce.create_from_hex('01234567')
        n3 = models.MosaicNonce.create_from_hex('01234568')

        self.assertTrue(n1 == n1)
        self.assertTrue(n1 == n2)
        self.assertFalse(n1 == n3)
        self.assertTrue(n2 == n2)
        self.assertFalse(n2 == n3)
        self.assertTrue(n3 == n3)

    def test_to_dto(self):
        self.assertEqual(self.nonce.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.nonce, models.MosaicNonce.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.nonce.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.nonce, models.MosaicNonce.from_catbuffer(self.catbuffer, self.network_type))


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
