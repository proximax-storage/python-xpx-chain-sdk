from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestDiagnosticStorage(harness.TestCase):

    @harness.test_case(
        sync_data=client.BlockchainHTTP,
        async_data=client.AsyncBlockchainHTTP
    )
    async def test_diagnostic_storage(self, data, await_cb, with_cb):
        async with with_cb(data(responses.ENDPOINT)) as http:
            self.assertIsInstance(await await_cb(http.get_diagnostic_storage()), models.BlockchainStorageInfo)
