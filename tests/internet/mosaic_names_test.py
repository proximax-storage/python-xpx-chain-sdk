from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


class TestMosaicNames(harness.TestCase):

    @harness.test_case(
        sync_data=client.MosaicHttp,
        async_data=client.AsyncMosaicHttp
    )
    async def test_names(self, data, cb):
        http = data(responses.ENDPOINT)
        ids = [models.MosaicId.from_hex("d525ad41d95fcf29")]

        result = await cb(http.get_mosaic_names(ids))
        if len(result):
            self.assertEqual(result[0].name, "xem")
