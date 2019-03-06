import aiohttp
import asyncio

from nem2 import client
from nem2 import models
from tests.harness import AsyncTestCase
from tests import responses


class TestAsyncLoop(AsyncTestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName=methodName, loop=asyncio.new_event_loop())

    async def test_loop(self):
        http = client.AsyncHttp(responses.ENDPOINT, loop=self.loop)
        with aiohttp.default_response(200, **responses.BLOCK_INFO["Ok"]):
            block_info = await http.blockchain.get_block_by_height(1)
            self.assertEqual(block_info.total_fee, 0)


class TestAsyncHttp(AsyncTestCase):

    async def test_exceptions(self):
        http = client.AsyncBlockchainHttp(responses.ENDPOINT)

        with self.assertRaises(aiohttp.ClientResponseError):
            with aiohttp.default_exception(aiohttp.ClientResponseError):
                await http.get_block_by_height(1)
        with self.assertRaises(ConnectionRefusedError):
            with aiohttp.default_exception(ConnectionRefusedError):
                await http.get_block_by_height(1)

    def test_from_http(self):
        http = client.AsyncHttp(responses.ENDPOINT)
        copy = client.AsyncHttp.from_http(http)
        self.assertTrue(http._host is copy._host)

    async def test_network_type(self):
        http = client.AsyncHttp(responses.ENDPOINT)
        with aiohttp.default_response(200, **responses.NETWORK_TYPE["MIJIN_TEST"]):
            self.assertEqual(await http.network_type, models.NetworkType.MIJIN_TEST)


class TestAsyncAccountHttp(AsyncTestCase):
    pass


class TestAsyncBlockchainHttp(AsyncTestCase):

    async def test_get_block_by_height(self):
        http = client.AsyncBlockchainHttp(responses.ENDPOINT)

        with aiohttp.default_response(200, **responses.BLOCK_INFO["Ok"]):
            block_info = await http.get_block_by_height(1)
            self.assertEqual(block_info.hash, "3A2D7D82D9B7F2C12E1CD549BC0C515A9150698EC0ADBF94121AB5D1730CEAA1")
            self.assertEqual(block_info.generation_hash, "80BB92D88ED9908CFD33E85E10DAA716F055C61997BEF3F2F6F711B5F3B66986")
            self.assertEqual(block_info.total_fee, 0)
            self.assertEqual(block_info.num_transactions, 25)
            self.assertEqual(block_info.signature, "A9BB70EDB0E04A83829F3A32BA0C1361FD8E317243DF748EE00FA8A0E52D4A6793B41752A29FDD10407B1FAC96259AC0D6B489F7CC4ADF960B69103FF51D5A01")
            self.assertEqual(block_info.signer.public_key, "7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808")
            self.assertEqual(block_info.version, 36867)
            self.assertEqual(block_info.type, 32835)
            self.assertEqual(block_info.height, 1)
            self.assertEqual(block_info.timestamp, 0)
            self.assertEqual(block_info.difficulty, 100000000000000)
            self.assertEqual(block_info.previous_block_hash, "0000000000000000000000000000000000000000000000000000000000000000")
            self.assertEqual(block_info.block_transactions_hash, "54B187F7D6B1D45F133F06706566E832A9F325F1E62FE927C0B5C65DAC8A2C56")


class TestAsyncMosaicHttp(AsyncTestCase):
    # TODO(ahuszagh) Implement
    pass


class TestAsyncNamespaceHttp(AsyncTestCase):
    # TODO(ahuszagh) Implement
    pass


class TestAsyncNetworkHttp(AsyncTestCase):
    # TODO(ahuszagh) Implement
    pass


class TestAsyncTransactionHttp(AsyncTestCase):
    # TODO(ahuszagh) Implement
    pass
