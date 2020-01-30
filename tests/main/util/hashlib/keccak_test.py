import binascii

from xpxchain.util.hashlib.keccak import crypto
from xpxchain.util.hashlib.keccak import fallback
from tests import harness
from .helper import *


def generate_testcase(bits, full_hexdigest):
    name = "keccak_{}".format(bits)
    digest_size = bits // 8
    crypto_func = getattr(crypto, name)
    fallback_func = getattr(fallback, name)

    class KeccakTest(harness.TestCase):

        def test_init(self):
            actual = hexdigest(fallback_func(), b'Hello World!')
            expected = hexdigest(crypto_func(), b'Hello World!')
            self.assertEqual(actual, expected)

        def test_properties(self):
            hasher = fallback_func()
            self.assertEqual(hasher.digest_size, digest_size)

        def test_update(self):
            hasher = fallback_func()
            hasher.update(b'Hello')
            hasher.update(b' ')
            hasher.update(b'World!')
            self.assertEqual(hasher.hexdigest(), full_hexdigest)

        def test_digest(self):
            self.assertEqual(digest(fallback_func(), b'Hello World!'), binascii.unhexlify(full_hexdigest))

        def test_hexdigest(self):
            self.assertEqual(hexdigest(fallback_func(), b'Hello World!'), full_hexdigest)

        def test_bytes(self):
            for test in STRING_TESTS:
                actual = hexdigest(fallback_func(), test)
                expected = hexdigest(crypto_func(), test)
                self.assertEqual(actual, expected)

    return KeccakTest


TestKeccak224 = generate_testcase(224, "71519a3ec955d57fce5eabf34f64296e80890478eba9e9b36c9c9d5b")
TestKeccak256 = generate_testcase(256, "3ea2f1d0abf3fc66cf29eebb70cbd4e7fe762ef8a09bcc06c8edf641230afec0")
TestKeccak384 = generate_testcase(384, "1f93aefa2bf7e59893b2f29e0a21a58a7e9bbc3f3ce21f3ab3f7d41aa49fa27ca62fd1f42dc99f8497c346a505154b7e")
TestKeccak512 = generate_testcase(512, "75b70545b09569a8d61251b06fc49b520b6ad5322684fd9466836eb143670afdfa25e0403492e0a7dfb7298a9c7e08576bcf26bc9875adfa88e886009cb2fe00")
