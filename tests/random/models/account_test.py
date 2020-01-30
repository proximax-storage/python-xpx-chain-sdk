from xpxchain import models
from xpxchain import util
from tests import harness


class TestAccount(harness.TestCase):

    @harness.randomize(key={'fixed_length': 32})
    def test_create_from_private_key(self, key: bytes):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.Account.create_from_private_key(key, network_type)
        pub = models.PublicAccount.create_from_public_key(model.public_key, network_type)
        self.assertTrue(model.address.is_valid())
        self.assertEqual(model.public_account, pub)

    @harness.randomize(key={'fixed_length': 33})
    def test_create_from_invalid_private_key(self, key: bytes):
        network_type = models.NetworkType.MIJIN_TEST
        with self.assertRaises(ValueError):
            models.Account.create_from_private_key(key, network_type)


class TestAddress(harness.TestCase):

    @harness.randomize(address={'pattern': r'[MSXVmsxv][A-Za-z2-7]{39}'})
    def test_mostly_valid(self, address: str):
        model = models.Address(address)
        self.assertEqual(model.address.lower(), address.lower())
        self.assertFalse(model.is_valid())

    @harness.randomize(address={'pattern': r'[A-LN-RT-UY-Za-ln-rt-uy-z][A-Za-z2-7]{39}'})
    def test_invalid_identifier(self, address: str):
        with self.assertRaises(KeyError):
            models.Address(address)

    @harness.randomize(encoded={'fixed_length': 20})
    def test_valid(self, encoded: bytes):
        encoded = b'\x90' + encoded
        checksum = util.hashlib.sha3_256(encoded).digest()[:4]
        model = models.Address.create_from_encoded(encoded + checksum)
        self.assertTrue(model.is_valid())

    @harness.randomize(key={'fixed_length': 32})
    def test_create_from_public_key(self, key: bytes):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.Address.create_from_public_key(key, network_type)
        self.assertTrue(model.is_valid())

    @harness.randomize(key={'fixed_length': 33})
    def test_create_from_invalid_public_key(self, key: bytes):
        network_type = models.NetworkType.MIJIN_TEST
        with self.assertRaises(ValueError):
            models.Address.create_from_public_key(key, network_type)


class TestPublicAccount(harness.TestCase):

    @harness.randomize(key={'fixed_length': 32})
    def test_create_from_public_key(self, key: bytes):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.PublicAccount.create_from_public_key(key, network_type)
        address = models.Address.create_from_public_key(key, network_type)
        self.assertTrue(model.address.is_valid())
        self.assertEqual(model.address, address)

    @harness.randomize(key={'fixed_length': 33})
    def test_create_from_invalid_public_key(self, key: bytes):
        network_type = models.NetworkType.MIJIN_TEST
        with self.assertRaises(ValueError):
            models.PublicAccount.create_from_public_key(key, network_type)
