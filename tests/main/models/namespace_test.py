from nem2 import models
from tests import harness


class TestAddressAlias(harness.TestCase):

    def setUp(self):
        public_key = '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246'
        self.network_type = models.NetworkType.MIJIN_TEST
        self.mosaic_id = models.MosaicId(5)
        self.address = models.Address.create_from_public_key(public_key, self.network_type)
        self.alias = models.AddressAlias(self.address)
        self.dto = {'type': 2, 'address': {'address': 'SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54', 'networkType': 144}}

    def test_init(self):
        self.assertEqual(self.alias.type, models.AliasType.ADDRESS)
        self.assertEqual(self.alias.value, self.address)
        self.assertEqual(self.alias.address, self.address)

        self.assertEqual(repr(self.alias), "AddressAlias(type=<AliasType.ADDRESS: 2>, value=Address(address='SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54', network_type=<NetworkType.MIJIN_TEST: 144>))")
        self.assertEqual(str(self.alias), repr(self.alias))
        self.assertNotEqual(self.alias, models.Alias())
        self.assertEqual(self.alias, models.Alias(self.address))
        self.assertNotEqual(self.alias, models.Alias(self.mosaic_id))

        with self.assertRaises(ValueError):
            self.alias.mosaic_id

        self.assertEqual(self.alias.to_dto(self.network_type), self.dto)
        self.assertEqual(self.alias, models.Alias.from_dto(self.dto, self.network_type))

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.alias.__dict__


class TestAlias(harness.TestCase):

    def setUp(self):
        public_key = '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246'
        self.network_type = models.NetworkType.MIJIN_TEST
        self.address = models.Address.create_from_public_key(public_key, models.NetworkType.MIJIN_TEST)
        self.mosaic_id = models.MosaicId(5)
        self.empty_alias = models.Alias()
        self.empty_dto = None
        self.address_alias = models.Alias(self.address)
        self.address_dto = {'type': 2, 'address': {'address': 'SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54', 'networkType': 144}}
        self.mosaic_alias = models.Alias(self.mosaic_id)
        self.mosaic_dto = {'type': 1, 'mosaicId': [5, 0]}

    def test_none(self):
        self.assertEqual(self.empty_alias.type, models.AliasType.NONE)
        self.assertEqual(self.empty_alias.value, None)

        self.assertEqual(repr(self.empty_alias), 'Alias(type=<AliasType.NONE: 0>, value=None)')
        self.assertEqual(str(self.empty_alias), repr(self.empty_alias))
        self.assertEqual(self.empty_alias, models.Alias())
        self.assertNotEqual(self.empty_alias, models.Alias(self.address))
        self.assertNotEqual(self.empty_alias, models.Alias(self.mosaic_id))

        with self.assertRaises(ValueError):
            self.empty_alias.address
        with self.assertRaises(ValueError):
            self.empty_alias.mosaic_id
        with self.assertRaises(TypeError):
            self.empty_alias.__dict__

        self.assertEqual(self.empty_alias.to_dto(self.network_type), self.empty_dto)
        self.assertEqual(self.empty_alias, models.Alias.from_dto(self.empty_dto, self.network_type))

    def test_address(self):
        self.assertEqual(self.address_alias.type, models.AliasType.ADDRESS)
        self.assertEqual(self.address_alias.value, self.address)
        self.assertEqual(self.address_alias.address, self.address)

        self.assertEqual(repr(self.address_alias), "Alias(type=<AliasType.ADDRESS: 2>, value=Address(address='SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54', network_type=<NetworkType.MIJIN_TEST: 144>))")
        self.assertEqual(str(self.address_alias), repr(self.address_alias))
        self.assertNotEqual(self.address_alias, models.Alias())
        self.assertEqual(self.address_alias, models.Alias(self.address))
        self.assertNotEqual(self.address_alias, models.Alias(self.mosaic_id))

        with self.assertRaises(ValueError):
            self.address_alias.mosaic_id
        with self.assertRaises(TypeError):
            self.address_alias.__dict__

        self.assertEqual(self.address_alias.to_dto(self.network_type), self.address_dto)
        self.assertEqual(models.Alias.from_dto(self.address_dto, self.network_type), self.address_alias)

    def test_mosaic_id(self):
        self.assertEqual(self.mosaic_alias.type, models.AliasType.MOSAIC_ID)
        self.assertEqual(self.mosaic_alias.value, self.mosaic_id)
        self.assertEqual(self.mosaic_alias.mosaic_id, self.mosaic_id)
        self.assertEqual(self.mosaic_alias.mosaicId, self.mosaic_id)

        self.assertEqual(repr(self.mosaic_alias), "Alias(type=<AliasType.MOSAIC_ID: 1>, value=MosaicId(id=5))")
        self.assertEqual(str(self.mosaic_alias), repr(self.mosaic_alias))
        self.assertNotEqual(self.mosaic_alias, models.Alias())
        self.assertNotEqual(self.mosaic_alias, models.Alias(self.address))
        self.assertEqual(self.mosaic_alias, models.Alias(self.mosaic_id))

        with self.assertRaises(ValueError):
            self.mosaic_alias.address
        with self.assertRaises(TypeError):
            self.mosaic_alias.__dict__

        self.assertEqual(self.mosaic_alias.to_dto(self.network_type), self.mosaic_dto)
        self.assertEqual(models.Alias.from_dto(self.mosaic_dto, self.network_type), self.mosaic_alias)


