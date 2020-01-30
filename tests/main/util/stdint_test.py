from xpxchain import util
from tests import harness


def run_test(case, name, items):
    get = lambda name: getattr(util, name)
    for value, low, high, cat, dto in items:
        case.assertEqual(get(f'{name}_low')(value), low)
        case.assertEqual(get(f'{name}_high')(value), high)
        case.assertEqual(get(f'{name}_from_catbuffer')(cat), value)
        case.assertEqual(get(f'{name}_from_dto')(dto), value)
        case.assertEqual(get(f'{name}_to_catbuffer')(value), cat)
        case.assertEqual(get(f'{name}_to_dto')(value), dto)
        case.assertEqual(next(get(f'{name}_iter_from_catbuffer')(cat)), value)
        case.assertEqual(next(get(f'{name}_iter_from_dto')([dto])), value)
        case.assertEqual(next(get(f'{name}_iter_to_catbuffer')([value])), cat)
        case.assertEqual(next(get(f'{name}_iter_to_dto')([value])), dto)


class TestUnsignedInt(harness.TestCase):

    def test_exceptions(self):
        with self.assertRaises(OverflowError):
            util.u8_high(1 << 8)
        with self.assertRaises(OverflowError):
            util.u8_low(1 << 8)
        with self.assertRaises(OverflowError):
            util.u8_from_catbuffer(b'\x00\x00')
        with self.assertRaises(ValueError):
            next(util.u16_iter_from_catbuffer(b'\x00'))
        with self.assertRaises(OverflowError):
            util.u8_to_dto(1 << 8)
        with self.assertRaises(OverflowError):
            util.u8_from_dto(1 << 8)
        with self.assertRaises(OverflowError):
            util.u16_to_dto(1 << 16)
        with self.assertRaises(OverflowError):
            util.u16_from_dto(1 << 16)
        with self.assertRaises(OverflowError):
            util.u32_to_dto(1 << 32)
        with self.assertRaises(OverflowError):
            util.u32_from_dto(1 << 32)
        with self.assertRaises(OverflowError):
            util.u64_to_dto(1 << 64)
        with self.assertRaises(ArithmeticError):
            util.u64_from_dto([1 << 32, 0])
        with self.assertRaises(ArithmeticError):
            util.u64_from_dto([0, 1 << 32])
        with self.assertRaises(ArithmeticError):
            util.u64_from_dto([0])
        with self.assertRaises(ArithmeticError):
            util.u64_from_dto([0, 0, 0])
        with self.assertRaises(OverflowError):
            util.u128_to_dto(1 << 128)
        with self.assertRaises(ArithmeticError):
            util.u128_from_dto([[1 << 32, 0]])

    def test_u8(self):
        run_test(
            case=self,
            name='u8',
            items=[
                (0x00, 0x0, 0x0, b'\x00', 0x00),
                (0x01, 0x1, 0x0, b'\x01', 0x01),
                (0x0F, 0xF, 0x0, b'\x0F', 0x0F),
                (0x1F, 0xF, 0x1, b'\x1F', 0x1F),
            ],
        )

    def test_u16(self):
        run_test(
            case=self,
            name='u16',
            items=[
                (0x0000, 0x00, 0x00, b'\x00\x00', 0x0000),
                (0x0001, 0x01, 0x00, b'\x01\x00', 0x0001),
                (0x00FF, 0xFF, 0x00, b'\xFF\x00', 0x00FF),
                (0x01FF, 0xFF, 0x01, b'\xFF\x01', 0x01FF),
            ],
        )

    def test_u32(self):
        run_test(
            case=self,
            name='u32',
            items=[
                (0x00000000, 0x0000, 0x0000, b'\x00\x00\x00\x00', 0x00000000),
                (0x00000001, 0x0001, 0x0000, b'\x01\x00\x00\x00', 0x00000001),
                (0x0000FFFF, 0xFFFF, 0x0000, b'\xFF\xFF\x00\x00', 0x0000FFFF),
                (0x0001FFFF, 0xFFFF, 0x0001, b'\xFF\xFF\x01\x00', 0x0001FFFF),
            ],
        )

    def test_u64(self):
        run_test(
            case=self,
            name='u64',
            items=[
                (0x0000000000000000, 0x00000000, 0x00000000, b'\x00\x00\x00\x00\x00\x00\x00\x00', [0x00000000, 0x00000000]),
                (0x0000000000000001, 0x00000001, 0x00000000, b'\x01\x00\x00\x00\x00\x00\x00\x00', [0x00000001, 0x00000000]),
                (0x00000000FFFFFFFF, 0xFFFFFFFF, 0x00000000, b'\xFF\xFF\xFF\xFF\x00\x00\x00\x00', [0xFFFFFFFF, 0x00000000]),
                (0x00000001FFFFFFFF, 0xFFFFFFFF, 0x00000001, b'\xFF\xFF\xFF\xFF\x01\x00\x00\x00', [0xFFFFFFFF, 0x00000001]),
            ],
        )

    def test_u128(self):
        run_test(
            case=self,
            name='u128',
            items=[
                (0x00000000000000000000000000000000, 0x0000000000000000, 0x0000000000000000, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', [[0x00000000, 0x00000000], [0x00000000, 0x00000000]]),
                (0x00000000000000000000000000000001, 0x0000000000000001, 0x0000000000000000, b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', [[0x00000001, 0x00000000], [0x00000000, 0x00000000]]),
                (0x0000000000000000FFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0x0000000000000000, b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00', [[0xFFFFFFFF, 0xFFFFFFFF], [0x00000000, 0x00000000]]),
                (0x0000000000000001FFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF, 0x0000000000000001, b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x01\x00\x00\x00\x00\x00\x00\x00', [[0xFFFFFFFF, 0xFFFFFFFF], [0x00000001, 0x00000000]]),
            ],
        )
