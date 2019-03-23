from nem2 import models
from tests import harness


@harness.model_test_case({
    'type': models.AddressAlias,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'value': models.Address('SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54'),
    },
    # TODO(ahuszagh) Check the format, and confirm.
    # https://nem2.slack.com/archives/CEZKUE4KB/p1553274126174200
    'dto': {
        'type': 2,
        'address': '90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
    },
    'extras': {
        'mosaic_id': models.MosaicId(5),
    },
})
class TestAddressAlias(harness.TestCase):

    def test_rich_eq(self):
        empty_alias = models.Alias()
        address_alias = models.Alias(models.AliasType.ADDRESS, self.data['value'])
        mosaic_alias = models.Alias(models.AliasType.MOSAIC_ID, self.extras['mosaic_id'])

        self.assertNotEqual(self.model, empty_alias)
        self.assertEqual(self.model, address_alias)
        self.assertNotEqual(self.model, mosaic_alias)

    def test_properties(self):
        with self.assertRaises(ValueError):
            self.model.mosaic_id


@harness.model_test_case({
    'type': models.Alias,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'type': models.AliasType.ADDRESS,
        'value': models.Address('SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54'),
    },
    # TODO(ahuszagh) Check the format, and confirm.
    # https://nem2.slack.com/archives/CEZKUE4KB/p1553274126174200
    'dto': {
        'type': 2,
        'address': '90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
    },
})
class TestAliasAddress(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.Alias,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'type': models.AliasType.NONE,
        'value': None,
    },
    'eq': False,
    'dto': {
        'type': 0,
    },
})
class TestAliasEmpty(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.Alias,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'type': models.AliasType.MOSAIC_ID,
        'value': models.MosaicId(5),
    },
    'dto': {
        'type': 1,
        'mosaicId': [5, 0],
    },
})
class TestAliasMosaicId(harness.TestCase):
    pass


@harness.enum_test_case({
    'type': models.AliasActionType,
    'enums': [
        models.AliasActionType.LINK,
        models.AliasActionType.UNLINK,
    ],
    'values': [
        0,
        1,
    ],
    'descriptions': [
        'Link an alias.',
        'Unlink an alias.',
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
class TestAliasActionType(harness.TestCase):
    pass


@harness.enum_test_case({
    'type': models.AliasType,
    'enums': [
        models.AliasType.NONE,
        models.AliasType.MOSAIC_ID,
        models.AliasType.ADDRESS,
    ],
    'values': [
        0,
        1,
        2,
    ],
    'descriptions': [
        'No alias.',
        'Mosaic ID alias.',
        'Address alias.',
    ],
    'dto': [
        0,
        1,
        2,
    ],
    'catbuffer': [
        b'\x00',
        b'\x01',
        b'\x02',
    ],
})
class TestAliasType(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.EmptyAlias,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'value': None,
    },
    'eq': False,
    'dto': {
        'type': 0,
    },
    'extras': {
        'address': models.Address('SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54'),
        'mosaic_id': models.MosaicId(5),
    },
})
class TestEmptyAlias(harness.TestCase):

    def test_rich_eq(self):
        empty_alias = models.Alias()
        address_alias = models.Alias(models.AliasType.ADDRESS, self.extras['address'])
        mosaic_alias = models.Alias(models.AliasType.MOSAIC_ID, self.extras['mosaic_id'])

        self.assertEqual(self.model, empty_alias)
        self.assertNotEqual(self.model, address_alias)
        self.assertNotEqual(self.model, mosaic_alias)

    def test_properties(self):
        with self.assertRaises(ValueError):
            self.model.address
        with self.assertRaises(ValueError):
            self.model.mosaic_id


@harness.model_test_case({
    'type': models.MosaicAlias,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'value': models.MosaicId(5),
    },
    'dto': {
        'type': 1,
        'mosaicId': [5, 0],
    },
    'extras': {
        'address': models.Address('SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54'),
    },
})
class TestMosaicAlias(harness.TestCase):

    def test_rich_eq(self):
        empty_alias = models.Alias()
        address_alias = models.Alias(models.AliasType.ADDRESS, self.extras['address'])
        mosaic_alias = models.Alias(models.AliasType.MOSAIC_ID, self.data['value'])

        self.assertNotEqual(self.model, empty_alias)
        self.assertNotEqual(self.model, address_alias)
        self.assertEqual(self.model, mosaic_alias)

    def test_properties(self):
        with self.assertRaises(ValueError):
            self.model.address


