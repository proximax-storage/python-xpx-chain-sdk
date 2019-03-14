import copy
import typing

from nem2 import util
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

    def test_deepcopy(self):
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
