from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config


class TestNetworkHttp(harness.TestCase):
    
    def test_get_network_type(self):
        with client.NetworkHTTP(config.ENDPOINT) as http:
            info = http.get_network_type()
            self.assertEqual(isinstance(info, models.NetworkType), True)
