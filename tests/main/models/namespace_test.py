from nem2 import models
from tests import harness


class TestAddressAlias(harness.TestCase):

    def setUp(self):
        self.mosaic_id = models.MosaicId(5)
        public_key = '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246'
        self.address = models.Address.create_from_public_key(public_key, models.NetworkType.MIJIN_TEST)

    def test_init(self):
        value = models.AddressAlias(self.address)
        self.assertEqual(value.type, models.AliasType.ADDRESS)
        self.assertEqual(value.value, self.address)
        self.assertEqual(value.address, self.address)

        self.assertEqual(repr(value), "AddressAlias(type=<AliasType.ADDRESS: 2>, value=Address(address='SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54', network_type=<NetworkType.MIJIN_TEST: 144>))")
        self.assertEqual(str(value), repr(value))
        self.assertNotEqual(value, models.Alias())
        self.assertEqual(value, models.Alias(self.address))
        self.assertNotEqual(value, models.Alias(self.mosaic_id))

        with self.assertRaises(ValueError):
            value.mosaic_id

        dto = {'type': 2, 'address': {'address': 'SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54', 'networkType': 144}}
        self.assertEqual(value.to_dto(), dto)
        self.assertEqual(models.Alias.from_dto(dto), value)

    def test_slots(self):
        value = models.AddressAlias(self.address)
        with self.assertRaises(TypeError):
            value.__dict__


class TestAlias(harness.TestCase):

    def setUp(self):
        self.mosaic_id = models.MosaicId(5)
        public_key = '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246'
        self.address = models.Address.create_from_public_key(public_key, models.NetworkType.MIJIN_TEST)

    def test_none(self):
        value = models.Alias()
        self.assertEqual(value.type, models.AliasType.NONE)
        self.assertEqual(value.value, None)

        self.assertEqual(repr(value), 'Alias(type=<AliasType.NONE: 0>, value=None)')
        self.assertEqual(str(value), repr(value))
        self.assertEqual(value, models.Alias())
        self.assertNotEqual(value, models.Alias(self.address))
        self.assertNotEqual(value, models.Alias(self.mosaic_id))

        with self.assertRaises(ValueError):
            value.address
        with self.assertRaises(ValueError):
            value.mosaic_id
        with self.assertRaises(TypeError):
            value.__dict__

        self.assertEqual(value.to_dto(), None)
        self.assertEqual(models.Alias.from_dto(None), value)

    def test_address(self):
        value = models.Alias(self.address)
        self.assertEqual(value.type, models.AliasType.ADDRESS)
        self.assertEqual(value.value, self.address)
        self.assertEqual(value.address, self.address)

        self.assertEqual(repr(value), "Alias(type=<AliasType.ADDRESS: 2>, value=Address(address='SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54', network_type=<NetworkType.MIJIN_TEST: 144>))")
        self.assertEqual(str(value), repr(value))
        self.assertNotEqual(value, models.Alias())
        self.assertEqual(value, models.Alias(self.address))
        self.assertNotEqual(value, models.Alias(self.mosaic_id))

        with self.assertRaises(ValueError):
            value.mosaic_id
        with self.assertRaises(TypeError):
            value.__dict__

        dto = {'type': 2, 'address': {'address': 'SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54', 'networkType': 144}}
        self.assertEqual(value.to_dto(), dto)
        self.assertEqual(models.Alias.from_dto(dto), value)

    def test_mosaic_id(self):
        value = models.Alias(self.mosaic_id)
        self.assertEqual(value.type, models.AliasType.MOSAIC_ID)
        self.assertEqual(value.value, self.mosaic_id)
        self.assertEqual(value.mosaic_id, self.mosaic_id)
        self.assertEqual(value.mosaicId, self.mosaic_id)

        self.assertEqual(repr(value), "Alias(type=<AliasType.MOSAIC_ID: 1>, value=MosaicId(id=5))")
        self.assertEqual(str(value), repr(value))
        self.assertNotEqual(value, models.Alias())
        self.assertNotEqual(value, models.Alias(self.address))
        self.assertEqual(value, models.Alias(self.mosaic_id))

        with self.assertRaises(ValueError):
            value.address
        with self.assertRaises(TypeError):
            value.__dict__

        dto = {'type': 1, 'mosaicId': [5, 0]}
        self.assertEqual(value.to_dto(), dto)
        self.assertEqual(models.Alias.from_dto(dto), value)


class TestAliasActionType(harness.TestCase):

    def setUp(self):
        self.link = models.AliasActionType.LINK
        self.unlink = models.AliasActionType.UNLINK

    def test_values(self):
        self.assertEqual(self.link, 0)
        self.assertEqual(self.unlink, 1)

    def test_description(self):
        self.assertEqual(self.link.description(), "Link an alias.")
        self.assertEqual(self.unlink.description(), "Unlink an alias.")


