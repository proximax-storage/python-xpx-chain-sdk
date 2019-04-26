from nem2 import models
from nem2 import util
from tests import harness


@harness.model_test_case({
    'type': models.Account,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'address': models.Address('SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG'),
        'public_key': '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
    },
})
class TestAccount(harness.TestCase):

    def test_properties(self):
        public_account = models.PublicAccount(self.model.address, self.model.public_key)
        self.assertEqual(self.model.network_type, self.network_type)
        self.assertEqual(self.model.public_account, public_account)

    @harness.ignore_warnings_test
    def test_create_from_private_key(self):
        value = self.type.create_from_private_key(self.data['private_key'], self.network_type)
        self.assertEqual(value, self.model)

    @harness.ignore_warnings_test
    def test_generate_new_account(self):
        def fake_entropy(size: int) -> bytes:
            return b'0' * size

        # try the random version
        value = self.type.generate_new_account(self.network_type)
        message = b'Hello World!'
        signature = value.sign_data(message)
        self.assertTrue(value.public_account.verify_signature(message, signature))

        # try with a deterministic version
        value = self.type.generate_new_account(self.network_type, fake_entropy)
        self.assertEqual(value.address.address, 'SA4PGCTZHFCTC5WHYSZCEJZPOO3X7OFBAHCMSL4U')
        self.assertEqual(value.public_key, 'dcedb3902b8fa33f8ced2c9ea62497ae4f43e8208cdedaf4d7cac50abc53ddac')
        self.assertEqual(value.private_key, '3030303030303030303030303030303030303030303030303030303030303030')
        signature = util.hexlify(value.sign_data(message))
        self.assertEqual(signature, 'bbe720fa06fe26f79896f5880baf7e8d112d796c648c56414e2079349baff54c5d46ab08115fad1865de2288a1eeecfaedc3143df14fc81841aec17fa8cba70e')
        self.assertTrue(value.public_account.verify_signature(message, signature))

    @harness.ignore_warnings_test
    def test_sign(self):
        transaction = 'bb000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        signed = util.hexlify(self.model.sign(transaction))
        self.assertEqual(signed, 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7')

    @harness.ignore_warnings_test
    def test_sign_data(self):
        message = b'Hello World!'
        signature = util.hexlify(self.model.sign_data(message))
        self.assertEqual(signature, '40af0cb5a7a7533f07a4ba6f1cb2df64f2347feb1b2eaabb9374d28603d146497ea83d3d6ee15758d39c298b48f58e578cc42f36a373e15eef7412e0bd19a801')

    @harness.ignore_warnings_test
    def test_verify_signature(self):
        message = b'Hello World!'
        signature = '40af0cb5a7a7533f07a4ba6f1cb2df64f2347feb1b2eaabb9374d28603d146497ea83d3d6ee15758d39c298b48f58e578cc42f36a373e15eef7412e0bd19a801'
        self.assertTrue(self.model.verify_signature(message, signature))

    @harness.ignore_warnings_test
    def test_verify_transaction(self):
        payload = 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.assertTrue(self.model.verify_transaction(payload))

    def test_invalid_keys(self):
        with self.assertRaises(ValueError):
            self.type(self.data['address'], self.data['public_key'], '')
        with self.assertRaises(ValueError):
            self.type(self.data['address'], '', self.data['private_key'])


@harness.model_test_case({
    'type': models.AccountInfo,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'meta': None,
        'address': models.Address('SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM'),
        'address_height': 1,
        'public_key': '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808',
        'public_key_height': 1,
        'mosaics': [],
        'importance': 0,
        'importance_height': 0,
    },
    'dto': {
        'meta': {},
        'account': {
            'address': '90f6c07a4cf9ad1bf0644d419218b72fcdf1efcc07a6c9202c',
            'addressHeight': [1, 0],
            'publicKey': '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808',
            'publicKeyHeight': [1, 0],
            'mosaics': [],
            'importance': [0, 0],
            'importanceHeight': [0, 0],
        },
    }
})
class TestAccountInfo(harness.TestCase):

    def test_properties(self):
        public_account = models.PublicAccount(self.model.address, self.model.public_key)
        self.assertEqual(self.model.public_account, public_account)


class TestAccountMetadata(harness.TestCase):
    pass    # TODO(ahuszagh) Implement...


class TestAccountProperty(harness.TestCase):
    pass    # TODO(ahuszagh) Implement...


class TestAccountProperties(harness.TestCase):
    pass    # TODO(ahuszagh) Implement...


class TestAccountPropertiesInfo(harness.TestCase):
    pass    # TODO(ahuszagh) Implement...


class TestAccountPropertiesMetadata(harness.TestCase):
    pass    # TODO(ahuszagh) Implement...


