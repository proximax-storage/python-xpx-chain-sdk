import functools

from nem2 import util
from tests import harness


def create():

    class A:
        def __init__(self):
            pass

        def __int__(self):
            return 3

    class B:
        def __init__(self):
            pass

        @staticmethod
        def c():
            return 1

        def d(self):
            return 2

        @classmethod
        def e(cls):
            return 3

        @property
        def f(self):
            return 4

        @f.setter
        def f(self, value):
            pass

        @f.deleter
        def f(self):
            pass

        @util.reify
        def g(self):
            return 5

    def c():
        return 5

    def decorate(f):
        @functools.wraps(f)
        def wrapper():
            return f()
        return wrapper

    @decorate
    def d():
        return 6

    return A, B, c, d


A1, B1, c1, d1 = create()
A2, B2, c2, d2 = map(util.defactorize, create())


class DefactorizeTest(harness.TestCase):

    def test_empty_class(self):
        self.assertEqual(A1.__qualname__, 'create.<locals>.A')
        self.assertEqual(A2.__qualname__, 'A')

        self.assertEqual(A1.__init__.__qualname__, 'create.<locals>.A.__init__')
        self.assertEqual(A2.__init__.__qualname__, 'A.__init__')

        self.assertEqual(A1.__int__.__qualname__, 'create.<locals>.A.__int__')
        self.assertEqual(A2.__int__.__qualname__, 'create.<locals>.A.__int__')

    def test_class(self):
        self.assertEqual(B1.__qualname__, 'create.<locals>.B')
        self.assertEqual(B2.__qualname__, 'B')

        self.assertEqual(B1.__init__.__qualname__, 'create.<locals>.B.__init__')
        self.assertEqual(B2.__init__.__qualname__, 'B.__init__')

    def test_staticmethod(self):
        self.assertEqual(B1.c.__qualname__, 'create.<locals>.B.c')
        self.assertEqual(B2.c.__qualname__, 'B.c')

    def test_classmethod(self):
        self.assertEqual(B1.e.__qualname__, 'create.<locals>.B.e')
        self.assertEqual(B2.e.__qualname__, 'B.e')

    def test_method(self):
        self.assertEqual(B1.d.__qualname__, 'create.<locals>.B.d')
        self.assertEqual(B2.d.__qualname__, 'B.d')

    def test_property(self):
        self.assertEqual(B1.f.fget.__qualname__, 'create.<locals>.B.f')
        self.assertEqual(B2.f.fget.__qualname__, 'B.f')

        self.assertEqual(B1.f.fset.__qualname__, 'create.<locals>.B.f')
        self.assertEqual(B2.f.fset.__qualname__, 'B.f')

        self.assertEqual(B1.f.fdel.__qualname__, 'create.<locals>.B.f')
        self.assertEqual(B2.f.fdel.__qualname__, 'B.f')

    def test_reify(self):
        self.assertEqual(B1.g.fget.__qualname__, 'create.<locals>.B.g')
        self.assertEqual(B2.g.fget.__qualname__, 'B.g')

    def test_function(self):
        self.assertEqual(c1.__qualname__, 'create.<locals>.c')
        self.assertEqual(c2.__qualname__, 'c')

    def test_decorator(self):
        self.assertEqual(d1.__qualname__, 'create.<locals>.d')
        self.assertEqual(d2.__qualname__, 'd')

        self.assertEqual(d1.__wrapped__.__qualname__, 'create.<locals>.d')
        self.assertEqual(d2.__wrapped__.__qualname__, 'd')
