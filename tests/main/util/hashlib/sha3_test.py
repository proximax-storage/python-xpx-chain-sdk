import binascii

from Crypto.Hash import SHA3_224, SHA3_256, SHA3_384, SHA3_512
from xpxchain.util import hashlib
from tests import harness
from .helper import *

HASH = {
    224: SHA3_224,
    256: SHA3_256,
    384: SHA3_384,
    512: SHA3_512,
}


def generate_testcase(bits, full_hexdigest):
    name = "sha3_{}".format(bits)
    digest_size = bits // 8
    func = getattr(hashlib, name)
    func_c = HASH[bits].new

    class Sha3Test(harness.TestCase):

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

    return Sha3Test


TestSha3224 = generate_testcase(224, "716596afadfa17cd1cb35133829a02b03e4eed398ce029ce78a2161d")
TestSha3256 = generate_testcase(256, "d0e47486bbf4c16acac26f8b653592973c1362909f90262877089f9c8a4536af")
TestSha3384 = generate_testcase(384, "f324cbd421326a2abaedf6f395d1a51e189d4a71c755f531289e519f079b224664961e385afcc37da348bd859f34fd1c")
TestSha3512 = generate_testcase(512, "32400b5e89822de254e8d5d94252c52bdcb27a3562ca593e980364d9848b8041b98eabe16c1a6797484941d2376864a1b0e248b0f7af8b1555a778c336a5bf48")
