import binascii

from Crypto.Hash import RIPEMD160 as ripemd160_c
from xpxchain.util import hashlib
from tests import harness
from .helper import *


class TestRipemd160(harness.TestCase):

    def setUp(self):
        self.full_hexdigest = '8476ee4631b9b30ac2754b0ee0c47e161d3f724c'

    def test_init(self):
        actual = hexdigest(hashlib.ripemd160(), b'Hello World!')
        expected = hexdigest(ripemd160_c.new(), b'Hello World!')
        self.assertEqual(actual, expected)

    def test_properties(self):
        hasher = hashlib.ripemd160()
        self.assertEqual(hasher.digest_size, 20)

    def test_update(self):
        hasher = hashlib.ripemd160()
        hasher.update(b'Hello')
        hasher.update(b' ')
        hasher.update(b'World!')
        self.assertEqual(hasher.hexdigest(), self.full_hexdigest)

    def test_digest(self):
        self.assertEqual(digest(hashlib.ripemd160(), b'Hello World!'), binascii.unhexlify(self.full_hexdigest))

    def test_hexdigest(self):
        self.assertEqual(hexdigest(hashlib.ripemd160(), b'Hello World!'), self.full_hexdigest)

    def test_bytes(self):
        for test in STRING_TESTS:
            actual = hexdigest(hashlib.ripemd160(), test)
            expected = hexdigest(ripemd160_c.new(), test)
            self.assertEqual(actual, expected)
