import aiohttp
import requests

from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestNamespaceHttp(harness.TestCase):

    @harness.test_case(
        sync_data=(client.NamespaceHttp, requests),
        async_data=(client.AsyncNamespaceHttp, aiohttp)
    )
    async def test_get_namespace(self, data, cb):
        http = data[0](responses.ENDPOINT)
        namespace_id = models.NamespaceId.from_hex("84b3552d375ffa4b")

        with data[1].default_response(200, **responses.NAMESPACE_INFO["nem"]):
            info = await cb(http.get_namespace(namespace_id))
            self.assertEqual(info.active, True)
            self.assertEqual(info.index, 0)
            self.assertEqual(info.meta_id, '5C7C07005CC1FE000176FA2B')
            self.assertEqual(info.type, models.NamespaceType.ROOT_NAMESPACE)
            self.assertEqual(info.depth, 1)
            self.assertEqual(info.levels, [namespace_id])
            self.assertEqual(info.parent_id, models.NamespaceId(0))
            self.assertEqual(info.owner.address.address, 'SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM')
            self.assertEqual(info.owner.public_key, '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808')
            self.assertEqual(info.start_height, 1)
            self.assertEqual(info.end_height, 18446744073709551615)
            self.assertEqual(info.alias, models.EmptyAlias())
            self.assertEqual(info, await cb(http.getNamespace(namespace_id)))

    @harness.test_case(
        sync_data=(client.NamespaceHttp, requests),
        async_data=(client.AsyncNamespaceHttp, aiohttp)
    )
    async def test_get_namespace_names(self, data, cb):
        http = data[0](responses.ENDPOINT)
        ids = [models.NamespaceId.from_hex("84b3552d375ffa4b")]

        with data[1].default_response(200, **responses.NAMESPACE_NAMES["nem"]):
            names = await cb(http.get_namespace_names(ids))
            self.assertEqual(len(names), 1)
            self.assertEqual(names[0].namespace_id.id, 0x84b3552d375ffa4b)
            self.assertEqual(names[0].name, "nem")
            self.assertEqual(names, await cb(http.getNamespaceNames(ids)))
