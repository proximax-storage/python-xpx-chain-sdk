from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config


class TestConfigHttp(harness.TestCase):
    
    def test_get_config(self):
        with client.ConfigHTTP(config.ENDPOINT) as http:
            info = http.get_config(1)
            self.assertEqual(isinstance(info, models.CatapultConfig), True),
    
    def test_get_upgrade(self):
        with client.ConfigHTTP(config.ENDPOINT) as http:
            info = http.get_upgrade(1)
            self.assertEqual(isinstance(info, models.CatapultUpgrade), True),
