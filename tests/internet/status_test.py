from nem2 import client
from tests.harness import AsyncTestCase, TestCase
from tests import responses


class StatusTest(TestCase):

    def test_sync(self):
        http = client.Http(responses.ENDPOINT)
        self.assertEqual(http.status(), client.Status.SYNCHRONIZED)

class AsyncStatusTest(AsyncTestCase):

    async def test_async(self):
        http = client.AsyncHttp(responses.ENDPOINT)
        self.assertEqual(await http.status(), client.Status.SYNCHRONIZED)
