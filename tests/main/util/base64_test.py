import binascii

from nem2 import util
from tests.harness import TestCase


class Base32Test(TestCase):

    def test_b32encode(self):
        self.assertEqual(util.b32encode(b'5'), 'GU======')
        self.assertEqual(util.b32encode(b'5', with_suffix=False), 'GU')

        with self.assertRaises(TypeError):
            util.b32encode('5')

    def test_b32decode(self):
        self.assertEqual(util.b32decode('GU======'), b'5')
        self.assertEqual(util.b32decode(b'GU======'), b'5')
        self.assertEqual(util.b32decode('GU', with_suffix=False), b'5')
        self.assertEqual(util.b32decode(b'GU', with_suffix=False), b'5')

        with self.assertRaises(binascii.Error):
            util.b32decode('G', with_suffix=False)
        with self.assertRaises(binascii.Error):
            util.b32decode('GU')


class Base64Test(TestCase):

    def test_b64encode(self):
        self.assertEqual(util.b64encode(b'5'), 'NQ==')
        self.assertEqual(util.b64encode(b'5', with_suffix=False), 'NQ')

        with self.assertRaises(TypeError):
            util.b64encode('5')

    def test_b64decode(self):
        self.assertEqual(util.b64decode('NQ=='), b'5')
        self.assertEqual(util.b64decode(b'NQ=='), b'5')
        self.assertEqual(util.b64decode('NQ', with_suffix=False), b'5')
        self.assertEqual(util.b64decode(b'NQ', with_suffix=False), b'5')

        with self.assertRaises(binascii.Error):
            util.b64decode('N', with_suffix=False)
        with self.assertRaises(binascii.Error):
            util.b64decode('NQ')
