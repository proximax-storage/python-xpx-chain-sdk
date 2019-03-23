from nem2 import client
from nem2 import models
from tests import harness


@harness.http_test_case({
    'clients': (client.MosaicHTTP, client.AsyncMosaicHTTP),
    'tests': [
        {
            'name': 'test_get_mosaic_names',
            'params': [[models.MosaicId.from_hex('d525ad41d95fcf29')]],
            'method': 'get_mosaic_names',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].name, 'xem'),
            ]
        },
    ],
})
class TestMosaicHttp(harness.TestCase):
    pass
