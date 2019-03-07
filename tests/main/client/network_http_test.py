import aiohttp
import requests

from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestNetworkHttp(harness.TestCase):

    @harness.test_case(
        sync_data=(client.NetworkHttp, requests),
        async_data=(client.AsyncNetworkHttp, aiohttp),
    )
    async def test_get_network_type(self, data, cb):
        http = data[0](responses.ENDPOINT)
        with data[1].default_response(200, **responses.NETWORK_TYPE["MIJIN_TEST"]):
            self.assertEqual(await cb(http.get_network_type()), models.NetworkType.MIJIN_TEST)
            self.assertEqual(await cb(http.getNetworkType()), models.NetworkType.MIJIN_TEST)
