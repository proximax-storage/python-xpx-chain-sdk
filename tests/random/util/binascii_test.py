import binascii

from xpxchain import util
from tests import harness


class TestBinascii(harness.TestCase):

    @harness.randomize(calls=100, data={'min_length': 0, 'max_length': 100})
    def test_hex_encoding(self, decoded: bytes):
        encoded = util.hexlify(decoded)
        self.assertEqual(len(encoded), 2 * len(decoded))
        self.assertEqual(util.encode_hex(decoded), encoded)
        self.assertEqual(util.encode_hex(encoded), encoded)
        self.assertEqual(util.unhexlify(encoded), decoded)
        self.assertEqual(util.decode_hex(decoded), decoded)
        self.assertEqual(util.decode_hex(encoded), decoded)

        with self.assertRaises(binascii.Error):
            util.decode_hex(encoded + '0')
        with self.assertRaises(binascii.Error):
            util.decode_hex(encoded[:-1])
