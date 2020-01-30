import binascii
import warnings

from xpxchain.util.signature.ed25519 import sha3 as ed25519
from tests import harness

# DUMMY DATA
# Never use this private key for real data.
SIGNING_KEY = '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955'
VERIFYING_KEY = '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955'
MESSAGE = '68656c6c6f20776f726c64'
SIGNATURE = '80b2168f89f1197b3c00cb8555ada77a5866e5d14ebdc907467fe4ad2da204348333adcdf3a267b395e3a6b4a50ce9021a5a017885a5882f33a6d1c8f64a2d0d'


class TestEd25519Sha3(harness.TestCase):

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
