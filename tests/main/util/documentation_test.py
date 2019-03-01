from nem2.util import documentation
from tests.harness import TestCase

def docfunc():
    """Function doc string."""

    return 1


undocfunc1 = documentation.undoc(docfunc)

@documentation.undoc
def undocfunc2():
    """Function doc string (never appears)."""

    return 1


class MyClass:
    """Dummy class to test wrapping individual components."""

    # PROPERTY

    @property
    def docprop(self):
        """Property doc string."""
        return 1

    undocprop1 = documentation.undoc(docprop)

    @documentation.undoc
    @property
    def undocprop2(self):
        """Property doc string (never appears)."""
        return 1

    # METHOD

    def docmeth(self):
        """Method doc string."""
        return 1

    undocmeth1 = documentation.undoc(docmeth)

    @documentation.undoc
    def undocmeth2(self):
        """Method doc string (never appears)."""
        return 1

    # CLASSMETHOD

    @classmethod
    def docclsmeth(cls):
        """Classmethod doc string."""
        return 1

    undocclsmeth1 = documentation.undoc(docclsmeth)

    @documentation.undoc
    @classmethod
    def undocclsmeth2(cls):
        """Classmethod doc string (never appears)."""
        return 1

    # STATICMETHOD

    @staticmethod
    def docstaticmeth():
        """Staticmethod doc string."""
        return 1

    undocstaticmeth1 = documentation.undoc(docstaticmeth)

    @documentation.undoc
    @staticmethod
    def undocstaticmeth2():
        """Staticmethod doc string (never appears)."""
        return 1



class TestDocHidden(TestCase):

    def test_function(self):
        self.assertTrue(docfunc.__doc__ is not None)
        self.assertTrue(undocfunc1.__doc__ is None)
        self.assertTrue(undocfunc2.__doc__ is None)

        self.assertEqual(docfunc(), 1)
        self.assertEqual(undocfunc1(), 1)
        self.assertEqual(undocfunc2(), 1)

    def test_property(self):
        self.assertTrue(MyClass.docprop.__doc__ is not None)
        self.assertTrue(MyClass.undocprop1.__doc__ is None)
        self.assertTrue(MyClass.undocprop2.__doc__ is None)

        inst = MyClass()
        self.assertEqual(inst.docprop, 1)
        self.assertEqual(inst.undocprop1, 1)
        self.assertEqual(inst.undocprop2, 1)

    def test_method(self):
        inst = MyClass()
        self.assertTrue(inst.docmeth.__doc__ is not None)
        self.assertTrue(inst.undocmeth1.__doc__ is None)
        self.assertTrue(inst.undocmeth2.__doc__ is None)

        self.assertEqual(inst.docmeth(), 1)
        self.assertEqual(inst.undocmeth1(), 1)
        self.assertEqual(inst.undocmeth2(), 1)

    def test_classmethod(self):
        self.assertTrue(MyClass.docclsmeth.__doc__ is not None)
        self.assertTrue(MyClass.undocclsmeth1.__doc__ is None)
        self.assertTrue(MyClass.undocclsmeth2.__doc__ is None)

        self.assertEqual(MyClass.docclsmeth(), 1)
        self.assertEqual(MyClass.undocclsmeth1(), 1)
        self.assertEqual(MyClass.undocclsmeth2(), 1)

    def test_staticmethod(self):
        pass
