from nem2 import client
from nem2 import models
from tests.harness import AsyncTestCase, TestCase
from tests import responses


class NetworkTest(TestCase):

    def test_sync(self):
        http = client.Http(responses.ENDPOINT)
        network = http.network
        self.assertIsInstance(http.network_type, models.NetworkType)
        self.assertIsInstance(network.get_network_type(), models.NetworkType)
        self.assertIsInstance(network.getNetworkType(), models.NetworkType)


class AsyncNetworkTest(AsyncTestCase):

    async def test_async(self):
        http = client.AsyncHttp(responses.ENDPOINT)
        network = http.network
        self.assertIsInstance(await http.network_type, models.NetworkType)
        self.assertIsInstance(await network.get_network_type(), models.NetworkType)
        self.assertIsInstance(await network.getNetworkType(), models.NetworkType)
