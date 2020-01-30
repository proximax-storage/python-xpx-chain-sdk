import binascii
import warnings

from xpxchain.util.signature.ed25519 import sha2 as ed25519
from tests import harness

# DUMMY DATA
# Never use this private key for real data.
SIGNING_KEY = '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca650ecfeda636be59c1b610e90467e4f99628ca2aca770b7535c59c2894b44377'
VERIFYING_KEY = '650ecfeda636be59c1b610e90467e4f99628ca2aca770b7535c59c2894b44377'
MESSAGE = '68656c6c6f20776f726c64'
SIGNATURE = 'bc8d4afa282164cee1f5179ef87c77b2923c6d7fef3c7175b49df765f7cf14a8810c5721716e557efd76e3cf08a2ca85b02dbaae4d010e3ba7a6d9cd2c68260f'


class TestEd25519Sha2(harness.TestCase):

    def setUp(self):
        self.signing_key = ed25519.SigningKey(binascii.unhexlify(SIGNING_KEY))
        self.verifying_key = ed25519.VerifyingKey(binascii.unhexlify(VERIFYING_KEY))
        self.message = binascii.unhexlify(MESSAGE)
        self.signature = binascii.unhexlify(SIGNATURE)

    def test_create_keypair(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # dummy entropy function so we can use existing seed
            entropy = lambda x: self.signing_key.to_seed()[:x]
            signing_key, verifying_key = ed25519.create_keypair(entropy)
            self.assertEqual(signing_key, self.signing_key)
            self.assertEqual(verifying_key, self.verifying_key)

    def test_from_seed(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            seed = self.signing_key.to_seed()
            signing_key = ed25519.SigningKey(seed)
            self.assertEqual(signing_key, self.signing_key)
            self.assertEqual(signing_key.get_verifying_key(), self.verifying_key)

    def test_sign(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            signature = self.signing_key.sign(self.message)
            self.assertEqual(signature, self.signature)

    def test_verify(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            self.verifying_key.verify(self.signature, self.message)

            with self.assertRaises(ed25519.BadSignatureError):
                signature = self.signature[:-1] + b'0'
                self.verifying_key.verify(signature, self.message)

            with self.assertRaises((AssertionError, ValueError)):
                self.verifying_key.verify(self.signature + b'0', self.message)
            with self.assertRaises((AssertionError, ValueError)):
                self.verifying_key.verify(self.signature[:-1], self.message)
