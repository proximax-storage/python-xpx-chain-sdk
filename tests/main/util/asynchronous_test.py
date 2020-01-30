import asyncio

from xpxchain import util
from tests import harness


class TestLoop(harness.TestCase):

    def test_get_event_loop(self):
        new_loop = asyncio.new_event_loop()
        self.assertIs(asyncio.get_event_loop(), util.get_event_loop())
        self.assertIs(new_loop, util.get_event_loop(new_loop))

        new_loop.close()

    def test_no_running_loop(self):
        with self.assertRaises(RuntimeError):
            util.get_running_loop()

    async def test_get_running_loop(self):
        self.assertIs(self.loop, util.get_running_loop())
