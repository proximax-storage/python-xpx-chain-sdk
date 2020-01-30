import binascii

from Crypto.Hash import SHA224, SHA256, SHA384, SHA512
from xpxchain.util import hashlib
from tests import harness
from .helper import *

HASH = {
    224: SHA224,
    256: SHA256,
    384: SHA384,
    512: SHA512,
}


def generate_testcase(bits, full_hexdigest):
    name = "sha{}".format(bits)
    digest_size = bits // 8
    func = getattr(hashlib, name)
    func_c = HASH[bits].new

    class Sha2Test(harness.TestCase):

        def test_init(self):
            actual = hexdigest(func(), b'Hello World!')
            expected = hexdigest(func_c(), b'Hello World!')
            self.assertEqual(actual, expected)

        def test_properties(self):
            hasher = func()
            self.assertEqual(hasher.digest_size, digest_size)

        def test_update(self):
            hasher = func()
            hasher.update(b'Hello')
            hasher.update(b' ')
            hasher.update(b'World!')
            self.assertEqual(hasher.hexdigest(), full_hexdigest)

        def test_digest(self):
            self.assertEqual(digest(func(), b'Hello World!'), binascii.unhexlify(full_hexdigest))

        def test_hexdigest(self):
            self.assertEqual(hexdigest(func(), b'Hello World!'), full_hexdigest)

        def test_bytes(self):
            for test in STRING_TESTS:
                actual = hexdigest(func(), test)
                expected = hexdigest(func_c(), test)
                self.assertEqual(actual, expected)

    return Sha2Test


TestSha3224 = generate_testcase(224, "4575bb4ec129df6380cedde6d71217fe0536f8ffc4e18bca530a7a1b")
TestSha3256 = generate_testcase(256, "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069")
TestSha3384 = generate_testcase(384, "bfd76c0ebbd006fee583410547c1887b0292be76d582d96c242d2a792723e3fd6fd061f9d5cfd13b8f961358e6adba4a")
TestSha3512 = generate_testcase(512, "861844d6704e8573fec34d967e20bcfef3d424cf48be04e6dc08f2bd58c729743371015ead891cc3cf1c9d34b49264b510751b1ff9e537937bc46b5d6ff4ecc8")
