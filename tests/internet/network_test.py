from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestNetwork(harness.TestCase):

    @harness.test_case(
        sync_data=client.NetworkHttp,
        async_data=client.AsyncNetworkHttp
    )
    async def test_network(self, data, await_cb, with_cb):
        async with with_cb(data(responses.ENDPOINT)) as http:
            self.assertIsInstance(await await_cb(http.network_type), models.NetworkType)
            self.assertIsInstance(await await_cb(http.get_network_type()), models.NetworkType)
            self.assertIsInstance(await await_cb(http.getNetworkType()), models.NetworkType)
