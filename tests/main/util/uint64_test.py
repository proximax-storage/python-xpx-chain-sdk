from nem2 import util
from tests.harness import TestCase


class TestUint64(TestCase):

    def test_uint64_to_dto(self):
        self.assertEqual(util.uint64_to_dto(0x0), [0, 0])
        self.assertEqual(util.uint64_to_dto(0x1), [1, 0])
        self.assertEqual(util.uint64_to_dto(0xFFFFFFFF), [0xFFFFFFFF, 0])
        self.assertEqual(util.uint64_to_dto(0x1FFFFFFFF), [0xFFFFFFFF, 0x1])

    def test_dto_to_uint64(self):
        self.assertEqual(util.dto_to_uint64([0, 0]), 0x0)
        self.assertEqual(util.dto_to_uint64([1, 0]), 0x1)
        self.assertEqual(util.dto_to_uint64([0xFFFFFFFF, 0]), 0xFFFFFFFF)
        self.assertEqual(util.dto_to_uint64([0xFFFFFFFF, 0x1]), 0x1FFFFFFFF)
