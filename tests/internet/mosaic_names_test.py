from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestMosaicNames(harness.TestCase):

    @harness.test_case(
        sync_data=client.MosaicHTTP,
        async_data=client.AsyncMosaicHTTP
    )
    async def test_names(self, data, await_cb, with_cb):
        async with with_cb(data(responses.ENDPOINT)) as http:
            ids = [models.MosaicId.from_hex("d525ad41d95fcf29")]
            result = await await_cb(http.get_mosaic_names(ids))
            if len(result):
                self.assertEqual(result[0].name, "xem")
