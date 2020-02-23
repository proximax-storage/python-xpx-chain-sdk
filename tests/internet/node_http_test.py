from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config


class TestNodeHttp(harness.TestCase):
    
    def test_get_node_info(self):
        with client.NodeHTTP(config.ENDPOINT) as http:
            info = http.get_node_info()
            self.assertEqual(isinstance(info, models.NodeInfo), True)
    
    def test_get_node_time(self):
        with client.NodeHTTP(config.ENDPOINT) as http:
            info = http.get_node_time()
            self.assertEqual(isinstance(info, models.NodeTime), True)