@harness.model_test_case({
    'type': models.NamespaceId,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'id': 5,
    },
    'dto': [5, 0],
    'catbuffer': b'\x05\x00\x00\x00\x00\x00\x00\x00',
})
class TestNamespaceId(harness.TestCase):

    def test_init(self):
        self.assertEqual(self.type(5).id, 5)
        self.assertEqual(self.type("").id, 0)
        self.assertEqual(self.type("sample").id, 0x88B64C3BE2F47144)
        self.assertEqual(self.type("sample.sub").id, 0xFA9429715A71ACC9)
        self.assertEqual(self.type("sample.sub.full").id, 0x8BC7011B0B344C54)

    def test_encoded(self):
        def encode(value):
            return self.type(value).encoded

        self.assertEqual('0500000000000000', self.model.encoded)
        self.assertEqual('4bfa5f372d55b384', encode(0x84b3552d375ffa4b))
        self.assertEqual('08a12f89ee5a49f8', encode(0xf8495aee892fa108))
        self.assertEqual('1f810565e8f4aeab', encode(0xabaef4e86505811f))
        self.assertEqual('552d1c0a2bc9b8ae', encode(0xaeb8c92b0a1c2d55))
        self.assertEqual('bfca1440d49ae090', encode(0x90e09ad44014cabf))
        self.assertEqual('ccf10b96814211ab', encode(0xab114281960bf1cc))

    def test_create_from_encoded(self):
        def from_encoded(value):
            return self.type.create_from_encoded(value)

        def test_from_encoded(value):
            self.assertEqual(from_encoded(value).encoded, value)

        test_from_encoded('4bfa5f372d55b384')
        test_from_encoded('08a12f89ee5a49f8')
        test_from_encoded('1f810565e8f4aeab')
        test_from_encoded('552d1c0a2bc9b8ae')
        test_from_encoded('bfca1440d49ae090')
        test_from_encoded('ccf10b96814211ab')

    def test_int(self):
        self.assertEqual(int(self.model), 5)

    def test_index(self):
        self.assertEqual(hex(self.model), "0x5")

    def test_format(self):
        value = self.type(5)
        self.assertEqual(f'{value:x}', '5')
        self.assertEqual(f'{value:X}', '5')

        value = self.type(13)
        self.assertEqual(f'{value:x}', 'd')
        self.assertEqual(f'{value:X}', 'D')


@harness.model_test_case({
    'type': models.NamespaceInfo,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'active': True,
        'index': 0,
        'meta_id': '5c7c07005cc1fe000176fa2b',
        'type': models.NamespaceType.ROOT_NAMESPACE,
        'depth': 1,
        'levels': [
            models.NamespaceId(0x84b3552d375ffa4b),
        ],
        'parent_id': models.NamespaceId(0),
        'owner': models.PublicAccount.create_from_public_key('7a562888c7ae1e082579951d6d93bf931de979360acca4c4085d754e5e122808', models.NetworkType.MIJIN_TEST),
        'start_height': 1,
        'end_height': 0xffffffffffffffff,
        'alias': models.Alias(),
    },
    'dto': {
        'meta': {
            'active': True,
            'index': 0,
            'id': '5c7c07005cc1fe000176fa2b'
        },
        'namespace': {
            'type': 0,
            'depth': 1,
            'level0': [929036875, 2226345261],
            'parentId': [0, 0],
            'owner': '7a562888c7ae1e082579951d6d93bf931de979360acca4c4085d754e5e122808',
            'ownerAddress': '90f6c07a4cf9ad1bf0644d419218b72fcdf1efcc07a6c9202c',
            'startHeight': [1, 0],
            'endHeight': [4294967295, 4294967295]
        }
    },
})
class TestNamespaceInfo(harness.TestCase):

    def test_properties(self):
        self.assertEqual(self.model.id, models.NamespaceId(0x84b3552d375ffa4b))
        self.assertTrue(self.model.is_root())
        self.assertFalse(self.model.is_subnamespace())
        self.assertFalse(self.model.has_alias())

        with self.assertRaises(ValueError):
            self.model.parent_namespace_id()


@harness.model_test_case({
    'type': models.NamespaceName,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'namespace_id': models.NamespaceId(0x88b64c3be2f47144),
        'name': 'sample'
    },
    'dto': {
        'namespaceId': [0xe2f47144, 0x88b64c3b],
        'name': 'sample'
    },
})
class TestNamespaceNameDepth1(harness.TestCase):

    def test_create_from_name(self):
        self.assertEqual(self.model, self.type.create_from_name("sample"))


@harness.model_test_case({
    'type': models.NamespaceName,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'namespace_id': models.NamespaceId(0xfa9429715a71acc9),
        'name': 'sample.sub'
    },
    'dto': {
        'namespaceId': [0x5a71acc9, 0xfa942971],
        'name': 'sample.sub'
    },
})
class TestNamespaceNameDepth2(harness.TestCase):

    def test_create_from_name(self):
        self.assertEqual(self.model, self.type.create_from_name("sample.sub"))


@harness.model_test_case({
    'type': models.NamespaceName,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'namespace_id': models.NamespaceId(0x8bc7011b0b344c54),
        'name': 'sample.sub.full'
    },
    'dto': {
        'namespaceId': [0x0b344c54, 0x8bc7011b],
        'name': 'sample.sub.full'
    },
})
class TestNamespaceNameDepth3(harness.TestCase):

    def test_create_from_name(self):
        self.assertEqual(self.model, self.type.create_from_name("sample.sub.full"))


@harness.enum_test_case({
    'type': models.NamespaceType,
    'enums': [
        models.NamespaceType.ROOT_NAMESPACE,
        models.NamespaceType.SUB_NAMESPACE,
    ],
    'values': [
        0,
        1,
    ],
    'descriptions': [
        'Root namespace.',
        'Sub namespace.',
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
class TestNamespaceType(harness.TestCase):
    pass
