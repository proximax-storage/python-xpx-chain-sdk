from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config
from tests import responses

@harness.http_test_case({
    'clients': (client.BlockchainHTTP, client.AsyncBlockchainHTTP),
    'tests': [
        {
            #/blocks/{height}/limit/{limit}
            'name': 'test_get_blocks_by_height_with_limit',
            'params': [25, 25],
            'method': 'get_blocks_by_height_with_limit',
            'validation': [
                lambda x: (len(x), 25),
                lambda x: (isinstance(x[0], models.BlockInfo), True)
            ]
        },
        {
            #/block/{height}
            'name': 'test_get_block_by_height',
            'params': [25],
            'method': 'get_block_by_height',
            'validation': [
                lambda x: (isinstance(x, models.BlockInfo), True)
            ]
        },
        {
            #/block/{height}/transactions
            'name': 'test_get_block_transactions',
            'params': [1],
            'method': 'get_block_transactions',
            'validation': [
                lambda x: (len(x) > 0, True),
                lambda x: (isinstance(x[0], models.Transaction), True),
                lambda x: (x[0].signer.public_key, config.nemesis_signer_public_key),
            ]
        },
        {
            #/block/{height}/receipts
            'name': 'test_get_block_receipts',
            'params': [25],
            'method': 'get_block_receipts',
            'validation': [
                lambda x: (isinstance(x, models.Statements), True),
                lambda x: (len(x.transaction_statements), 1),
                lambda x: (isinstance(x.transaction_statements[0], models.TransactionStatement), True),
                lambda x: (len(x.transaction_statements[0].receipts), 1),
                lambda x: (isinstance(x.transaction_statements[0].receipts[0], models.BalanceChangeReceipt), True),
                lambda x: (x.transaction_statements[0].receipts[0].account, config.nemesis_harvesting_public_key)
            ]
        },
        #TODO: Looks like there's no hash in receipts yet 
        #/block/{height}/receipt/{hash}/merkle
    ],
})
class TestBlockHttp(harness.TestCase):
    def __init__(self, task) -> None:
        super().__init__(task)

        if (task == 'test_get_merkle_by_hash_in_block'):
            with client.BlockchainHTTP(responses.ENDPOINT) as http:
                reply = http.get_block_transactions(1)
                self.tx_hash = reply[0].transaction_info.hash

    
    def test_get_merkle_by_hash_in_block(self):
        with client.BlockchainHTTP(responses.ENDPOINT) as http:
            reply = http.get_merkle_by_hash_in_block(1, self.tx_hash)    
            self.assertEqual(isinstance(reply, models.MerkleProofInfo), True)
            self.assertEqual(len(reply.merkle_path) > 0, True)
            self.assertEqual(isinstance(reply.merkle_path[0], models.MerklePathItem), True)
