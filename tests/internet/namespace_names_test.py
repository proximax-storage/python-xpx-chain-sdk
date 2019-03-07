from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestNamespaceNames(harness.TestCase):

    @harness.create(__qualname__, client.NamespaceHttp, client.AsyncNamespaceHttp)
    async def test(self, cls, func):
        http = cls(responses.ENDPOINT)
        ids = [models.NamespaceId.from_hex("84b3552d375ffa4b")]

        result = await func(http.get_namespace_names(ids))
        if len(result):
            self.assertEqual(result[0].name, "nem")

    test_sync = harness.new_sync(__qualname__)
    test_async = harness.new_async(__qualname__)
