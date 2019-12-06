from nem2 import client
from nem2 import models
from tests import harness
from tests import config


@harness.http_test_case({
    'clients': (client.BlockchainHTTP, client.AsyncBlockchainHTTP),
    'tests': [
#        {
#            #/blocks/{height}/limit/{limit}
#            'name': 'test_get_blocks_by_height_with_limit',
#            'params': [100, 25],
#            'method': 'get_blocks_by_height_with_limit',
#            'validation': [
#                lambda x: (len(x), 25),
#                lambda x: (isinstance(x[0], models.BlockInfo), True)
#            ]
#        },
#        {
#            #/block/{height}
#            'name': 'test_get_block_by_height',
#            'params': [100],
#            'method': 'get_block_by_height',
#            'validation': [
#                lambda x: (isinstance(x, models.BlockInfo), True)
#            ]
#        },
#        {
#            #/block/{height}/transactions
#            'name': 'test_get_block_transactions',
#            'params': [100],
#            'method': 'get_block_transactions',
#            'validation': [
#                lambda x: (len(x), 0)
#            ]
#        },
#        {
#            #/block/{height}/transactions/{hash}/merkle
#            'name': 'test_get_merkle_by_hash_in_block',
#            'params': [1, "BE34D62D7410F2DE7F70F423647F1D983FD315FAE44576A75714CB902355FC72"],
#            'method': 'get_merkle_by_hash_in_block',
#            'validation': [
#                lambda x: (isinstance(x, models.MerkleProofInfo), True),
#                lambda x: (len(x.merkle_path), 5),
#                lambda x: (isinstance(x.merkle_path[0], models.MerklePathItem), True)
#            ]
#        },
        {
            #/block/{height}/receipts
            'name': 'test_get_block_receipts',
            'params': [42545],
            'method': 'get_block_receipts',
            'validation': [
                lambda x: (isinstance(x, models.Statements), True),
                lambda x: (len(x.transaction_statements), 1),
                lambda x: (isinstance(x.transaction_statements[0], models.TransactionStatement), True),
                lambda x: (x.transaction_statements[0].height, 42545),
                lambda x: (len(x.transaction_statements[0].receipts), 1),
                lambda x: (isinstance(x.transaction_statements[0].receipts[0], models.BalanceChangeReceipt), True),
                lambda x: (x.transaction_statements[0].receipts[0].account, "346E56F77F07B19D48B3AEF969EDB01F68A5AC9FAF8E5E007577D71BA66385FB")
            ]
        },
    ],
})
class TestBlockHttp(harness.TestCase):
    pass
