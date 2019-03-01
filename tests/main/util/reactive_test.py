import asyncio

from nem2.util.reactive import observable
from tests.harness import TestCase

LOOP = asyncio.get_event_loop()

@observable
async def foo():
    return 3

async def bar():
    return await foo()


class TestObservableDecorator(TestCase):

    def test_asyncio(self):
        self.assertEqual(LOOP.run_until_complete(foo()), 3)
        self.assertEqual(LOOP.run_until_complete(bar()), 3)

    def test_subscribe(self):
        source = foo()
        try:
            import rx
            source.subscribe(lambda x: None)
        except ImportError:
            with self.assertRaises(AttributeError):
                source.subscribe(lambda x: None)

        self.assertEqual(LOOP.run_until_complete(foo()), 3)
