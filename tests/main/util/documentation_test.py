from nem2 import util
from tests import harness

@util.doc("""Function doc string.""")
def docfunc1():
    return 1


docfunc2 = util.doc("""Function doc string.""")(docfunc1)
undocfunc1 = util.undoc(docfunc1)

@util.undoc
def undocfunc2():
    """Function doc string (never appears)."""

    return 1


class MyClass:
    """Dummy class to test wrapping individual components."""

    # PROPERTY

    @util.doc("""Property doc string.""")
    @property
    def docprop1(self):
        return 1

    docprop2 = util.doc("""Property doc string.""")(docprop1)
    undocprop1 = util.undoc(docprop1)

    @util.undoc
    @property
    def undocprop2(self):
        """Property doc string (never appears)."""
        return 1

    # REIFIED PROPERTIES

    @util.doc("""Reified property doc string.""")
    @util.reify
    def docrei1(self):
        return 1

    docrei2 = util.doc("""Reified property doc string.""")(docrei1)
    undocrei1 = util.undoc(docrei1)

    @util.undoc
    @util.reify
    def undocrei2(self):
        """Reified property doc string (never appears)."""
        return 1

    # METHOD

    @util.doc("""Method doc string.""")
    def docmeth1(self):
        return 1

    docmeth2 = util.doc("""Method doc string.""")(docmeth1)
    undocmeth1 = util.undoc(docmeth1)

    @util.undoc
    def undocmeth2(self):
        """Method doc string (never appears)."""
        return 1

    # CLASSMETHOD

    @util.doc("""Classmethod doc string.""")
    @classmethod
    def docclsmeth1(cls):
        return 1

    docclsmeth2 = util.doc("""Classmethod doc string.""")(docclsmeth1)
    undocclsmeth1 = util.undoc(docclsmeth1)

    @util.undoc
    @classmethod
    def undocclsmeth2(cls):
        """Classmethod doc string (never appears)."""
        return 1

    # STATICMETHOD

    @util.doc("""Staticmethod doc string.""")
    @staticmethod
    def docstaticmeth1():
        return 1

    docstaticmeth2 = util.doc("""Staticmethod doc string.""")(docstaticmeth1)
    undocstaticmeth1 = util.undoc(docstaticmeth1)

    @util.undoc
    @staticmethod
    def undocstaticmeth2():
        """Staticmethod doc string (never appears)."""
        return 1


class TestDocumentation(harness.TestCase):

    def test_function(self):
        self.assertTrue(docfunc1.__doc__ is not None)
        self.assertEqual(docfunc1.__doc__, docfunc2.__doc__)
        self.assertTrue(undocfunc1.__doc__ is None)
        self.assertTrue(undocfunc2.__doc__ is None)

        self.assertEqual(docfunc1(), 1)
        self.assertEqual(docfunc2(), 1)
        self.assertEqual(undocfunc1(), 1)
        self.assertEqual(undocfunc2(), 1)

    def test_property(self):
        self.assertTrue(MyClass.docprop1.__doc__ is not None)
        self.assertEqual(MyClass.docprop1.__doc__, MyClass.docprop2.__doc__)
        self.assertTrue(MyClass.undocprop1.__doc__ is None)
        self.assertTrue(MyClass.undocprop2.__doc__ is None)

        inst = MyClass()
        self.assertEqual(inst.docprop1, 1)
        self.assertEqual(inst.docprop2, 1)
        self.assertEqual(inst.undocprop1, 1)
        self.assertEqual(inst.undocprop2, 1)

    def test_reify(self):
        self.assertTrue(MyClass.docrei1.__doc__ is not None)
        self.assertEqual(MyClass.docrei1.__doc__, MyClass.docrei2.__doc__)
        self.assertTrue(MyClass.undocrei1.__doc__ is None)
        self.assertTrue(MyClass.undocrei2.__doc__ is None)

        inst = MyClass()
        self.assertEqual(inst.docrei1, 1)
        self.assertEqual(inst.docrei2, 1)
        self.assertEqual(inst.undocrei1, 1)
        self.assertEqual(inst.undocrei2, 1)

    def test_method(self):
        inst = MyClass()
        self.assertTrue(inst.docmeth1.__doc__ is not None)
        self.assertEqual(inst.docmeth1.__doc__, inst.docmeth2.__doc__)
        self.assertTrue(inst.undocmeth1.__doc__ is None)
        self.assertTrue(inst.undocmeth2.__doc__ is None)

        self.assertEqual(inst.docmeth1(), 1)
        self.assertEqual(inst.docmeth2(), 1)
        self.assertEqual(inst.undocmeth1(), 1)
        self.assertEqual(inst.undocmeth2(), 1)

    def test_classmethod(self):
        self.assertTrue(MyClass.docclsmeth1.__doc__ is not None)
        self.assertEqual(MyClass.docclsmeth1.__doc__, MyClass.docclsmeth2.__doc__)
        self.assertTrue(MyClass.undocclsmeth1.__doc__ is None)
        self.assertTrue(MyClass.undocclsmeth2.__doc__ is None)

        self.assertEqual(MyClass.docclsmeth1(), 1)
        self.assertEqual(MyClass.docclsmeth2(), 1)
        self.assertEqual(MyClass.undocclsmeth1(), 1)
        self.assertEqual(MyClass.undocclsmeth2(), 1)

    def test_staticmethod(self):
        self.assertTrue(MyClass.docstaticmeth1.__doc__ is not None)
        self.assertEqual(MyClass.docstaticmeth1.__doc__, MyClass.docstaticmeth2.__doc__)
        self.assertTrue(MyClass.undocstaticmeth1.__doc__ is None)
        self.assertTrue(MyClass.undocstaticmeth2.__doc__ is None)

        self.assertEqual(MyClass.docstaticmeth1(), 1)
        self.assertEqual(MyClass.docstaticmeth2(), 1)
        self.assertEqual(MyClass.undocstaticmeth1(), 1)
        self.assertEqual(MyClass.undocstaticmeth2(), 1)
