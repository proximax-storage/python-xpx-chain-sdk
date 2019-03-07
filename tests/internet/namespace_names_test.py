from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestNamespaceNames(harness.TestCase):

    @harness.test_case(
        sync_data=client.NamespaceHttp,
        async_data=client.AsyncNamespaceHttp
    )
    async def test_names(self, data, cb):
        http = data(responses.ENDPOINT)
        ids = [models.NamespaceId.from_hex("84b3552d375ffa4b")]

        result = await cb(http.get_namespace_names(ids))
        if len(result):
            self.assertEqual(result[0].name, "nem")
