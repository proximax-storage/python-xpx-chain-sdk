from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestBlockchainScore(harness.TestCase):

    @harness.test_case(
        sync_data=client.BlockchainHttp,
        async_data=client.AsyncBlockchainHttp
    )
    async def test_blockchain_score(self, data, await_cb, with_cb):
        async with with_cb(data(responses.ENDPOINT)) as http:
            self.assertIsInstance(await await_cb(http.get_blockchain_score()), models.BlockchainScore)