@harness.model_test_case({
    'type': models.Address,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'address': 'SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54',
    },
    'dto': '90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc',
    'catbuffer': b'\x90\xfa9\xecG\xe0V\x00\xaf\xa7C\x08\xa7\xea`}\x14^7\x1b_O\x14G\xbc',
    'extras': {
        'plain': 'SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54',
        'pretty': 'SD5DT3-CH4BLA-BL5HIM-EKP2TA-PUKF4N-Y3L5HR-IR54',
        'encoded': b'\x90\xfa9\xecG\xe0V\x00\xaf\xa7C\x08\xa7\xea`}\x14^7\x1b_O\x14G\xbc',
        'public_key': '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246',
        'invalid': 'SD5DT3-CH4BLA-BL5HIM-EKP2TA-PUKF4N-Y3L5HR-IR55'
    }
})
class TestAddress(harness.TestCase):

    def test_properties(self):
        self.assertEqual(self.model.network_type, self.network_type)
        self.assertEqual(self.model.encoded, self.extras['encoded'])

    def test_create_from_raw_address(self):
        self.assertEqual(self.model, self.type.create_from_raw_address(self.extras['pretty']))

    def test_create_from_encoded(self):
        self.assertEqual(self.model, self.type.create_from_encoded(self.extras['encoded']))

    def test_create_from_public_key(self):
        public_key = self.extras['public_key']

        value = self.type.create_from_public_key(public_key, models.NetworkType.MAIN_NET)
        self.assertEqual(value.address, 'ND5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L4CNFATI')

        value = self.type.create_from_public_key(public_key, models.NetworkType.TEST_NET)
        self.assertEqual(value.address, 'TD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L4SH3LND')

        value = self.type.create_from_public_key(public_key, models.NetworkType.MIJIN)
        self.assertEqual(value.address, 'MD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L4R2R2JH')

        value = self.type.create_from_public_key(public_key, models.NetworkType.MIJIN_TEST)
        self.assertEqual(value.address, 'SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54')

    def test_plain(self):
        self.assertEqual(self.model.plain(), self.extras['plain'])

    def test_pretty(self):
        self.assertEqual(self.model.pretty(), self.extras['pretty'])

    def test_is_valid(self):
        self.assertTrue(self.type.create_from_raw_address(self.extras['plain']).is_valid())
        self.assertTrue(self.type.create_from_raw_address(self.extras['pretty']).is_valid())
        self.assertFalse(self.type.create_from_raw_address(self.extras['invalid']).is_valid())

    def test_invalid_address(self):
        with self.assertRaises(ValueError):
            self.type('')
        with self.assertRaises(ValueError):
            self.type.create_from_encoded('')
        with self.assertRaises(ValueError):
            self.type.create_from_public_key('', self.network_type)


class TestMultisigAccountGraphInfo(harness.TestCase):
    pass    # TODO(ahuszagh) Implement...


class TestMultisigAccountInfo(harness.TestCase):
    pass    # TODO(ahuszagh) Implement...
    # Now supports DTO, must include that.


class TestPropertyType(harness.TestCase):
    pass    # TODO(ahuszagh) Implement...
    # Now supports DTO/catbuffer, must include that.


@harness.model_test_case({
    'type': models.PublicAccount,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'public_key': '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
        'address': models.Address('SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG'),
    },
    'dto': '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
    'catbuffer': b'\x1b\x15?\x8bv\xef`\xa4\xbf\xe1R\xf4\xde6\x98\xbd#\x0b\xac\x9d\xc29\xd4\xe4HqZ\xa4k\xd5\x89U',
    'extras': {
        'message': b'Hello World!',
        'signature': '40af0cb5a7a7533f07a4ba6f1cb2df64f2347feb1b2eaabb9374d28603d146497ea83d3d6ee15758d39c298b48f58e578cc42f36a373e15eef7412e0bd19a801',
        'payload': 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
    }
})
class TestPublicAccount(harness.TestCase):

    def test_invalid_public_key(self):
        with self.assertRaises(ValueError):
            self.type(self.data['address'], '')

    def test_properties(self):
        self.assertEqual(self.model.network_type, self.network_type)

    def test_create_from_public_key(self):
        self.assertEqual(self.model, self.type.create_from_public_key(self.data['public_key'], self.network_type))

    @harness.ignore_warnings_test
    def test_verify_signature(self):
        self.assertTrue(self.model.verify_signature(self.extras['message'], self.extras['signature']))
        self.assertFalse(self.model.verify_signature(self.extras['message'], '0' * 128))
        with self.assertRaises(ValueError):
            self.assertTrue(self.model.verify_signature(self.extras['message'], ''))

    @harness.ignore_warnings_test
    def test_verify_transaction(self):
        self.assertTrue(self.model.verify_transaction(self.extras['payload']))
