from nem2 import models
from tests.harness import TestCase


class TestMosaic(TestCase):

    def test_init(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(value.id, models.MosaicId(5))
        self.assertEqual(value.amount, 1000)

    def test_properties(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(value.id, models.MosaicId(5))
        self.assertEqual(value.amount, 1000)

        with self.assertRaises(AttributeError):
            value.id = models.MosaicId(10)
        with self.assertRaises(AttributeError):
            value.id.id = 10
        with self.assertRaises(AttributeError):
            value.amount = 10

    def test_repr(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(repr(value), "Mosaic(id=MosaicId(id=5), amount=1000)")

    def test_str(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(str(value), "Mosaic(id=MosaicId(id=5), amount=1000)")

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
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(value.to_dto(), {'amount': [1000, 0], 'id': [5, 0]})

    def test_from_dto(self):
        value = models.Mosaic.from_dto({'amount': [1000, 0], 'id': [5, 0]})
        self.assertEqual(value.id, models.MosaicId(5))
        self.assertEqual(value.amount, 1000)

    def test_to_catbuffer(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(value.to_catbuffer(), b"\x05\x00\x00\x00\x00\x00\x00\x00\xe8\x03\x00\x00\x00\x00\x00\x00")

    def test_from_catbuffer(self):
        value, rem = models.Mosaic.from_catbuffer(b"\x05\x00\x00\x00\x00\x00\x00\x00\xe8\x03\x00\x00\x00\x00\x00\x00")
        self.assertEqual(value.id, models.MosaicId(5))
        self.assertEqual(value.amount, 1000)
        self.assertEqual(rem, b'')

    def test_serialize(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(value.serialize(models.InterchangeFormat.DTO), value.to_dto())
        self.assertEqual(value.serialize(models.InterchangeFormat.CATBUFFER), value.to_catbuffer())

    def test_deserialize(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(models.Mosaic.deserialize(value.to_dto(), models.InterchangeFormat.DTO), value)
        self.assertEqual(models.Mosaic.deserialize(value.to_catbuffer(), models.InterchangeFormat.CATBUFFER), value)


class TestMosaicId(TestCase):

    def test_init(self):
        value = models.MosaicId(5)
        self.assertEqual(value.id, 5)

    def test_properties(self):
        value = models.MosaicId(5)
        self.assertEqual(value.id, 5)

        with self.assertRaises(AttributeError):
            value.id = 10

    def test_int(self):
        value = models.MosaicId(5)
        self.assertEqual(int(value), 5)

    def test_index(self):
        value = models.MosaicId(5)
        self.assertEqual(hex(value), "0x5")

    def test_create_from_nonce(self):
        nonce = models.MosaicNonce(b'\x00\x00\x00\x00')
        public_key = '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246'
        network_type = models.NetworkType.MIJIN_TEST
        owner = models.PublicAccount.create_from_public_key(public_key, network_type)
        value = models.MosaicId.create_from_nonce(nonce, owner)
        self.assertEqual(value.id, 0x2FF7D64F483BC0A6)

        self.assertEqual(value, models.MosaicId.createFromNonce(nonce, owner))

    def test_repr(self):
        value = models.MosaicId(5)
        self.assertEqual(repr(value), "MosaicId(id=5)")

    def test_str(self):
        value = models.MosaicId(5)
        self.assertEqual(str(value), "MosaicId(id=5)")

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
        value = models.MosaicId(5)
        self.assertEqual(value.to_dto(), [5, 0])

    def test_from_dto(self):
        value = models.MosaicId.from_dto([5, 0])
        self.assertEqual(value.id, 5)

    def test_to_catbuffer(self):
        value = models.MosaicId(5)
        self.assertEqual(value.to_catbuffer(), b"\x05\x00\x00\x00\x00\x00\x00\x00")

    def test_from_catbuffer(self):
        value, rem = models.MosaicId.from_catbuffer(b"\x05\x00\x00\x00\x00\x00\x00\x00")
        self.assertEqual(value.id, 5)
        self.assertEqual(rem, b'')

    def test_serialize(self):
        value = models.MosaicId(5)
        self.assertEqual(value.serialize(models.InterchangeFormat.DTO), value.to_dto())
        self.assertEqual(value.serialize(models.InterchangeFormat.CATBUFFER), value.to_catbuffer())

    def test_deserialize(self):
        value = models.MosaicId(5)
        self.assertEqual(models.MosaicId.deserialize(value.to_dto(), models.InterchangeFormat.DTO), value)
        self.assertEqual(models.MosaicId.deserialize(value.to_catbuffer(), models.InterchangeFormat.CATBUFFER), value)


class TestMosaicInfo(TestCase):
    # TODO(ahuszagh) Implement...
    pass


class TestMosaicNonce(TestCase):

    def setUp(self):
        self.data = b'\x00\x00\x00\x00'
        self.nonce = models.MosaicNonce(self.data)

    def test_properties(self):
        self.assertEqual(self.nonce.nonce, self.data)

        with self.assertRaises(AttributeError):
            self.nonce.nonce = self.data

    def test_int(self):
        self.assertEqual(int(self.nonce), 0)

    def test_index(self):
        self.assertEqual(hex(self.nonce), "0x0")

    def test_create_random(self):
        def fake_entropy(size: int):
            return b'4' * size

        self.assertEqual(models.MosaicNonce.create_random(fake_entropy).nonce, b'4444')
        models.MosaicNonce.create_random()
        models.MosaicNonce.createRandom()

    def test_create_from_hex(self):
        data = '00000000'
        self.assertEqual(models.MosaicNonce.create_from_hex(data), self.nonce)
        self.assertEqual(models.MosaicNonce.createFromHex(data), self.nonce)

    def test_repr(self):
        self.assertEqual(repr(self.nonce), "MosaicNonce(nonce=b'\\x00\\x00\\x00\\x00')")

    def test_str(self):
        self.assertEqual(str(self.nonce), "MosaicNonce(nonce=b'\\x00\\x00\\x00\\x00')")

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
        self.assertEqual(self.nonce.to_dto(), [0, 0, 0, 0])

    def test_from_dto(self):
        value = models.MosaicNonce.from_dto([0, 0, 0, 0])
        self.assertEqual(value.nonce, self.data)

    def test_to_catbuffer(self):
        self.assertEqual(self.nonce.to_catbuffer(), self.data)

    def test_from_catbuffer(self):
        value, rem = models.MosaicNonce.from_catbuffer(self.data)
        self.assertEqual(value.nonce, self.data)
        self.assertEqual(rem, b'')

    def test_serialize(self):
        self.assertEqual(self.nonce.serialize(models.InterchangeFormat.DTO), self.nonce.to_dto())
        self.assertEqual(self.nonce.serialize(models.InterchangeFormat.CATBUFFER), self.nonce.to_catbuffer())

    def test_deserialize(self):
        self.assertEqual(models.MosaicNonce.deserialize(self.nonce.to_dto(), models.InterchangeFormat.DTO), self.nonce)
        self.assertEqual(models.MosaicNonce.deserialize(self.nonce.to_catbuffer(), models.InterchangeFormat.CATBUFFER), self.nonce)


class TestMosaicProperties(TestCase):

    def setUp(self):
        self.properties = models.MosaicProperties.create(
            supply_mutable=True,
            transferable=True,
            levy_mutable=False,
            divisibility=1,
            duration=100,
        )

    def test_properties(self):
        self.assertEqual(self.properties.flags, 3)
        self.assertEqual(self.properties.supply_mutable, True)
        self.assertEqual(self.properties.transferable, True)
        self.assertEqual(self.properties.levy_mutable, False)
        self.assertEqual(self.properties.divisibility, 1)
        self.assertEqual(self.properties.duration, 100)

        self.assertEqual(self.properties.supplyMutable, True)
        self.assertEqual(self.properties.levyMutable, False)

    def test_create(self):
        properties = models.MosaicProperties.create()
        self.assertEqual(properties.flags, 2)
        self.assertEqual(properties.divisibility, 0)
        self.assertEqual(properties.duration, 0)

    def test_repr(self):
        self.assertEqual(repr(self.properties), "MosaicProperties(flags=3, divisibility=1, duration=100)")

    def test_str(self):
        self.assertEqual(str(self.properties), "MosaicProperties(flags=3, divisibility=1, duration=100)")

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
        self.assertEqual(self.properties.to_dto(), [[3, 0], [1, 0], [100, 0]])

    def test_from_dto(self):
        value = models.MosaicProperties.from_dto([[3, 0], [1, 0], [100, 0]])
        self.assertEqual(value, self.properties)

    def test_to_catbuffer(self):
        self.assertEqual(self.properties.to_catbuffer(), b'\x01\x03\x01\x02d\x00\x00\x00\x00\x00\x00\x00')

    def test_from_catbuffer(self):
        value, rem = models.MosaicProperties.from_catbuffer(b'\x01\x03\x01\x02d\x00\x00\x00\x00\x00\x00\x00')
        self.assertEqual(value, self.properties)
        self.assertEqual(rem, b'')

    def test_serialize(self):
        self.assertEqual(self.properties.serialize(models.InterchangeFormat.DTO), self.properties.to_dto())
        self.assertEqual(self.properties.serialize(models.InterchangeFormat.CATBUFFER), self.properties.to_catbuffer())

    def test_deserialize(self):
        self.assertEqual(models.MosaicProperties.deserialize(self.properties.to_dto(), models.InterchangeFormat.DTO), self.properties)
        self.assertEqual(models.MosaicProperties.deserialize(self.properties.to_catbuffer(), models.InterchangeFormat.CATBUFFER), self.properties)


class TestMosaicSupplyType(TestCase):

    def setUp(self):
        self.decrease = models.MosaicSupplyType.DECREASE
        self.increase = models.MosaicSupplyType.INCREASE

    def test_values(self):
        self.assertEqual(self.decrease, 0)
        self.assertEqual(self.increase, 1)

    def test_description(self):
        self.assertEqual(self.decrease.description(), "Decrease mosaic supply.")
        self.assertEqual(self.increase.description(), "Increase mosaic supply.")

    def test_to_catbuffer(self):
        self.assertEqual(self.decrease.to_catbuffer(), b'\x00')
        self.assertEqual(self.increase.to_catbuffer(), b'\x01')

        self.assertEqual(self.decrease.toCatbuffer(), b'\x00')
        self.assertEqual(self.increase.toCatbuffer(), b'\x01')


class TestNetworkCurrencyMosaic(TestCase):

    def test_init(self):
        value = models.NetworkCurrencyMosaic(1)
        self.assertEqual(value.id.id, 0x85BBEA6CC462B244)
        self.assertEqual(value.amount, 1)

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
        self.assertEqual(value, models.NetworkCurrencyMosaic.createRelative(1))

    def test_create_absolute(self):
        value = models.NetworkCurrencyMosaic.create_absolute(1)
        self.assertEqual(value.amount, 1)
        self.assertEqual(value, models.NetworkCurrencyMosaic.createAbsolute(1))


class TestNetworkHarvestMosaic(TestCase):

    def test_init(self):
        value = models.NetworkHarvestMosaic(1)
        self.assertEqual(value.id.id, 0x941299B2B7E1291C)
        self.assertEqual(value.amount, 1)

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
        self.assertEqual(value, models.NetworkHarvestMosaic.createRelative(1))

    def test_create_absolute(self):
        value = models.NetworkHarvestMosaic.create_absolute(1)
        self.assertEqual(value.amount, 1)
        self.assertEqual(value, models.NetworkHarvestMosaic.createAbsolute(1))
