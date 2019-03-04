from nem2 import util
from tests.harness import TestCase


class TestUint64(TestCase):

    def test_uint64_low(self):
        self.assertEqual(util.uint64_low(0x0), 0x0)
        self.assertEqual(util.uint64_low(0x1), 0x1)
        self.assertEqual(util.uint64_low(0xFFFFFFFF), 0xFFFFFFFF)
        self.assertEqual(util.uint64_low(0x1FFFFFFFF), 0xFFFFFFFF)

    def test_uint64_high(self):
        self.assertEqual(util.uint64_high(0x0), 0x0)
        self.assertEqual(util.uint64_high(0x1), 0x0)
        self.assertEqual(util.uint64_high(0xFFFFFFFF), 0x0)
        self.assertEqual(util.uint64_high(0x1FFFFFFFF), 0x1)

    def test_uint64_to_dto(self):
        self.assertEqual(util.uint64_to_dto(0x0), [0x0, 0x0])
        self.assertEqual(util.uint64_to_dto(0x1), [0x1, 0x0])
        self.assertEqual(util.uint64_to_dto(0xFFFFFFFF), [0xFFFFFFFF, 0x0])
        self.assertEqual(util.uint64_to_dto(0x1FFFFFFFF), [0xFFFFFFFF, 0x1])

    def test_dto_to_uint64(self):
        self.assertEqual(util.dto_to_uint64([0x0, 0x0]), 0x0)
        self.assertEqual(util.dto_to_uint64([0x1, 0x0]), 0x1)
        self.assertEqual(util.dto_to_uint64([0xFFFFFFFF, 0x0]), 0xFFFFFFFF)
        self.assertEqual(util.dto_to_uint64([0xFFFFFFFF, 0x1]), 0x1FFFFFFFF)

    def test_uint128_low(self):
        self.assertEqual(util.uint128_low(0x0), 0x0)
        self.assertEqual(util.uint128_low(0x1), 0x1)
        self.assertEqual(util.uint128_low(0xFFFFFFFFFFFFFFFF), 0xFFFFFFFFFFFFFFFF)
        self.assertEqual(util.uint128_low(0x1FFFFFFFFFFFFFFFF), 0xFFFFFFFFFFFFFFFF)

    def test_uint128_high(self):
        self.assertEqual(util.uint128_high(0x0), 0x0)
        self.assertEqual(util.uint128_high(0x1), 0x0)
        self.assertEqual(util.uint128_high(0xFFFFFFFFFFFFFFFF), 0x0)
        self.assertEqual(util.uint128_high(0x1FFFFFFFFFFFFFFFF), 0x1)

    def test_uint128_to_dto(self):
        self.assertEqual(util.uint128_to_dto(0x0), [[0x0, 0x0], [0x0, 0x0]])
        self.assertEqual(util.uint128_to_dto(0x1), [[0x1, 0x0], [0x0, 0x0]])
        self.assertEqual(util.uint128_to_dto(0xFFFFFFFFFFFFFFFF), [[0xFFFFFFFF, 0xFFFFFFFF], [0x0, 0x0]])
        self.assertEqual(util.uint128_to_dto(0x1FFFFFFFFFFFFFFFF), [[0xFFFFFFFF, 0xFFFFFFFF], [0x1, 0x0]])

    def test_dto_to_uint128(self):
        self.assertEqual(util.dto_to_uint128([[0x0, 0x0], [0x0, 0x0]]), 0x0)
        self.assertEqual(util.dto_to_uint128([[0x1, 0x0], [0x0, 0x0]]), 0x1)
        self.assertEqual(util.dto_to_uint128([[0xFFFFFFFF, 0xFFFFFFFF], [0x0, 0x0]]), 0xFFFFFFFFFFFFFFFF)
        self.assertEqual(util.dto_to_uint128([[0xFFFFFFFF, 0xFFFFFFFF], [0x1, 0x0]]), 0x1FFFFFFFFFFFFFFFF)
