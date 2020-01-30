import sys

from xpxchain import util
from tests import harness

HAS_REACTIVE = 'rx' in sys.modules


@util.observable
async def foo():
    return 3


@util.observable
class Bar:
    def __await__(self):
        return foo().__await__()


@util.observable
async def gen():
    for i in range(5):
        yield i


@util.observable
class AsyncIter:
    def __init__(self):
        self.i = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.i == 5:
            raise StopAsyncIteration
        value = self.i
        self.i += 1
        return value


class TestObservableDecorator(harness.TestCase):

    async def test_coroutine(self):
        self.assertEqual(await foo(), 3)
        self.assertEqual(await Bar(), 3)

    async def test_coroutine_subscribe(self):
        src = foo()
        if HAS_REACTIVE:
            src = src.to_observable()
            src.subscribe(lambda x: None)
        self.assertEqual(await src, 3)

    async def test_async_generator(self):
        l = [i async for i in gen()]
        self.assertEqual(l, list(range(5)))
        if HAS_REACTIVE:
            l = [i async for i in gen().to_observable()]
            self.assertEqual(l, list(range(5)))

    async def test_async_iterator(self):
        l = [i async for i in AsyncIter()]
        self.assertEqual(l, list(range(5)))

    async def test_subscribe(self):
        l1 = []
        l2 = []
        src1 = gen()
        src2 = AsyncIter()

        if HAS_REACTIVE:
            obs1 = src1.to_observable()
            obs2 = src2.to_observable()
            obs1.subscribe(lambda x: l1.append(x))
            obs2.subscribe(lambda x: l2.append(x))
            await obs1
            await obs2
        else:
            l1 = [i async for i in src1]
            l2 = [i async for i in src2]

        self.assertEqual(l1, list(range(5)))
        self.assertEqual(l2, list(range(5)))
