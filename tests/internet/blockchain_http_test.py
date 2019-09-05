from nem2 import client
from nem2 import models
from tests import harness
from tests import config


@harness.http_test_case({
    'clients': (client.BlockchainHTTP, client.AsyncBlockchainHTTP),
    'tests': [
        {
            'name': 'test_get_blocks_by_height_with_limit',
            'params': [100, 25],
            'method': 'get_blocks_by_height_with_limit',
            'validation': [
                lambda x: (len(x), 25),
                lambda x: (isinstance(x[0], models.BlockInfo), True)
            ]
        },
        {
            'name': 'test_get_block_by_height',
            'params': [100],
            'method': 'get_block_by_height',
            'validation': [
                lambda x: (isinstance(x, models.BlockInfo), True)
            ]
        },
        {
            'name': 'test_get_block_transactions',
            'params': [100],
            'method': 'get_block_transactions',
            'validation': [
                lambda x: (len(x), 0)
            ]
        },
        {
            'name': 'test_get_merkle_by_hash_in_block',
            'params': [1, "BE34D62D7410F2DE7F70F423647F1D983FD315FAE44576A75714CB902355FC72"],
            'method': 'get_merkle_by_hash_in_block',
            'validation': [
                lambda x: (isinstance(x, models.MerkleProofInfo), True),
                lambda x: (len(x.merkle_path), 5),
                lambda x: (isinstance(x.merkle_path[0], models.MerklePathItem), True)
            ]
        },
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
