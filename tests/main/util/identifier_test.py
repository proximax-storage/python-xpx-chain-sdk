from xpxchain import util
from tests import harness


class TestIdentifier(harness.TestCase):

    def test_generate_mosaic_id(self):
        nonce = b'\x00\x00\x00\x00'
        public_key = util.unhexlify('7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246')
        self.assertEqual(util.generate_mosaic_id(nonce, public_key), 0x2FF7D64F483BC0A6)

    def test_generate_sub_namespace_id(self):
        self.assertEqual(util.generate_sub_namespace_id(0, "sample"), 0x88B64C3BE2F47144)
        self.assertEqual(util.generate_sub_namespace_id(0x88B64C3BE2F47144, "sub"), 0xFA9429715A71ACC9)
        self.assertEqual(util.generate_sub_namespace_id(0xFA9429715A71ACC9, "full"), 0x8BC7011B0B344C54)

    def test_generate_namespace_id(self):
        ids = [0x88B64C3BE2F47144, 0xFA9429715A71ACC9, 0x8BC7011B0B344C54]
        self.assertEqual(util.generate_namespace_id(""), ids[:0])
        self.assertEqual(util.generate_namespace_id("sample"), ids[:1])
        self.assertEqual(util.generate_namespace_id("sample.sub"), ids[:2])
        self.assertEqual(util.generate_namespace_id("sample.sub.full"), ids)

        with self.assertRaises(ValueError):
            util.generate_namespace_id("sample.sub.full.overload")
        with self.assertRaises(ValueError):
            util.generate_namespace_id("-sample")
        with self.assertRaises(ValueError):
            util.generate_namespace_id("_sample")
        with self.assertRaises(ValueError):
            util.generate_namespace_id("sample*")
