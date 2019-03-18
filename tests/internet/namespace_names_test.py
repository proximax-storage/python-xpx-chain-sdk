from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestNamespaceNames(harness.TestCase):

    @harness.test_case(
        sync_data=client.NamespaceHTTP,
        async_data=client.AsyncNamespaceHTTP
    )
    async def test_names(self, data, await_cb, with_cb):
        async with with_cb(data(responses.ENDPOINT)) as http:
            ids = [models.NamespaceId.from_hex("84b3552d375ffa4b")]
            result = await await_cb(http.get_namespace_names(ids))
            if len(result):
                self.assertEqual(result[0].name, "nem")
