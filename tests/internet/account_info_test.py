from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestAccountsInfo(harness.TestCase):

    @harness.test_case(
        sync_data=client.AccountHTTP,
        async_data=client.AsyncAccountHTTP
    )
    async def test_namespace_from_account(self, data, await_cb, with_cb):
        async with with_cb(data(responses.ENDPOINT)) as http:
            address = models.Address.create_from_raw_address("SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM")
            info = await await_cb(http.get_account_info(address))
            self.assertEqual(info.public_key, '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808')