class TestAliasType(harness.TestCase):

    def setUp(self):
        self.none = models.AliasType.NONE
        self.mosaic_id = models.AliasType.MOSAIC_ID
        self.address = models.AliasType.ADDRESS

    def test_values(self):
        self.assertEqual(self.none, 0)
        self.assertEqual(self.mosaic_id, 1)
        self.assertEqual(self.address, 2)

    def test_description(self):
        self.assertEqual(self.none.description(), "No alias.")
        self.assertEqual(self.mosaic_id.description(), "Mosaic ID alias.")
        self.assertEqual(self.address.description(), "Address alias.")

    def test_to_dto(self):
        self.assertEqual(self.none.to_dto(), 0)
        self.assertEqual(self.mosaic_id.to_dto(), 1)
        self.assertEqual(self.address.to_dto(), 2)
        self.assertEqual(self.none.toDto(), 0)

    def test_from_dto(self):
        self.assertEqual(self.none, models.AliasType.from_dto(0))
        self.assertEqual(self.mosaic_id, models.AliasType.fromDto(1))
        self.assertEqual(self.address, models.AliasType.from_dto(2))


class TestEmptyAlias(harness.TestCase):

    def setUp(self):
        self.mosaic_id = models.MosaicId(5)
        public_key = '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246'
        self.address = models.Address.create_from_public_key(public_key, models.NetworkType.MIJIN_TEST)

    def test_slots(self):
        value = models.EmptyAlias()
        with self.assertRaises(TypeError):
            value.__dict__

    def test_init(self):
        value = models.EmptyAlias()
        self.assertEqual(value.type, models.AliasType.NONE)
        self.assertEqual(value.value, None)

        self.assertEqual(repr(value), 'EmptyAlias(type=<AliasType.NONE: 0>, value=None)')
        self.assertEqual(str(value), repr(value))
        self.assertEqual(value, models.Alias())
        self.assertNotEqual(value, models.Alias(self.address))
        self.assertNotEqual(value, models.Alias(self.mosaic_id))

        with self.assertRaises(ValueError):
            value.address
        with self.assertRaises(ValueError):
            value.mosaic_id

        self.assertEqual(value.to_dto(), None)
        self.assertEqual(models.Alias.from_dto(None), value)


class TestMosaicAlias(harness.TestCase):

    def setUp(self):
        self.mosaic_id = models.MosaicId(5)
        public_key = '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246'
        self.address = models.Address.create_from_public_key(public_key, models.NetworkType.MIJIN_TEST)

    def test_slots(self):
        value = models.MosaicAlias(self.mosaic_id)
        with self.assertRaises(TypeError):
            value.__dict__

    def test_init(self):
        value = models.MosaicAlias(self.mosaic_id)
        self.assertEqual(value.type, models.AliasType.MOSAIC_ID)
        self.assertEqual(value.value, self.mosaic_id)
        self.assertEqual(value.mosaic_id, self.mosaic_id)
        self.assertEqual(value.mosaicId, self.mosaic_id)

        self.assertEqual(repr(value), "MosaicAlias(type=<AliasType.MOSAIC_ID: 1>, value=MosaicId(id=5))")
        self.assertEqual(str(value), repr(value))
        self.assertNotEqual(value, models.Alias())
        self.assertNotEqual(value, models.Alias(self.address))
        self.assertEqual(value, models.Alias(self.mosaic_id))

        with self.assertRaises(ValueError):
            value.address

        dto = {'type': 1, 'mosaicId': [5, 0]}
        self.assertEqual(value.to_dto(), dto)
        self.assertEqual(models.Alias.from_dto(dto), value)


