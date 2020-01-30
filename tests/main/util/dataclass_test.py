import copy
import typing

from xpxchain import util
from tests import harness

T = typing.TypeVar('T')


@util.dataclass(frozen=True, prev=None, next=None)
class LinkedList:
    value: T
    prev: typing.Optional['LinkedList']
    next: typing.Optional['LinkedList']

    def __next__(self):
        if self.next is None:
            raise StopIteration
        return self.next


class TestDataclass(harness.TestCase):

    def test_init(self):
        ll = LinkedList(5)
        self.assertEqual(ll.value, 5)
        self.assertEqual(ll.prev, None)
        self.assertEqual(ll.next, None)

    def test_frozen(self):
        ll = LinkedList(5)
        with self.assertRaises(util.FrozenInstanceError):
            ll.value = 6

    def test_slots(self):
        ll = LinkedList(5)
        with self.assertRaises(TypeError):
            ll.__dict__

    def test_copy(self):
        ll = LinkedList(5)
        self.assertEqual(ll, copy.copy(ll))

    def test_deepcopy(self):
        ll = LinkedList(5)
        self.assertEqual(ll, copy.deepcopy(ll))

    def test_asdict(self):
        ll = LinkedList(5)
        self.assertEqual(ll.asdict(), {'value': 5, 'prev': None, 'next': None})

    def test_astuple(self):
        ll = LinkedList(5)
        self.assertEqual(ll.astuple(), (5, None, None))

    def test_fields(self):
        ll = LinkedList(5)
        fields = ll.fields()
        self.assertEqual([i.name for i in fields], ['value', 'prev', 'next'])

    def test_replace(self):
        ll = LinkedList(5)
        self.assertEqual(ll.replace(value=10), LinkedList(10, ll.prev, ll.next))

    def test_str(self):
        ll = LinkedList(5)
        self.assertEqual(str(ll), 'LinkedList(value=5, prev=None, next=None)')

    def test_eq(self):
        ll1 = LinkedList(5)
        ll2 = LinkedList(5)
        ll3 = LinkedList(10)

        self.assertTrue(ll1 == ll1)
        self.assertTrue(ll1 == ll2)
        self.assertFalse(ll1 == ll3)
        self.assertTrue(ll2 == ll2)
        self.assertFalse(ll2 == ll3)
        self.assertTrue(ll3 == ll3)


class TestDataclassErrors(harness.TestCase):

    def test_noargs(self):
        @util.dataclass
        class Dataclass:
            first: int
            second: int

        self.assertTrue(util.is_dataclass(Dataclass))

    def test_defaults(self):
        with self.assertRaises(SyntaxError):
            @util.dataclass(frozen=True, first=0)
            class Dataclass1:
                first: int
                second: int

        with self.assertRaises(SyntaxError):
            @util.dataclass(second=0)
            class Dataclass2:
                first: int
                second: int

                def __init__(self, first=0, second=0):
                    pass

    def test_slots(self):
        @util.dataclass(slots=False)
        class Dataclass:
            first: int
            second: int = 2

        self.assertTrue(not hasattr(Dataclass, '__slots__'))
        dataclass = Dataclass(1)
        dataclass.third = 3

    def test_copy(self):
        @util.dataclass(copy=False, deepcopy=False)
        class Dataclass:
            first: int

        self.assertTrue(not hasattr(Dataclass, '__copy__'))
        self.assertTrue(not hasattr(Dataclass, '__deepcopy__'))

    def test_dataclass_methods(self):
        @util.dataclass(asdict=False, astuple=False, fields=False, replace=False)
        class Dataclass:
            first: int

        self.assertTrue(not hasattr(Dataclass, 'asdict'))
        self.assertTrue(not hasattr(Dataclass, 'astuple'))
        self.assertTrue(not hasattr(Dataclass, 'fields'))
        self.assertTrue(not hasattr(Dataclass, 'replace'))
