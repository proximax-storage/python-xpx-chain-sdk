import binascii

from xpxchain import util
from tests import harness


class Base32Test(harness.TestCase):

    def test_b32encode(self):
        self.assertEqual(util.b32encode(b'5'), 'GU======')
        self.assertEqual(util.b32encode(b'5', with_suffix=False), 'GU')

        with self.assertRaises(TypeError):
            util.b32encode('5')

    def test_encode_base32(self):
        self.assertEqual(util.encode_base32(b'5'), 'GU======')
        self.assertEqual(util.encode_base32('GU======'), 'GU======')
        self.assertEqual(util.encode_base32('GU======', with_suffix=False), 'GU')

    def test_b32decode(self):
        self.assertEqual(util.b32decode('GU======'), b'5')
        self.assertEqual(util.b32decode(b'GU======'), b'5')
        self.assertEqual(util.b32decode('GU', with_suffix=False), b'5')
        self.assertEqual(util.b32decode(b'GU', with_suffix=False), b'5')

        with self.assertRaises(binascii.Error):
            util.b32decode('G', with_suffix=False)
        with self.assertRaises(binascii.Error):
            util.b32decode('GU')

    def test_decode_base32(self):
        self.assertEqual(util.decode_base32('GU======'), b'5')
        self.assertEqual(util.decode_base32(b'5'), b'5')


class Base64Test(harness.TestCase):

    def test_b64encode(self):
        self.assertEqual(util.b64encode(b'5'), 'NQ==')
        self.assertEqual(util.b64encode(b'5', with_suffix=False), 'NQ')

        with self.assertRaises(TypeError):
            util.b64encode('5')

    def test_encode_base64(self):
        self.assertEqual(util.encode_base64(b'5'), 'NQ==')
        self.assertEqual(util.encode_base64('NQ=='), 'NQ==')
        self.assertEqual(util.encode_base64('NQ==', with_suffix=False), 'NQ')

    def test_b64decode(self):
        self.assertEqual(util.b64decode('NQ=='), b'5')
        self.assertEqual(util.b64decode(b'NQ=='), b'5')
        self.assertEqual(util.b64decode('NQ', with_suffix=False), b'5')
        self.assertEqual(util.b64decode(b'NQ', with_suffix=False), b'5')

        with self.assertRaises(binascii.Error):
            util.b64decode('N', with_suffix=False)
        with self.assertRaises(binascii.Error):
            util.b64decode('NQ')

    def test_decode_base64(self):
        self.assertEqual(util.decode_base64('NQ=='), b'5')
        self.assertEqual(util.decode_base64(b'5'), b'5')
