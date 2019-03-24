# Test our randomization test suite to ensure it is properly
# generating random data for our arguments.

from collections import deque
import enum
import math
import re
import string
import typing

from tests import harness


class Colors(enum.IntEnum):
    RED = 1 << 16
    GREEN = 1 << 8
    BLUE = 1


class TestRandomize(harness.TestCase):

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

    @harness.randomize
    def test_noargs_nokwds(self):
        pass

    @harness.randomize
    def test_enum(self, x: Colors):
        self.assertIsInstance(x, Colors)

    @harness.randomize
    def test_bool_nokwds(self, x: bool):
        self.assertIsInstance(x, bool)

    @harness.randomize
    def test_int_nokwds(self, x: int):
        self.assertIsInstance(x, int)

    @harness.randomize(x={'min_value': 5, 'max_value': 10})
    def test_int_range(self, x: int):
        self.assertIsInstance(x, int)
        self.assertGreaterEqual(x, 5)
        self.assertLessEqual(x, 10)

    @harness.randomize
    def test_u8(self, x: harness.U8):
        self.assertIsInstance(x, int)
        self.assertGreaterEqual(x, 0)
        self.assertLess(x, 1 << 8)

    @harness.randomize
    def test_u16(self, x: harness.U16):
        self.assertIsInstance(x, int)
        self.assertGreaterEqual(x, 0)
        self.assertLess(x, 1 << 16)

    @harness.randomize
    def test_u32(self, x: harness.U32):
        self.assertIsInstance(x, int)
        self.assertGreaterEqual(x, 0)
        self.assertLess(x, 1 << 32)

    @harness.randomize
    def test_u64(self, x: harness.U64):
        self.assertIsInstance(x, int)
        self.assertGreaterEqual(x, 0)
        self.assertLess(x, 1 << 64)

    @harness.randomize
    def test_u128(self, x: harness.U128):
        self.assertIsInstance(x, int)
        self.assertGreaterEqual(x, 0)
        self.assertLess(x, 1 << 128)

    @harness.randomize
    def test_i8(self, x: harness.I8):
        self.assertIsInstance(x, int)
        self.assertGreaterEqual(x, -(1 << 7))
        self.assertLess(x, 1 << 7)

    @harness.randomize
    def test_i16(self, x: harness.I16):
        self.assertIsInstance(x, int)
        self.assertGreaterEqual(x, -(1 << 15))
        self.assertLess(x, 1 << 15)

    @harness.randomize
    def test_i32(self, x: harness.I32):
        self.assertIsInstance(x, int)
        self.assertGreaterEqual(x, -(1 << 31))
        self.assertLess(x, 1 << 31)

    @harness.randomize
    def test_i64(self, x: harness.I64):
        self.assertIsInstance(x, int)
        self.assertGreaterEqual(x, -(1 << 63))
        self.assertLess(x, 1 << 63)

    @harness.randomize
    def test_i128(self, x: harness.I128):
        self.assertIsInstance(x, int)
        self.assertGreaterEqual(x, -(1 << 127))
        self.assertLess(x, 1 << 127)

    @harness.randomize
    def test_float_nokwds(self, x: float):
        self.assertIsInstance(x, float)

    @harness.randomize
    def test_f32(self, x: harness.F32):
        self.assertIsInstance(x, float)
        self.assertTrue(
            not math.isfinite(x)
            or x == 0.0
            or 1e-45 <= abs(x) <= 3.4028235e+38
        )

    @harness.randomize
    def test_f64(self, x: harness.F64):
        self.assertIsInstance(x, float)
        self.assertTrue(
            not math.isfinite(x)
            or x == 0.0
            or 5e-324 <= abs(x) <= 1.7976931348623157e+308
        )

    @harness.randomize
    def test_str_nokwds(self, x: str):
        self.assertIsInstance(x, str)

    @harness.randomize(x={'pattern': r'\w{5,10}'})
    def test_str_pattern(self, x: str):
        self.assertIsInstance(x, str)
        self.assertGreaterEqual(len(x), 5)
        self.assertLessEqual(len(x), 10)
        self.assertTrue(re.match(r'\w{5,10}', x))

    @harness.randomize(x={'letters': string.hexdigits})
    def test_str_letters(self, x: str):
        self.assertIsInstance(x, str)
        self.assertTrue(re.match(r'[A-Fa-f0-9]+', x))

    @harness.randomize(x={'min_length': 3, 'max_length': 4})
    def test_str_min_max_length(self, x: str):
        self.assertIsInstance(x, str)
        self.assertTrue(len(x) in (3, 4))

    @harness.randomize(x={'fixed_length': 10})
    def test_str_fixed_length(self, x: str):
        self.assertIsInstance(x, str)
        self.assertEqual(len(x), 10)

    @harness.randomize
    def test_bytes_nokwds(self, x: bytes):
        self.assertIsInstance(x, bytes)

    @harness.randomize(x={'letters': string.hexdigits.encode('ascii')})
    def test_bytes_letters(self, x: bytes):
        self.assertIsInstance(x, bytes)
        self.assertTrue(re.match(rb'[A-Fa-f0-9]+', x))

    @harness.randomize(x={'min_length': 3, 'max_length': 4})
    def test_bytes_min_max_length(self, x: bytes):
        self.assertIsInstance(x, bytes)
        self.assertTrue(len(x) in (3, 4))

    @harness.randomize(x={'fixed_length': 10})
    def test_bytes_fixed_length(self, x: bytes):
        self.assertIsInstance(x, bytes)
        self.assertEqual(len(x), 10)

    @harness.randomize
    def test_list_nokwds(self, x: typing.List[int]):
        self.assertIsInstance(x, list)
        for xi in x:
            self.assertIsInstance(xi, int)

    @harness.randomize(x={'value_type': int})
    def test_list_value_type(self, x: list):
        self.assertIsInstance(x, list)
        for xi in x:
            self.assertIsInstance(xi, int)

    @harness.randomize(x={'value': {'min_value': 5, 'max_value': 10}})
    def test_list_args(self, x: typing.List[int]):
        self.assertIsInstance(x, list)
        for xi in x:
            self.assertIsInstance(xi, int)
            self.assertGreaterEqual(xi, 5)
            self.assertLessEqual(xi, 10)

    @harness.randomize
    def test_set_nokwds(self, x: typing.Set[int]):
        self.assertIsInstance(x, set)
        for xi in x:
            self.assertIsInstance(xi, int)

    @harness.randomize
    def test_frozenset_kwds(self, x: typing.FrozenSet[int]):
        self.assertIsInstance(x, frozenset)
        for xi in x:
            self.assertIsInstance(xi, int)

    @harness.randomize
    def test_deque_nokwds(self, x: typing.Deque[int]):
        self.assertIsInstance(x, deque)
        for xi in x:
            self.assertIsInstance(xi, int)

    @harness.randomize
    def test_dict_nokwds(self, x: typing.Dict[str, int]):
        self.assertIsInstance(x, dict)
        for ki, vi in x.items():
            self.assertIsInstance(ki, str)
            self.assertIsInstance(vi, int)

    @harness.randomize(x={
        'key': {'fixed_length': 0},
        'value': {'min_value': 0, 'max_value': 0},
    })
    def test_dict_kwds(self, x: typing.Dict[str, int]):
        self.assertIsInstance(x, dict)
        for ki, vi in x.items():
            self.assertEqual(ki, '')
            self.assertEqual(vi, 0)


