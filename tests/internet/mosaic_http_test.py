from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config


class TestMosaicHttp(harness.TestCase):
    
    def test_get_mosaic(self):
        with client.MosaicHTTP(config.ENDPOINT) as http:
            info = http.get_mosaic(models.MosaicId.create_from_hex('0dc67fbe1cad29e3'))
            self.assertEqual(isinstance(info, models.MosaicInfo), True)
    
    def test_get_mosaics(self):
        with client.MosaicHTTP(config.ENDPOINT) as http:
            info = http.get_mosaics([models.MosaicId.create_from_hex('0dc67fbe1cad29e3')])
            self.assertEqual(len(info), 1)
            self.assertEqual(isinstance(info[0], models.MosaicInfo), True)
    
    def test_get_mosaic_names(self):
        with client.MosaicHTTP(config.ENDPOINT) as http:
            info = http.get_mosaic_names([models.MosaicId.create_from_hex('0dc67fbe1cad29e3')])
            self.assertEqual(len(info), 1),
            self.assertEqual(isinstance(info[0], models.MosaicName), True)
            self.assertEqual(info[0].names[0], 'prx.xpx')
