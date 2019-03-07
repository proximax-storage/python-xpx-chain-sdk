from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestNetwork(harness.TestCase):

    @harness.create(__qualname__, client.NetworkHttp, client.AsyncNetworkHttp)
    async def test(self, cls, func):
        http = cls(responses.ENDPOINT)
        self.assertIsInstance(await func(http.network_type), models.NetworkType)
        self.assertIsInstance(await func(http.get_network_type()), models.NetworkType)
        self.assertIsInstance(await func(http.getNetworkType()), models.NetworkType)

    test_sync = harness.new_sync(__qualname__)
    test_async = harness.new_async(__qualname__)
