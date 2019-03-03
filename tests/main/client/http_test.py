import requests

from nem2 import client
from tests.harness import TestCase
from tests import responses


class HttpTest(TestCase):

    def test_exceptions(self):
        http = client.BlockchainHttp(responses.ENDPOINT)

        with self.assertRaises(requests.HTTPError):
            with requests.default_exception(requests.HTTPError):
                http.get_block_by_height(1)
        with self.assertRaises(ConnectionRefusedError):
            with requests.default_exception(ConnectionRefusedError):
                http.get_block_by_height(1)

    def test_from_host(self):
        http = client.Http(responses.ENDPOINT)
        copy = client.Http.from_host(http._host)
        self.assertTrue(http._host is copy._host)


class AccountHttpTest(TestCase):
    pass


class BlockchainHttpTest(TestCase):

    def test_get_block_by_height(self):
        http = client.BlockchainHttp(responses.ENDPOINT)

        with requests.default_response(200, **responses.BLOCK_INFO["Ok"]):
            block_info = http.get_block_by_height(1)
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
