import datetime
import random

from nem2 import util
from nem2 import models
from tests import harness


def psuedo_entropy(size: int) -> bytes:
    return bytes([random.randint(0, 255) for _ in range(size)])


class TestDeadline(harness.TestCase):

    def setUp(self):
        self.datetime = datetime.datetime(2019, 3, 8, 0, 18, 57)
        self.dto = [1552004337, 0]

    def test_create(self):
        pass

    def test_to_dto(self):
        value = models.Deadline(self.datetime)
        self.assertEqual(value.to_dto(), self.dto)
        self.assertEqual(value.toDto(), value.to_dto())

    def test_from_dto(self):
        value = models.Deadline.from_dto(self.dto)
        self.assertEqual(value.deadline, self.datetime)
        self.assertEqual(value, models.Deadline.fromDto(self.dto))


class TestHashType(harness.TestCase):

    def setUp(self):
        self.digest_64 = (
            models.HashType.SHA3_256,
            models.HashType.KECCAK_256,
            models.HashType.HASH_256
        )
        self.digest_40 = (models.HashType.HASH_160,)

    def test_validate(self):
        hash_40 = util.hexlify(psuedo_entropy(20))
        hash_64 = util.hexlify(psuedo_entropy(32))

        for enum in self.digest_64:
            self.assertFalse(enum.validate(hash_40))
            self.assertTrue(enum.validate(hash_64))

        for enum in self.digest_40:
            self.assertTrue(enum.validate(hash_40))
            self.assertFalse(enum.validate(hash_64))

        hash_40 = hash_40[:-1] + 'x'
        hash_64 = hash_64[:-1] + 'x'

        for enum in self.digest_64:
            self.assertFalse(enum.validate(hash_40))
            self.assertFalse(enum.validate(hash_64))

        for enum in self.digest_40:
            self.assertFalse(enum.validate(hash_40))
            self.assertFalse(enum.validate(hash_64))
