import aiohttp

from nem2 import client
from tests.harness import AsyncTestCase
from tests import responses


class AsyncHttpTest(AsyncTestCase):

    async def test_exceptions(self):
        http = client.AsyncHttp(responses.ENDPOINT)

        with self.assertRaises(aiohttp.ClientResponseError):
            with aiohttp.default_exception(aiohttp.ClientResponseError):
                await http.heartbeat()
        with self.assertRaises(ConnectionRefusedError):
            with aiohttp.default_exception(ConnectionRefusedError):
                await http.heartbeat()

    async def test_heartbeat(self):
        http = client.AsyncHttp(responses.ENDPOINT)

        with aiohttp.default_response(200, **responses.HEARTBEAT["Ok"]):
            self.assertEqual(await http.heartbeat(), client.Heartbeat.OK)

    async def test_status(self):
        http = client.AsyncHttp(responses.ENDPOINT)

        with aiohttp.default_response(200, **responses.STATUS["Local"]):
            self.assertEqual(await http.status(), client.Status.LOCAL)
        with aiohttp.default_response(200, **responses.STATUS["Synchronized"]):
            self.assertEqual(await http.status(), client.Status.SYNCHRONIZED)
        with aiohttp.default_response(200, **responses.STATUS["Unknown"]):
            self.assertEqual(await http.status(), client.Status.UNKNOWN)
        with self.assertRaises(ValueError):
            with aiohttp.default_response(200, **responses.STATUS["Error"]):
                await http.status()
