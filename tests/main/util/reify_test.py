from nem2 import util
from tests import harness


class Obj:

    def __init__(self):
        self._counter = 0

    def increment(self) -> int:
        self._counter += 1
        return self._counter

    def reset(self):
        self._counter = 0

    @property
    def value(self) -> int:
        if self._counter != 0:
            raise TypeError("...")
        return self.increment()


class ReifiedObj:

    def __init__(self):
        self._counter = 0

    def increment(self) -> int:
        self._counter += 1
        return self._counter

    def reset(self):
        self._counter = 0

    @util.reify
    def value(self) -> int:
        if self._counter != 0:
            raise TypeError("...")
        return self.increment()


class TestReify(harness.TestCase):

    def test_property(self):
        obj = Obj()
        self.assertEqual(obj.value, 1)
        with self.assertRaises(TypeError):
            obj.value

    def test_reify(self):
        obj = ReifiedObj()
        self.assertEqual(obj.value, 1)
        self.assertEqual(obj.value, 1)

    def test_data_descriptor(self):
        obj = ReifiedObj()
        self.assertEqual(obj.value, 1)
        with self.assertRaises(TypeError):
            obj.value = 1
        with self.assertRaises(TypeError):
            del obj.value

        fget1 = lambda x: print('getter')
        r1 = util.reify(fget1)
        self.assertEqual(r1.fget, fget1)
        self.assertEqual(r1.fset, None)
        self.assertEqual(r1.fdel, None)

        fget2 = lambda x: print('getter')
        r2 = r1.getter(fget2)
        self.assertNotEqual(r1, r2)
        self.assertNotEqual(r2.fget, fget1)
        self.assertEqual(r2.fget, fget2)
        self.assertEqual(r2.fset, None)
        self.assertEqual(r2.fdel, None)

        with self.assertRaises(TypeError):
            r2.setter(lambda x: print('setter'))
        with self.assertRaises(TypeError):
            r2.deleter(lambda x: print('deleter'))
