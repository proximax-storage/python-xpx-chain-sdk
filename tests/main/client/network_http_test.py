import aiohttp
import requests

from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestNetworkHTTP(harness.TestCase):

    @harness.test_case(
        sync_data=(client.NetworkHTTP, requests),
        async_data=(client.AsyncNetworkHTTP, aiohttp),
    )
    async def test_get_network_type(self, data, await_cb, with_cb):
        async with with_cb(data[0](responses.ENDPOINT)) as http:
            with data[1].default_response(200, **responses.NETWORK_TYPE["MIJIN_TEST"]):
                self.assertEqual(await await_cb(http.get_network_type()), models.NetworkType.MIJIN_TEST)
