from xpxchain import client
from xpxchain import models
from tests import harness


@harness.http_test_case({
    'clients': (client.MosaicHTTP, client.AsyncMosaicHTTP),
    'tests': [
        {
            #/mosaic/{mosaicId}
            'name': 'test_get_mosaic',
            'params': [models.MosaicId.create_from_hex('0dc67fbe1cad29e3')],
            'method': 'get_mosaic',
            'validation': [
                lambda x: (x.owner.public_key, 'B4F12E7C9F6946091E2CB8B6D3A12B50D17CCBBF646386EA27CE2946A7423DCF'),
            ]
        },
        {
            #/mosaic
            'name': 'test_get_mosaics',
            'params': [[models.MosaicId.create_from_hex('0dc67fbe1cad29e3')]],
            'method': 'get_mosaics',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].owner.public_key, 'B4F12E7C9F6946091E2CB8B6D3A12B50D17CCBBF646386EA27CE2946A7423DCF'),
            ]
        },
        {
            #/mosaic/names
            'name': 'test_get_mosaic_names',
            'params': [[models.MosaicId.create_from_hex('0dc67fbe1cad29e3')]],
            'method': 'get_mosaic_names',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].names[0], 'prx.xpx'),
            ]
        },
    ],
})
class TestMosaicHttp(harness.TestCase):
    pass
