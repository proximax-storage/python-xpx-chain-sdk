from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config


class TestChainHttp(harness.TestCase):
    
    def test_get_blockchain_height(self):
        with client.BlockchainHTTP(config.ENDPOINT) as http:
            info = http.get_blockchain_height()
            self.assertEqual(isinstance(info, int), True)
            self.assertEqual(info >= 1, True)
    
    def test_get_blockchain_height(self):
        with client.BlockchainHTTP(config.ENDPOINT) as http:
            info = http.get_blockchain_score()
            self.assertEqual(isinstance(info, models.BlockchainScore), True),
