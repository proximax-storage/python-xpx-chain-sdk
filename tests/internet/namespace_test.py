from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestNamespace(harness.TestCase):

    @harness.test_case(
        sync_data=client.NamespaceHttp,
        async_data=client.AsyncNamespaceHttp
    )
    async def test_namespace(self, data, cb):
        http = data(responses.ENDPOINT)
        namespace_id = models.NamespaceId.from_hex("84b3552d375ffa4b")

        info = await cb(http.get_namespace(namespace_id))
        self.assertEqual(info.meta_id, '5C7C07005CC1FE000176FA2B')
