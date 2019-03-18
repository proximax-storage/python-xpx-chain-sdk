import aiohttp
import requests

from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestBlockchainHTTP(harness.TestCase):

    @harness.test_case(
        sync_data=(client.BlockchainHTTP, requests),
        async_data=(client.AsyncBlockchainHTTP, aiohttp)
    )
    async def test_get_block_by_height(self, data, await_cb, with_cb):

        async with with_cb(data[0](responses.ENDPOINT)) as http:
            # Set the network type
            with data[1].default_response(200, **responses.NETWORK_TYPE["MIJIN_TEST"]):
                await await_cb(http.network_type)

            with data[1].default_response(200, **responses.BLOCK_INFO["Ok"]):
                block_info = await await_cb(http.get_block_by_height(1))
                self.assertEqual(block_info.hash, "3A2D7D82D9B7F2C12E1CD549BC0C515A9150698EC0ADBF94121AB5D1730CEAA1")
                self.assertEqual(block_info.generation_hash, "80BB92D88ED9908CFD33E85E10DAA716F055C61997BEF3F2F6F711B5F3B66986")
                self.assertEqual(block_info.total_fee, 0)
                self.assertEqual(block_info.num_transactions, 25)
                self.assertEqual(block_info.signature, "A9BB70EDB0E04A83829F3A32BA0C1361FD8E317243DF748EE00FA8A0E52D4A6793B41752A29FDD10407B1FAC96259AC0D6B489F7CC4ADF960B69103FF51D5A01")
                self.assertEqual(block_info.signer.public_key, "7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808")
                self.assertEqual(block_info.network_type, models.NetworkType.MIJIN_TEST)
                self.assertEqual(block_info.version, 36867)
                self.assertEqual(block_info.type, 32835)
                self.assertEqual(block_info.height, 1)
                self.assertEqual(block_info.timestamp, 0)
                self.assertEqual(block_info.difficulty, 100000000000000)
                self.assertEqual(block_info.previous_block_hash, "0000000000000000000000000000000000000000000000000000000000000000")
                self.assertEqual(block_info.block_transactions_hash, "54B187F7D6B1D45F133F06706566E832A9F325F1E62FE927C0B5C65DAC8A2C56")
                self.assertEqual(block_info.merkle_tree[0], "smNSI9tFz7tOIc38NZ/n8iKm5fYADJnKnnKdsC5mYfU=")
                self.assertEqual(block_info, await await_cb(http.getBlockByHeight(1)))
