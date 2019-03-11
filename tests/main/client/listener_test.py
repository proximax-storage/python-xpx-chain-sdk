from nem2 import client
from tests import harness


class TestListener(harness.TestCase):

    def test(self):
        # TODO(ahuszagh) Give a better name.
        listener = client.Listener('localhost:3000/block')
        del listener
