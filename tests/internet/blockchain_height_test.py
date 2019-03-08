from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestBlockchainHeight(harness.TestCase):

    @harness.test_case(
        sync_data=client.BlockchainHttp,
        async_data=client.AsyncBlockchainHttp
    )
    async def test_blockchain_height(self, data, cb):
        http = data(responses.ENDPOINT)
        self.assertGreaterEqual(await cb(http.get_blockchain_height()), 11402)
