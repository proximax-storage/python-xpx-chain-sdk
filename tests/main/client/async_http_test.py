import aiohttp
import asyncio

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


class TestAsyncHttp(harness.TestCase):

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


class TestAsyncAccountHttp(harness.TestCase):
    # TODO(ahuszagh) Implement
    pass


class TestAsyncBlockchainHttp(harness.TestCase):

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


class TestAsyncMosaicHttp(harness.TestCase):
    # TODO(ahuszagh) Implement
    pass


class TestAsyncNamespaceHttp(harness.TestCase):

    async def test_get_namespace_names(self):
        http = client.AsyncNamespaceHttp(responses.ENDPOINT)
        ids = [models.NamespaceId.from_hex("84b3552d375ffa4b")]

        with aiohttp.default_response(200, **responses.NAMESPACE_NAMES["Ok"]):
            namespace_names = await http.get_namespace_names(ids)
            self.assertEqual(len(namespace_names), 1)
            self.assertEqual(namespace_names[0].namespace_id.id, 0x84b3552d375ffa4b)
            self.assertEqual(namespace_names[0].name, "nem")


class TestAsyncNetworkHttp(harness.TestCase):
    # TODO(ahuszagh) Implement
    pass


class TestAsyncTransactionHttp(harness.TestCase):
    # TODO(ahuszagh) Implement
    pass
