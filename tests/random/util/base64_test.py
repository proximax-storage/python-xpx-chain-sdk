import binascii
import math

from xpxchain import util
from tests import harness


class TestBase64(harness.TestCase):

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_base32_encoding(self, decoded: bytes):
        encoded = util.b32encode(decoded)
        self.assertEqual(len(encoded), 8 * int(math.ceil(len(decoded) / 5)))
        self.assertEqual(util.b32decode(encoded), decoded)

        with self.assertRaises(binascii.Error):
            util.b32decode(encoded + '0')
        with self.assertRaises(binascii.Error):
            util.b32decode(encoded[:-1])

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_base64_encoding(self, decoded: bytes):
        encoded = util.b64encode(decoded)
        self.assertEqual(len(encoded), 4 * int(math.ceil(len(decoded) / 3)))
        self.assertEqual(util.b64decode(encoded), decoded)

        with self.assertRaises(binascii.Error):
            util.b32decode(encoded + '0')
        with self.assertRaises(binascii.Error):
            util.b32decode(encoded[:-1])
