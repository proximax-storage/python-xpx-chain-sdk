import aiohttp
import requests

from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestAccountHTTP(harness.TestCase):

    @harness.test_case(
        sync_data=(client.AccountHTTP, requests),
        async_data=(client.AsyncAccountHTTP, aiohttp)
    )
    async def test_get_namespaces_from_account(self, data, await_cb, with_cb):
        async with with_cb(data[0](responses.ENDPOINT)) as http:
            # Set the network type
            with data[1].default_response(200, **responses.NETWORK_TYPE["MIJIN_TEST"]):
                await await_cb(http.network_type)

            address = models.Address.create_from_raw_address("SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM")
            with data[1].default_response(200, **responses.ACCOUNT_INFO["Ok"]):
                info = await await_cb(http.get_account_info(address))
                self.assertEqual(info.public_key, '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808')

    @harness.test_case(
        sync_data=(client.AccountHTTP, requests),
        async_data=(client.AsyncAccountHTTP, aiohttp)
    )
    async def test_get_namespaces_from_accounts(self, data, await_cb, with_cb):
        async with with_cb(data[0](responses.ENDPOINT)) as http:
            # Set the network type
            with data[1].default_response(200, **responses.NETWORK_TYPE["MIJIN_TEST"]):
                await await_cb(http.network_type)

            addresses = [models.Address.create_from_raw_address("SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM")]
            with data[1].default_response(200, **responses.ACCOUNTS_INFO["Ok"]):
                infos = await await_cb(http.get_accounts_info(addresses))
                self.assertEqual(len(infos), 1)
                self.assertEqual(infos[0].public_key, '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808')
