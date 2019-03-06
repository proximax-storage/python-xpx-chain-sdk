import asyncio

from nem2 import util
from tests.harness import TestCase

LOOP = asyncio.get_event_loop()

@util.observable
async def foo():
    return 3


@util.observable(LOOP)
async def baz():
    return await foo()

async def bar():
    return await foo()


class TestObservableDecorator(TestCase):

    def test_asyncio(self):
        self.assertEqual(LOOP.run_until_complete(foo()), 3)
        self.assertEqual(LOOP.run_until_complete(baz()), 3)
        self.assertEqual(LOOP.run_until_complete(bar()), 3)

    def test_subscribe(self):
        src1 = foo()
        src2 = baz()
        try:
            import rx
            src1.subscribe(lambda x: None)
            src2.subscribe(lambda x: None)
        except ImportError:
            with self.assertRaises(AttributeError):
                src1.subscribe(lambda x: None)
            with self.assertRaises(AttributeError):
                src2.subscribe(lambda x: None)

        self.assertEqual(LOOP.run_until_complete(src1), 3)
        self.assertEqual(LOOP.run_until_complete(src2), 3)
