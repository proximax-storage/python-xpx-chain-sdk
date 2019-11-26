from nem2 import client
from nem2 import models
from tests import harness
from tests import config


@harness.http_test_case({
    'clients': (client.BlockchainHTTP, client.AsyncBlockchainHTTP),
    'tests': [
        {
            #/chain/height
            'name': 'test_get_blockchain_height',
            'params': [],
            'method': 'get_blockchain_height',
            'validation': [
                lambda x: (isinstance(x, int), True),
                lambda x: (x >= config.Blockchain.height, True),
            ]
        },
        {
            #/chain/score
            'name': 'test_get_blockchain_score',
            'params': [],
            'method': 'get_blockchain_score',
            'validation': [
                lambda x: (isinstance(x, models.BlockchainScore), True),
            ]
        },
    ],
})
class TestChainHttp(harness.TestCase):
    pass