class TestRandomizeForwardRef(harness.TestCase):

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

    @harness.randomize
    def test_noargs_nokwds(self):
        pass

    @harness.randomize
    def test_enum(self, x: 'Colors'):
        self.assertIsInstance(x, Colors)

    @harness.randomize
    def test_bool_nokwds(self, x: 'bool'):
        self.assertIsInstance(x, bool)

    @harness.randomize
    def test_int_nokwds(self, x: 'int'):
        self.assertIsInstance(x, int)

    @harness.randomize
    def test_float_nokwds(self, x: 'float'):
        self.assertIsInstance(x, float)

    @harness.randomize
    def test_str_nokwds(self, x: 'str'):
        self.assertIsInstance(x, str)

    @harness.randomize
    def test_bytes_nokwds(self, x: 'bytes'):
        self.assertIsInstance(x, bytes)

    @harness.randomize
    def test_list_nokwds(self, x: 'typing.List[int]'):
        self.assertIsInstance(x, list)
        for xi in x:
            self.assertIsInstance(xi, int)


class TestInvalidRandomize(harness.TestCase):

    def test_invalid_list(self):
        with self.assertRaises(TypeError):
            @harness.randomize
            def test(self, x: list):
                pass

    def test_invalid_set(self):
        with self.assertRaises(TypeError):
            @harness.randomize
            def test(self, x: set):
                pass

    def test_invalid_frozenset(self):
        with self.assertRaises(TypeError):
            @harness.randomize
            def test(self, x: frozenset):
                pass

    def test_invalid_deque(self):
        with self.assertRaises(TypeError):
            @harness.randomize
            def test(self, x: deque):
                pass

    def test_invalid_dict(self):
        with self.assertRaises(TypeError):
            @harness.randomize
            def test(self, x: dict):
                pass


class TestInvalidRandomizeFutureRef(harness.TestCase):

    def test_invalid_list(self):
        with self.assertRaises(TypeError):
            @harness.randomize
            def test(self, x: 'list'):
                pass

    def test_invalid_set(self):
        with self.assertRaises(TypeError):
            @harness.randomize
            def test(self, x: 'set'):
                pass

    def test_invalid_frozenset(self):
        with self.assertRaises(TypeError):
            @harness.randomize
            def test(self, x: 'frozenset'):
                pass

    def test_invalid_deque(self):
        with self.assertRaises(TypeError):
            @harness.randomize
            def test(self, x: 'deque'):
                pass

    def test_invalid_dict(self):
        with self.assertRaises(TypeError):
            @harness.randomize
            def test(self, x: 'dict'):
                pass
