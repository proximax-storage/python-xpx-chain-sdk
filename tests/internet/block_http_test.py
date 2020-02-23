from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config
from tests import responses


class TestBlockHttp(harness.TestCase):
    def __init__(self, task) -> None:
        super().__init__(task)

        if (task == 'test_get_merkle_by_hash_in_block'):
            with client.BlockchainHTTP(config.ENDPOINT) as http:
                reply = http.get_block_transactions(1)
                self.tx_hash = reply[0].transaction_info.hash

    def test_get_merkle_by_hash_in_block(self):
        with client.BlockchainHTTP(config.ENDPOINT) as http:
            info = http.get_merkle_by_hash_in_block(1, self.tx_hash)
            self.assertEqual(isinstance(info, models.MerkleProofInfo), True)
            self.assertEqual(len(info.merkle_path) > 0, True)
            self.assertEqual(isinstance(info.merkle_path[0], models.MerklePathItem), True)
        
    def test_get_blocks_by_height_with_limit(self):
        with client.BlockchainHTTP(config.ENDPOINT) as http:
            info = http.get_blocks_by_height_with_limit(25, 25)
            self.assertEqual(len(info), 25)
            self.assertEqual(isinstance(info[0], models.BlockInfo), True)
            
    def test_get_block_by_height(self):
        with client.BlockchainHTTP(config.ENDPOINT) as http:
            info = http.get_block_by_height(25)
            self.assertEqual(isinstance(info, models.BlockInfo), True)
            
    def test_get_block_transactions(self):
        with client.BlockchainHTTP(config.ENDPOINT) as http:
            info = http.get_block_transactions(1)
            self.assertEqual(len(info) > 0, True)
            self.assertEqual(isinstance(info[0], models.Transaction), True)
            self.assertEqual(info[0].signer.public_key, config.nemesis.public_key.upper())
    
    def test_get_block_receipts(self):
        with client.BlockchainHTTP(config.ENDPOINT) as http:
            info = http.get_block_receipts(25)
            self.assertEqual(isinstance(info, models.Statements), True),
            self.assertEqual(len(info.transaction_statements), 1),
            self.assertEqual(isinstance(info.transaction_statements[0], models.TransactionStatement), True),
            self.assertEqual(len(info.transaction_statements[0].receipts), 1),
            self.assertEqual(isinstance(info.transaction_statements[0].receipts[0], models.BalanceChangeReceipt), True),

    def test_get_diagnostic_storage(self):
        with client.BlockchainHTTP(config.ENDPOINT) as http:
            info = http.get_diagnostic_storage()
            self.assertEqual(isinstance(info, models.BlockchainStorageInfo), True),
    
    def test_get_diagnostic_server(self):
        with client.BlockchainHTTP(config.ENDPOINT) as http:
            info = http.get_diagnostic_server()
            self.assertEqual(isinstance(info, models.BlockchainServerInfo), True),
