from xpxchain import util
from tests import harness


def test_stdint(self, x: int, name: str):
    getattr(util, f'{name}_high')(x)
    getattr(util, f'{name}_low')(x)

    dto = getattr(util, f'{name}_to_dto')(x)
    self.assertEqual(getattr(util, f'{name}_from_dto')(dto), x)

    catbuffer = getattr(util, f'{name}_to_catbuffer')(x)
    self.assertEqual(getattr(util, f'{name}_from_catbuffer')(catbuffer), x)


def test_stdint_error(self, x: int, name: str):
    with self.assertRaises(ArithmeticError):
        getattr(util, f'{name}_high')(x)
    with self.assertRaises(ArithmeticError):
        getattr(util, f'{name}_low')(x)
    with self.assertRaises(ArithmeticError):
        dto = getattr(util, f'{name}_to_dto')(x)
        self.assertEqual(getattr(util, f'{name}_from_dto')(dto), x)
    with self.assertRaises(ArithmeticError):
        catbuffer = getattr(util, f'{name}_to_catbuffer')(x)
        self.assertEqual(getattr(util, f'{name}_from_catbuffer')(catbuffer), x)


class TestUnsignedInt(harness.TestCase):

    @harness.randomize
    def test_u8(self, x: harness.U8):
        test_stdint(self, x, 'u8')

    @harness.randomize(x={'min_value': -1 << 8, 'max_value': -1})
    def test_u8_underflow(self, x: int):
        test_stdint_error(self, x, 'u8')

    @harness.randomize(x={'min_value': 1 << 8, 'max_value': 1 << 9})
    def test_u8_overflow(self, x: int):
        test_stdint_error(self, x, 'u8')

    @harness.randomize
    def test_u16(self, x: harness.U16):
        test_stdint(self, x, 'u16')

    @harness.randomize(x={'min_value': -1 << 16, 'max_value': -1})
    def test_u16_underflow(self, x: int):
        test_stdint_error(self, x, 'u16')

    @harness.randomize(x={'min_value': 1 << 16, 'max_value': 1 << 17})
    def test_u16_overflow(self, x: int):
        test_stdint_error(self, x, 'u16')

    @harness.randomize
    def test_u32(self, x: harness.U32):
        test_stdint(self, x, 'u32')

    @harness.randomize(x={'min_value': -1 << 32, 'max_value': -1})
    def test_u32_underflow(self, x: int):
        test_stdint_error(self, x, 'u32')

    @harness.randomize(x={'min_value': 1 << 32, 'max_value': 1 << 33})
    def test_u32_overflow(self, x: int):
        test_stdint_error(self, x, 'u32')

    @harness.randomize
    def test_u64(self, x: harness.U64):
        test_stdint(self, x, 'u64')

    @harness.randomize(x={'min_value': -1 << 64, 'max_value': -1})
    def test_u64_underflow(self, x: int):
        test_stdint_error(self, x, 'u64')

    @harness.randomize(x={'min_value': 1 << 64, 'max_value': 1 << 65})
    def test_u64_overflow(self, x: int):
        test_stdint_error(self, x, 'u64')

    @harness.randomize
    def test_u128(self, x: harness.U128):
        test_stdint(self, x, 'u128')

    @harness.randomize(x={'min_value': -1 << 128, 'max_value': -1})
    def test_u128_underflow(self, x: int):
        test_stdint_error(self, x, 'u128')

    @harness.randomize(x={'min_value': 1 << 128, 'max_value': 1 << 129})
    def test_u128_overflow(self, x: int):
        test_stdint_error(self, x, 'u128')