class TestAliasActionType(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.link = models.AliasActionType.LINK
        self.unlink = models.AliasActionType.UNLINK
        self.dto = 0
        self.catbuffer = b'\x00'

    def test_values(self):
        self.assertEqual(self.link, 0)
        self.assertEqual(self.unlink, 1)

    def test_description(self):
        self.assertEqual(self.link.description(), "Link an alias.")
        self.assertEqual(self.unlink.description(), "Unlink an alias.")

    def test_to_dto(self):
        self.assertEqual(self.link.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.link, models.AliasActionType.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.link.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.link, models.AliasActionType.from_catbuffer(self.catbuffer, self.network_type))


class TestAliasType(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.none = models.AliasType.NONE
        self.mosaic_id = models.AliasType.MOSAIC_ID
        self.address = models.AliasType.ADDRESS
        self.dto = 0
        self.catbuffer = b'\x00'

    def test_values(self):
        self.assertEqual(self.none, 0)
        self.assertEqual(self.mosaic_id, 1)
        self.assertEqual(self.address, 2)

    def test_description(self):
        self.assertEqual(self.none.description(), "No alias.")
        self.assertEqual(self.mosaic_id.description(), "Mosaic ID alias.")
        self.assertEqual(self.address.description(), "Address alias.")

    def test_to_dto(self):
        self.assertEqual(self.none.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.none, models.AliasType.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.none.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.none, models.AliasType.from_catbuffer(self.catbuffer, self.network_type))


class TestEmptyAlias(harness.TestCase):

    def setUp(self):
        public_key = '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246'
        self.network_type = models.NetworkType.MIJIN_TEST
        self.mosaic_id = models.MosaicId(5)
        self.address = models.Address.create_from_public_key(public_key, models.NetworkType.MIJIN_TEST)
        self.alias = models.EmptyAlias()
        self.dto = None

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.alias.__dict__

    def test_init(self):
        self.assertEqual(self.alias.type, models.AliasType.NONE)
        self.assertEqual(self.alias.value, None)

        self.assertEqual(repr(self.alias), 'EmptyAlias(type=<AliasType.NONE: 0>, value=None)')
        self.assertEqual(str(self.alias), repr(self.alias))
        self.assertEqual(self.alias, models.Alias())
        self.assertNotEqual(self.alias, models.Alias(self.address))
        self.assertNotEqual(self.alias, models.Alias(self.mosaic_id))

        with self.assertRaises(ValueError):
            self.alias.address
        with self.assertRaises(ValueError):
            self.alias.mosaic_id

        self.assertEqual(self.alias.to_dto(self.network_type), self.dto)
        self.assertEqual(self.alias, models.Alias.from_dto(self.dto, self.network_type))


class TestMosaicAlias(harness.TestCase):

    def setUp(self):
        public_key = '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246'
        self.network_type = models.NetworkType.MIJIN_TEST
        self.mosaic_id = models.MosaicId(5)
        self.address = models.Address.create_from_public_key(public_key, models.NetworkType.MIJIN_TEST)
        self.alias = models.MosaicAlias(self.mosaic_id)
        self.dto = {'type': 1, 'mosaicId': [5, 0]}

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.alias.__dict__

    def test_init(self):
        self.assertEqual(self.alias.type, models.AliasType.MOSAIC_ID)
        self.assertEqual(self.alias.value, self.mosaic_id)
        self.assertEqual(self.alias.mosaic_id, self.mosaic_id)
        self.assertEqual(self.alias.mosaicId, self.mosaic_id)

        self.assertEqual(repr(self.alias), "MosaicAlias(type=<AliasType.MOSAIC_ID: 1>, value=MosaicId(id=5))")
        self.assertEqual(str(self.alias), repr(self.alias))
        self.assertNotEqual(self.alias, models.Alias())
        self.assertNotEqual(self.alias, models.Alias(self.address))
        self.assertEqual(self.alias, models.Alias(self.mosaic_id))

        with self.assertRaises(ValueError):
            self.alias.address

        self.assertEqual(self.alias.to_dto(self.network_type), self.dto)
        self.assertEqual(self.alias, models.Alias.from_dto(self.dto, self.network_type))


class TestNamespaceId(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.namespace_id = models.NamespaceId(5)
        self.dto = [5, 0]
        self.catbuffer = b'\x05\x00\x00\x00\x00\x00\x00\x00'

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
        with self.assertRaises(TypeError):
            self.namespace_id.__dict__

    def test_int(self):
        self.assertEqual(int(self.namespace_id), 5)

    def test_index(self):
        self.assertEqual(hex(self.namespace_id), "0x5")

    def test_format(self):
        value = models.NamespaceId(5)
        self.assertEqual(f'{value:x}', '5')
        self.assertEqual(f'{value:X}', '5')

        value = models.NamespaceId(13)
        self.assertEqual(f'{value:x}', 'd')
        self.assertEqual(f'{value:X}', 'D')

    def test_repr(self):
        self.assertEqual(repr(self.namespace_id), "NamespaceId(id=5)")

    def test_str(self):
        self.assertEqual(str(self.namespace_id), repr(self.namespace_id))

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
        self.assertEqual(self.namespace_id.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.namespace_id, models.NamespaceId.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.namespace_id.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.namespace_id, models.NamespaceId.from_catbuffer(self.catbuffer, self.network_type))


class TestNamespaceInfo(harness.TestCase):
    # TODO(ahuszagh) Implement...
    pass


class TestNamespaceName(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.namespace_id = models.NamespaceId(0x88B64C3BE2F47144)
        self.name = "sample"
        self.namespace_name = models.NamespaceName(self.namespace_id, self.name)
        self.dto = {'namespaceId': [3807670596, 2293648443], 'name': 'sample'}

    def test_init(self):
        self.assertEqual(self.namespace_name.namespace_id, self.namespace_id)
        self.assertEqual(self.namespace_name.name, self.name)
        self.assertEqual(self.namespace_name.namespaceId, self.namespace_id)

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.namespace_name.__dict__

    def test_create_from_name(self):
        value = models.NamespaceName.create_from_name("sample")
        self.assertEqual(value.namespace_id, self.namespace_id)
        self.assertEqual(value.name, self.name)

    def test_repr(self):
        self.assertEqual(repr(self.namespace_name), "NamespaceName(namespace_id=NamespaceId(id=9851145055013990724), name='sample')")

    def test_str(self):
        self.assertEqual(str(self.namespace_name), repr(self.namespace_name))

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
        self.assertEqual(self.namespace_name.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.namespace_name, models.NamespaceName.from_dto(self.dto, self.network_type))


class TestNamespaceType(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.root = models.NamespaceType.ROOT_NAMESPACE
        self.sub = models.NamespaceType.SUB_NAMESPACE
        self.dto = 0
        self.catbuffer = b'\x00'

    def test_values(self):
        self.assertEqual(self.root, 0)
        self.assertEqual(self.sub, 1)

    def test_description(self):
        self.assertEqual(self.root.description(), "Root namespace.")
        self.assertEqual(self.sub.description(), "Sub namespace.")

    def test_to_dto(self):
        self.assertEqual(self.root.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.root, models.NamespaceType.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.root.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.root, models.NamespaceType.from_catbuffer(self.catbuffer, self.network_type))
