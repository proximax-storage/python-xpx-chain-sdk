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
    async def test_get_namespace_names(self, data, cb):
        http = data[0](responses.ENDPOINT)
        ids = [models.NamespaceId.from_hex("84b3552d375ffa4b")]

        with data[1].default_response(200, **responses.NAMESPACE_NAMES["Ok"]):
            names = await cb(http.get_namespace_names(ids))
            self.assertEqual(len(names), 1)
            self.assertEqual(names[0].namespace_id.id, 0x84b3552d375ffa4b)
            self.assertEqual(names[0].name, "nem")
            self.assertEqual(names, await cb(http.getNamespaceNames(ids)))
