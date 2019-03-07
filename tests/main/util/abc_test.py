import abc
import enum

from nem2 import util
from tests import harness


class Base(abc.ABC):

    memo = {}

    @property
    def baz(self):
        return 1

    @property
    @abc.abstractmethod
    def foo(self):
        return 1

    @abc.abstractmethod
    def bar(self):
        return self.foo


class DerivedEnum(Base, enum.IntEnum, metaclass=util.ABCEnumMeta):
    SUCCESS = 0
    FAILURE = 1

    @property
    def foo(self):
        return super().foo

    def bar(self):
        return super().bar()


class TestABCEnumMeta(harness.TestCase):

    def test_derived(self):
        self.assertEqual(DerivedEnum.SUCCESS, 0)
        self.assertEqual(DerivedEnum.FAILURE, 1)
        self.assertEqual(DerivedEnum.FAILURE.foo, 1)
        self.assertEqual(DerivedEnum.FAILURE.bar(), 1)
        self.assertIs(DerivedEnum.memo, Base.memo)

        self.assertTrue(issubclass(DerivedEnum, Base))
        self.assertTrue(issubclass(DerivedEnum, enum.IntEnum))

        base = enum.IntEnum
        bases = (Base, enum.IntEnum,)
        mro = [DerivedEnum, Base, abc.ABC, enum.IntEnum, int, enum.Enum, object]
        self.assertEqual(DerivedEnum.mro(), mro)
        self.assertEqual(DerivedEnum.__base__, base)
        self.assertEqual(DerivedEnum.__bases__, bases)

    def test_partial_derive(self):
        with self.assertRaises(TypeError):
            class PartiallyDerivedEnum(Base, enum.IntEnum, metaclass=util.ABCEnumMeta):
                SUCCESS = 0

