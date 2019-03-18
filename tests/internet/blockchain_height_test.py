from nem2 import client
from tests import harness
from tests import responses


class TestBlockchainHeight(harness.TestCase):

    @harness.test_case(
        sync_data=client.BlockchainHTTP,
        async_data=client.AsyncBlockchainHTTP
    )
    async def test_blockchain_height(self, data, await_cb, with_cb):
        async with with_cb(data(responses.ENDPOINT)) as http:
            self.assertGreaterEqual(await await_cb(http.get_blockchain_height()), 11402)
