from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestNamespaceFromAccount(harness.TestCase):

    @harness.test_case(
        sync_data=client.NamespaceHttp,
        async_data=client.AsyncNamespaceHttp
    )
    async def test_namespace_from_account(self, data, await_cb, with_cb):
        async with with_cb(data(responses.ENDPOINT)) as http:
            address = models.Address.create_from_raw_address("SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM")
            infos = await await_cb(http.get_namespaces_from_account(address))
            self.assertEqual(len(infos), 1)
            self.assertEqual(infos[0].meta_id, '5C7C07005CC1FE000176FA2B')