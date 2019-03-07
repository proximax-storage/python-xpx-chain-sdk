import base64
import warnings

from nem2 import models
from tests import harness


class TestAccount(harness.TestCase):

    def setUp(self):
        self.private_key = "97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca"
        self.public_key = "1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955"
        self.network_type = models.NetworkType.MAIN_NET
        self.address = models.Address.create_from_public_key(self.public_key, self.network_type)

    def test_init(self):
        value = models.Account(self.address, self.public_key, self.private_key)
        self.assertEqual(value.address, self.address)
        self.assertEqual(value.public_key, self.public_key)
        self.assertEqual(value.private_key, self.private_key)

    def test_properties(self):
        value = models.Account(self.address, self.public_key, self.private_key)
        self.assertEqual(value.address.address, "NAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGBSM5RH7")
        self.assertEqual(value.public_key, self.public_key)
        self.assertEqual(value.private_key, self.private_key)
        self.assertEqual(value.network_type, self.network_type)
        self.assertEqual(value.public_account, models.PublicAccount(self.address, self.public_key))

        self.assertEqual(value.publicKey, value.public_key)
        self.assertEqual(value.privateKey, value.private_key)
        self.assertEqual(value.networkType, value.network_type)
        self.assertEqual(value.public_account, value.publicAccount)

    def test_create_from_private_key(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            value = models.Account.create_from_private_key(self.private_key, self.network_type)
            self.assertEqual(value.address, self.address)
            self.assertEqual(value.public_key, self.public_key)
            self.assertEqual(value.private_key, self.private_key)

    def test_generate_new_account(self):
        def fake_entropy(size: int) -> bytes:
            return b'0' * size

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # try the random version
            value = models.Account.generate_new_account(self.network_type)
            message = b'Hello World!'
            signature = value.sign_data(message)
            self.assertTrue(value.public_account.verify_signature(message, signature))

            # try with a deterministic version
            value = models.Account.generate_new_account(self.network_type, fake_entropy)
            self.assertEqual(value.address.address, 'NA4PGCTZHFCTC5WHYSZCEJZPOO3X7OFBAHZCCC4K')
            self.assertEqual(value.public_key, 'dcedb3902b8fa33f8ced2c9ea62497ae4f43e8208cdedaf4d7cac50abc53ddac')
            self.assertEqual(value.private_key, '3030303030303030303030303030303030303030303030303030303030303030')
            signature = value.sign_data(message)
            self.assertEqual(signature, 'bbe720fa06fe26f79896f5880baf7e8d112d796c648c56414e2079349baff54c5d46ab08115fad1865de2288a1eeecfaedc3143df14fc81841aec17fa8cba70e')
            self.assertTrue(value.public_account.verify_signature(message, signature))

    # TODO(ahuszagh) Implement....
    # sign

    def test_sign_data(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            value = models.Account(self.address, self.public_key, self.private_key)
            message = b'Hello World!'
            signature = value.sign_data(message)
            self.assertEqual(signature, '40af0cb5a7a7533f07a4ba6f1cb2df64f2347feb1b2eaabb9374d28603d146497ea83d3d6ee15758d39c298b48f58e578cc42f36a373e15eef7412e0bd19a801')

    def test_repr(self):
        value = models.Account(self.address, self.public_key, self.private_key)
        self.assertEqual(repr(value), "Account(address=Address(address='NAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGBSM5RH7', network_type=<NetworkType.MAIN_NET: 104>), public_key='1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955', private_key='97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca')")

    def test_str(self):
        value = models.Account(self.address, self.public_key, self.private_key)
        self.assertEqual(str(value), 'Account(address=Address(address=NAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGBSM5RH7, network_type=NetworkType.MAIN_NET), public_key=1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955, private_key=97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca)')

    def test_eq(self):
        a1 = models.Account(self.address, self.public_key, self.private_key)
        a2 = models.Account(self.address, self.public_key, self.private_key)
        a3 = models.Account(self.address, self.public_key, self.private_key[:-1] + 'b')

        self.assertTrue(a1 == a1)
        self.assertTrue(a1 == a2)
        self.assertFalse(a1 == a3)
        self.assertTrue(a2 == a2)
        self.assertFalse(a2 == a3)
        self.assertTrue(a3 == a3)


class TestAccountInfo(harness.TestCase):
    pass    # TODO(ahuszagh) Implement...


class TestAddress(harness.TestCase):

    def setUp(self):
        self.plain = "SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54"
        self.pretty = "SD5DT3-CH4BLA-BL5HIM-EKP2TA-PUKF4N-Y3L5HR-IR54"
        self.encoded = b"\x90\xfa9\xecG\xe0V\x00\xaf\xa7C\x08\xa7\xea`}\x14^7\x1b_O\x14G\xbc"

    def test_init(self):
        value = models.Address(self.pretty)
        self.assertEqual(value.address, self.plain)
        self.assertEqual(value.network_type, models.NetworkType.MIJIN_TEST)

    def test_properties(self):
        value = models.Address(self.pretty)
        self.assertEqual(value.address, self.plain)
        self.assertEqual(value.network_type, models.NetworkType.MIJIN_TEST)
        self.assertEqual(value.encoded, self.encoded)

        self.assertEqual(value.networkType, value.network_type)

    def test_create_from_raw_address(self):
        value = models.Address.create_from_raw_address(self.pretty)
        self.assertEqual(value.address, self.plain)
        self.assertEqual(value.network_type, models.NetworkType.MIJIN_TEST)

        self.assertEqual(value, models.Address.createFromRawAddress(value.address))

    def test_create_from_encoded(self):
        value = models.Address.create_from_encoded(self.encoded)
        self.assertEqual(value.address, self.plain)
        self.assertEqual(value.network_type, models.NetworkType.MIJIN_TEST)

        self.assertEqual(value, models.Address.createFromEncoded(value.encoded))

    def test_create_from_public_key(self):
        public_key = '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246'

        value = models.Address.create_from_public_key(public_key, models.NetworkType.MAIN_NET)
        self.assertEqual(value.address, 'ND5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L4CNFATI')

        value = models.Address.create_from_public_key(public_key, models.NetworkType.TEST_NET)
        self.assertEqual(value.address, 'TD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L4SH3LND')

        value = models.Address.create_from_public_key(public_key, models.NetworkType.MIJIN)
        self.assertEqual(value.address, 'MD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L4R2R2JH')

        value = models.Address.create_from_public_key(public_key, models.NetworkType.MIJIN_TEST)
        self.assertEqual(value.address, 'SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54')

        self.assertEqual(value, models.Address.createFromPublicKey(public_key, value.network_type))

    def test_plain(self):
        value = models.Address.create_from_raw_address(self.pretty)
        self.assertEqual(value.plain(), self.plain)

    def test_pretty(self):
        value = models.Address.create_from_raw_address(self.pretty)
        self.assertEqual(value.pretty(), self.pretty)

    def test_is_valid(self):
        value = models.Address.create_from_raw_address(self.pretty)
        self.assertTrue(value.is_valid())

        value = models.Address.create_from_raw_address("SD5DT3-CH4BLA-BL5HIM-EKP2TA-PUKF4N-Y3L5HR-IR55")
        self.assertFalse(value.is_valid())

        self.assertFalse(value.isValid())

    def test_repr(self):
        value = models.Address.create_from_raw_address(self.pretty)
        self.assertEqual(repr(value), "Address(address='SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54', network_type=<NetworkType.MIJIN_TEST: 144>)")

    def test_str(self):
        value = models.Address.create_from_raw_address(self.plain)
        self.assertEqual(str(value), "Address(address=SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54, network_type=NetworkType.MIJIN_TEST)")

    def test_eq(self):
        a1 = models.Address.create_from_raw_address(self.plain)
        a2 = models.Address.create_from_raw_address(self.pretty)
        a3 = models.Address.create_from_raw_address("NALICE2A73DLYTP4365GNFCURAUP3XVBFO7YNYOW")

        self.assertTrue(a1 == a1)
        self.assertTrue(a1 == a2)
        self.assertFalse(a1 == a3)
        self.assertTrue(a2 == a2)
        self.assertFalse(a2 == a3)
        self.assertTrue(a3 == a3)

    def test_to_dto(self):
        value = models.Address.create_from_raw_address(self.pretty)
        dto = value.to_dto()
        self.assertEqual(dto['address'], self.plain)
        self.assertEqual(dto['networkType'], value.network_type)
        self.assertEqual(value, models.Address.createFromRawAddress(value.address))
        self.assertEqual(value.to_dto(), value.toDto())

    def test_from_dto(self):
        value = models.Address.create_from_raw_address(self.plain)
        self.assertEqual(value.address, self.plain)
        self.assertEqual(value.network_type, models.NetworkType.MIJIN_TEST)
        self.assertEqual(value, models.Address.from_dto(value.to_dto()))
        self.assertEqual(value, models.Address.fromDto(value.to_dto()))

    def test_to_catbuffer(self):
        value = models.Address.create_from_raw_address(self.plain)
        self.assertEqual(value.to_catbuffer(), self.encoded)
        self.assertEqual(value.to_catbuffer(), value.toCatbuffer())

    def test_from_catbuffer(self):
        value, rem = models.Address.from_catbuffer(self.encoded)
        self.assertEqual(value.address, self.plain)
        self.assertEqual(value.network_type, models.NetworkType.MIJIN_TEST)
        self.assertEqual(value, models.Address.fromCatbuffer(value.encoded)[0])
        self.assertEqual(rem, b'')

    def test_serialize(self):
        value = models.Address.create_from_raw_address(self.pretty)
        self.assertEqual(value.serialize(models.InterchangeFormat.DTO), value.to_dto())
        self.assertEqual(value.serialize(models.InterchangeFormat.CATBUFFER), value.to_catbuffer())

    def test_deserialize(self):
        value = models.Address.create_from_raw_address(self.pretty)
        self.assertEqual(models.Address.deserialize(value.to_dto(), models.InterchangeFormat.DTO), value)
        self.assertEqual(models.Address.deserialize(value.to_catbuffer(), models.InterchangeFormat.CATBUFFER), value)


class TestMultisigAccountGraphInfo(harness.TestCase):
    pass    # TODO(ahuszagh) Implement...


class TestMultisigAccountInfo(harness.TestCase):
    pass    # TODO(ahuszagh) Implement...


class TestPublicAccount(harness.TestCase):

    def setUp(self):
        self.public_key = "1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955"
        self.network_type = models.NetworkType.MAIN_NET
        self.address = models.Address.create_from_public_key(self.public_key, self.network_type)

    def test_init(self):
        value = models.PublicAccount(self.address, self.public_key)
        self.assertEqual(value.address, self.address)
        self.assertEqual(value.public_key, self.public_key)

    def test_properties(self):
        value = models.PublicAccount(self.address, self.public_key)
        self.assertEqual(value.address.address, "NAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGBSM5RH7")
        self.assertEqual(value.public_key, self.public_key)
        self.assertEqual(value.network_type, self.network_type)

        self.assertEqual(value.publicKey, value.public_key)
        self.assertEqual(value.networkType, value.network_type)

    def test_create_from_public_key(self):
        value = models.PublicAccount.create_from_public_key(self.public_key, self.network_type)
        self.assertEqual(value.address, self.address)
        self.assertEqual(value.public_key, self.public_key)

        self.assertEqual(value, models.PublicAccount.createFromPublicKey(value.public_key, value.network_type))

    def test_verify_signature(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            value = models.PublicAccount(self.address, self.public_key)
            message = b'Hello World!'
            signature = '40af0cb5a7a7533f07a4ba6f1cb2df64f2347feb1b2eaabb9374d28603d146497ea83d3d6ee15758d39c298b48f58e578cc42f36a373e15eef7412e0bd19a801'
            self.assertTrue(value.verify_signature(message, signature))
            self.assertTrue(value.verifySignature(message, signature))

    def test_repr(self):
        value = models.PublicAccount(self.address, self.public_key)
        self.assertEqual(repr(value), "PublicAccount(address=Address(address='NAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGBSM5RH7', network_type=<NetworkType.MAIN_NET: 104>), public_key='1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955')")

    def test_str(self):
        value = models.PublicAccount(self.address, self.public_key)
        self.assertEqual(str(value), "PublicAccount(address=Address(address=NAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGBSM5RH7, network_type=NetworkType.MAIN_NET), public_key=1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955)")

    def test_eq(self):
        a1 = models.PublicAccount(self.address, self.public_key)
        a2 = models.PublicAccount(self.address, self.public_key)
        a3 = models.PublicAccount(self.address, self.public_key[:-1] + 'b')

        self.assertTrue(a1 == a1)
        self.assertTrue(a1 == a2)
        self.assertFalse(a1 == a3)
        self.assertTrue(a2 == a2)
        self.assertFalse(a2 == a3)
        self.assertTrue(a3 == a3)