class TestNamespaceId(harness.TestCase):

    def test_init(self):
        value = models.NamespaceId(5)
        self.assertEqual(value.id, 5)

        value = models.NamespaceId("")
        self.assertEqual(value.id, 0)

        value = models.NamespaceId("sample")
        self.assertEqual(value.id, 0x88B64C3BE2F47144)

        value = models.NamespaceId("sample.sub")
        self.assertEqual(value.id, 0xFA9429715A71ACC9)

        value = models.NamespaceId("sample.sub.full")
        self.assertEqual(value.id, 0x8BC7011B0B344C54)

    def test_slots(self):
        value = models.NamespaceId(5)
        with self.assertRaises(TypeError):
            value.__dict__

    def test_int(self):
        value = models.NamespaceId(5)
        self.assertEqual(int(value), 5)

    def test_index(self):
        value = models.NamespaceId(5)
        self.assertEqual(hex(value), "0x5")

    def test_format(self):
        value = models.NamespaceId(5)
        self.assertEqual(f'{value:x}', '5')
        self.assertEqual(f'{value:X}', '5')

        value = models.NamespaceId(13)
        self.assertEqual(f'{value:x}', 'd')
        self.assertEqual(f'{value:X}', 'D')

    def test_repr(self):
        value = models.NamespaceId(5)
        self.assertEqual(repr(value), "NamespaceId(id=5)")

    def test_str(self):
        value = models.NamespaceId(5)
        self.assertEqual(str(value), "NamespaceId(id=5)")

    def test_eq(self):
        id1 = models.NamespaceId(5)
        id2 = models.NamespaceId(5)
        id3 = models.NamespaceId(8)

        self.assertTrue(id1 == id1)
        self.assertTrue(id1 == id2)
        self.assertFalse(id1 == id3)
        self.assertTrue(id2 == id2)
        self.assertFalse(id2 == id3)
        self.assertTrue(id3 == id3)

    def test_to_dto(self):
        value = models.NamespaceId(5)
        dto = value.to_dto()
        self.assertEqual(dto, [5, 0])

        self.assertEqual(value.toDto(), dto)

    def test_from_dto(self):
        value = models.NamespaceId(5)
        dto = value.to_dto()
        self.assertEqual(value, models.NamespaceId.from_dto(dto))
        self.assertEqual(value, models.NamespaceId.fromDto(dto))


class TestNamespaceInfo(harness.TestCase):
    # TODO(ahuszagh) Implement...
    pass


class TestNamespaceName(harness.TestCase):

    def test_init(self):
        namespace_id = models.NamespaceId(0x88B64C3BE2F47144)
        value = models.NamespaceName(namespace_id, "sample")
        self.assertEqual(value.namespace_id, namespace_id)
        self.assertEqual(value.name, "sample")
        self.assertEqual(value.namespaceId, value.namespace_id)

    def test_slots(self):
        value = models.NamespaceName.create_from_name("sample")
        with self.assertRaises(TypeError):
            value.__dict__

    def test_create_from_name(self):
        value = models.NamespaceName.create_from_name("sample")
        self.assertEqual(value.namespace_id.id, 0x88B64C3BE2F47144)
        self.assertEqual(value.name, "sample")

    def test_repr(self):
        value = models.NamespaceName.create_from_name("sample")
        self.assertEqual(repr(value), "NamespaceName(namespace_id=NamespaceId(id=9851145055013990724), name='sample')")

    def test_str(self):
        value = models.NamespaceName.create_from_name("sample")
        self.assertEqual(str(value), repr(value))

    def test_eq(self):
        n1 = models.NamespaceName.create_from_name("sample")
        n2 = models.NamespaceName.create_from_name("sample")
        n3 = models.NamespaceName.create_from_name("sample3")

        self.assertTrue(n1 == n1)
        self.assertTrue(n1 == n2)
        self.assertFalse(n1 == n3)
        self.assertTrue(n2 == n2)
        self.assertFalse(n2 == n3)
        self.assertTrue(n3 == n3)

    def test_to_dto(self):
        value = models.NamespaceName.create_from_name("sample")
        dto = value.to_dto()
        self.assertEqual(dto['namespaceId'], [3807670596, 2293648443])
        self.assertEqual(dto['name'], 'sample')

        self.assertEqual(value.toDto(), dto)

    def test_from_dto(self):
        value = models.NamespaceName.create_from_name("sample")
        dto = value.to_dto()
        self.assertEqual(value, models.NamespaceName.from_dto(dto))
        self.assertEqual(value, models.NamespaceName.fromDto(dto))


class TestNamespaceType(harness.TestCase):

    def setUp(self):
        self.root = models.NamespaceType.ROOT_NAMESPACE
        self.sub = models.NamespaceType.SUB_NAMESPACE

    def test_values(self):
        self.assertEqual(self.root, 0)
        self.assertEqual(self.sub, 1)

    def test_description(self):
        self.assertEqual(self.root.description(), "Root namespace.")
        self.assertEqual(self.sub.description(), "Sub namespace.")

    def test_to_dto(self):
        self.assertEqual(self.root.to_dto(), 0)
        self.assertEqual(self.sub.to_dto(), 1)
        self.assertEqual(self.root.toDto(), 0)

    def test_from_dto(self):
        self.assertEqual(self.root, models.NamespaceType.from_dto(0))
        self.assertEqual(self.sub, models.NamespaceType.fromDto(1))
