from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestDiagnosticStorage(harness.TestCase):

    @harness.test_case(
        sync_data=client.BlockchainHttp,
        async_data=client.AsyncBlockchainHttp
    )
    async def test_diagnostic_storage(self, data, cb):
        http = data(responses.ENDPOINT)
        self.assertIsInstance(await cb(http.get_diagnostic_storage()), models.BlockchainStorageInfo)
