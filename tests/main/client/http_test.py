import asyncio
import aiohttp
import requests

from xpxchain import client
from xpxchain import models
from tests import harness
from tests import responses


class TestAsyncLoop(harness.TestCase):

    def test_loop(self):
        async def inner(loop):
            async with client.AsyncHTTP(responses.ENDPOINT, loop=loop) as http:
                # Set the network type
                with aiohttp.default_response(200, **responses.NETWORK_TYPE["MIJIN_TEST"]):
                    await http.network_type

                with aiohttp.default_response(200, **responses.BLOCK_INFO["Ok"]):
                    block_info = await http.blockchain.get_block_by_height(1)
                    self.assertEqual(block_info.total_fee, 0)

        loop = asyncio.new_event_loop()
        loop.run_until_complete(inner(loop))
        loop.close()


class TestHTTP(harness.TestCase):

    @harness.async_test(
        sync_data=(client.NetworkHTTP, requests, client.HTTPError),
        async_data=(client.AsyncNetworkHTTP, aiohttp, client.AsyncHTTPError)
    )
    async def test_exceptions(self, data, await_cb, with_cb):
        async with with_cb(data[0](responses.ENDPOINT)) as http:
            with self.assertRaises(data[2]):
                with data[1].default_exception(data[2]):
                    await await_cb(http.get_network_type())
            with self.assertRaises(ConnectionRefusedError):
                with data[1].default_exception(ConnectionRefusedError):
                    await await_cb(http.get_network_type())

    @harness.async_test(
        sync_data=client.HTTP,
        async_data=client.AsyncHTTP
    )
    async def test_create_from_http(self, data, await_cb, with_cb):
        async with with_cb(data(responses.ENDPOINT)) as http:
            copy = data.create_from_http(http)
            self.assertTrue(http.raw is copy.raw)

    @harness.async_test(
        sync_data=(client.HTTP, requests),
        async_data=(client.AsyncHTTP, aiohttp)
    )
    async def test_network_type(self, data, await_cb, with_cb):
        async with with_cb(data[0](responses.ENDPOINT)) as http:
            with data[1].default_response(200, **responses.NETWORK_TYPE["MIJIN_TEST"]):
                self.assertEqual(await await_cb(http.network_type), models.NetworkType.MIJIN_TEST)
