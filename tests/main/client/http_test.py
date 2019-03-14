import asyncio
import aiohttp
import requests

from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestAsyncLoop(harness.TestCase):

    def test_loop(self):
        loop = asyncio.new_event_loop()
        http = client.AsyncHttp(responses.ENDPOINT, loop=loop)
        with aiohttp.default_response(200, **responses.BLOCK_INFO["Ok"]):
            block_info = loop.run_until_complete(http.blockchain.get_block_by_height(1))
            self.assertEqual(block_info.total_fee, 0)
        loop.close()


class TestHttp(harness.TestCase):

    @harness.test_case(
        sync_data=(client.NetworkHttp, requests, client.HTTPError),
        async_data=(client.AsyncNetworkHttp, aiohttp, client.AsyncHTTPError)
    )
    async def test_exceptions(self, data, cb):
        http = data[0](responses.ENDPOINT)
        with self.assertRaises(data[2]):
            with data[1].default_exception(data[2]):
                await cb(http.get_network_type())
        with self.assertRaises(ConnectionRefusedError):
            with data[1].default_exception(ConnectionRefusedError):
                await cb(http.get_network_type())

    @harness.test_case(
        sync_data=client.Http,
        async_data=client.AsyncHttp
    )
    async def test_from_http(self, data, cb):
        http = data(responses.ENDPOINT)
        copy = data.from_http(http)
        self.assertTrue(http.client is copy.client)

    @harness.test_case(
        sync_data=(client.Http, requests),
        async_data=(client.AsyncHttp, aiohttp)
    )
    async def test_network_type(self, data, cb):
        http = data[0](responses.ENDPOINT)
        with data[1].default_response(200, **responses.NETWORK_TYPE["MIJIN_TEST"]):
            self.assertEqual(await cb(http.network_type), models.NetworkType.MIJIN_TEST)
            self.assertEqual(await cb(http.networkType), models.NetworkType.MIJIN_TEST)
