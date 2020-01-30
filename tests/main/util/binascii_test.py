import binascii

from xpxchain import util
from tests import harness


class HexTest(harness.TestCase):

    def test_hexlify(self):
        self.assertEqual(util.hexlify(b'5'), '35')
        self.assertEqual(util.hexlify(b'5', with_prefix=True), '0x35')

        with self.assertRaises(TypeError):
            util.hexlify('5')

    def test_unhexlify(self):
        self.assertEqual(util.unhexlify('35'), b'5')
        self.assertEqual(util.unhexlify(b'35'), b'5')
        self.assertEqual(util.unhexlify('0x35', with_prefix=True), b'5')
        self.assertEqual(util.unhexlify(b'0x35', with_prefix=True), b'5')

        with self.assertRaises(binascii.Error):
            util.unhexlify('5')
        with self.assertRaises(binascii.Error):
            util.unhexlify('0x35')
