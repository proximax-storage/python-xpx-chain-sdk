from nem2 import client
from nem2 import models
from tests import harness
from tests import config


@harness.http_test_case({
    'clients': (client.BlockchainHTTP, client.AsyncBlockchainHTTP),
    'tests': [
        {
            'name': 'test_get_blockchain_height',
            'params': [],
            'method': 'get_blockchain_height',
            'validation': [
                lambda x: (x >= config.Blockchain.height, True),
            ]
        },
        {
            'name': 'test_get_blockchain_height',
            'params': [],
            'method': 'get_blockchain_height',
            'validation': [
                lambda x: (isinstance(x, int), True),
                lambda x: (x >= config.Blockchain.height, True),
            ]
        },
        {
            'name': 'test_get_blockchain_score',
            'params': [],
            'method': 'get_blockchain_score',
            'validation': [
                lambda x: (isinstance(x, models.BlockchainScore), True),
            ]
        },
        {
            'name': 'test_get_diagnostic_storage',
            'params': [],
            'method': 'get_diagnostic_storage',
            'validation': [
                lambda x: (isinstance(x, models.BlockchainStorageInfo), True),
            ]
        },
        {
            'name': 'test_get_diagnostic_server',
            'params': [],
            'method': 'get_diagnostic_server',
            'validation': [
                lambda x: (isinstance(x, models.BlockchainServerInfo), True),
            ]
        },
    ],
})
class TestBlockchainHttp(harness.TestCase):
    pass
