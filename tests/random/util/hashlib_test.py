from xpxchain.util import hashlib
from tests import harness


class TestHashFunctions(harness.TestCase):

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_ripemd160(self, data: bytes):
        self.assertEqual(len(hashlib.ripemd160(data).digest()), 20)

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_keccak224(self, data: bytes):
        self.assertEqual(len(hashlib.keccak_224(data).digest()), 28)

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_keccak256(self, data: bytes):
        self.assertEqual(len(hashlib.keccak_256(data).digest()), 32)

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_keccak384(self, data: bytes):
        self.assertEqual(len(hashlib.keccak_384(data).digest()), 48)

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_keccak512(self, data: bytes):
        self.assertEqual(len(hashlib.keccak_512(data).digest()), 64)

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_sha224(self, data: bytes):
        self.assertEqual(len(hashlib.sha224(data).digest()), 28)

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_sha256(self, data: bytes):
        self.assertEqual(len(hashlib.sha256(data).digest()), 32)

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_sha384(self, data: bytes):
        self.assertEqual(len(hashlib.sha384(data).digest()), 48)

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_sha512(self, data: bytes):
        self.assertEqual(len(hashlib.sha512(data).digest()), 64)

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_sha3_224(self, data: bytes):
        self.assertEqual(len(hashlib.sha3_224(data).digest()), 28)

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_sha3_256(self, data: bytes):
        self.assertEqual(len(hashlib.sha3_256(data).digest()), 32)

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_sha3_384(self, data: bytes):
        self.assertEqual(len(hashlib.sha3_384(data).digest()), 48)

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_sha3_512(self, data: bytes):
        self.assertEqual(len(hashlib.sha3_512(data).digest()), 64)
