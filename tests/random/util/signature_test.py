from xpxchain.util.signature import ed25519
from tests import harness


class TestEd25519(harness.TestCase):

    @harness.randomize(
        calls=100,
        seed={'fixed_length': 32},
        message={'min_length': 0, 'max_length': 100}
    )
    def test_sha2(self, seed: bytes, message: bytes):
        sk1 = ed25519.sha2.SigningKey(seed)
        vk1 = sk1.get_verifying_key()
        sig1 = sk1.sign(message)

        # Test success.
        self.assertEqual(sk1.to_seed(), seed)
        vk1.verify(sig1, message)

        # Test invalid key.
        sk2 = ed25519.sha2.SigningKey(seed[16:] + seed[:16])
        vk2 = sk2.get_verifying_key()
        self.assertNotEqual(sk2.to_seed(), seed)
        with self.assertRaises(ed25519.sha2.BadSignatureError):
            vk2.verify(sig1, message)

        # Test invalid signature.
        sig2 = sig1[32:] + sig1[:32]
        with self.assertRaises(ed25519.sha2.BadSignatureError):
            vk1.verify(sig2, message)

    @harness.randomize(
        calls=100,
        seed={'fixed_length': 32},
        message={'min_length': 0, 'max_length': 100}
    )
    def test_sha3(self, seed: bytes, message: bytes):
        sk1 = ed25519.sha3.SigningKey(seed)
        vk1 = sk1.get_verifying_key()
        sig1 = sk1.sign(message)

        # Test success.
        self.assertEqual(sk1.to_seed(), seed)
        vk1.verify(sig1, message)

        # Test invalid key.
        sk2 = ed25519.sha3.SigningKey(seed[16:] + seed[:16])
        vk2 = sk2.get_verifying_key()
        self.assertNotEqual(sk2.to_seed(), seed)
        with self.assertRaises(ed25519.sha3.BadSignatureError):
            vk2.verify(sig1, message)

        # Test invalid signature.
        sig2 = sig1[32:] + sig1[:32]
        with self.assertRaises(ed25519.sha3.BadSignatureError):
            vk1.verify(sig2, message)
