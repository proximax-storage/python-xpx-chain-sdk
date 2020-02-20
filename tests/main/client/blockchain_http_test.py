from xpxchain import client
from xpxchain import models
from tests import harness
from tests import responses


@harness.mocked_http_test_case({
    'clients': (client.BlockchainHTTP, client.AsyncBlockchainHTTP),
    'network_type': models.NetworkType.MIJIN_TEST,
    'tests': [
        {
            'name': 'test_get_block_by_height',
            'response': responses.BLOCK_INFO["Ok"],
            'params': [1],
            'method': 'get_block_by_height',
            'validation': [
                lambda x: (x.hash, '04628F15E89936912DCA6345D60E668F513D50E7FC6BAF3F1C723C92CFC4FED6'),
                lambda x: (x.generation_hash, '7CCDF81A60B0A03A3B30D715C5C7513916319C09215E22C67B0A81106FB21445'),
                lambda x: (x.total_fee, 0),
                lambda x: (x.num_transactions, 31),
                lambda x: (x.signature, "82D8C518BF32CA9A8478451F79B7EEC69F11E6022AF7230CE21F230A09E51A0CEB169454CB4AD4499BC9C0769B468AB5A6DD716D00C977F16BF63DD1B0653305"),
                lambda x: (x.signer.public_key, "A04335F99D9EE3787528A16C7A302F80D511E9CF71D97D95C2182E0EA75A1EF9"),
                lambda x: (x.network_type, models.NetworkType.MIJIN_TEST),
                lambda x: (x.version, 3),
                lambda x: (x.type, 32835),
                lambda x: (x.height, 1),
                lambda x: (x.timestamp, 0),
                lambda x: (x.fee_multiplier, 0),
                lambda x: (x.difficulty, 100000000000000),
                lambda x: (x.previous_block_hash, "0000000000000000000000000000000000000000000000000000000000000000"),
                lambda x: (x.block_transactions_hash, "36822DF1CF1827915A8CDDF8A47EBBF1D1C55666DB1E8AC942C447D3D0E6D494"),
                lambda x: (x.block_receipts_hash, "RMViDPTpgKd072qPgxmPVoabWcrmFs5v5EGS00GxiX0="),
                lambda x: (x.state_hash, "C61C28E078298D6A508A649637EAC7D9D1E5F3813856EF9B7F1579866ACB570E"),
                lambda x: (x.merkle_tree, []),
            ]
        },
        {
            'name': 'test_get_blocks_by_height_with_limit',
            'response': responses.BLOCKS_INFO["Ok"],
            'params': [1, 1],
            'method': 'get_blocks_by_height_with_limit',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].hash, '04628F15E89936912DCA6345D60E668F513D50E7FC6BAF3F1C723C92CFC4FED6'),
            ]
        },
        {
            'name': 'test_get_block_transactions',
            'response': responses.BLOCK_TRANSACTIONS["Ok"],
            'params': [1],
            'method': 'get_block_transactions',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].transaction_info.height, 1),
                lambda x: (x[0].transaction_info.hash, "0E814F8D301E90144F1F25384C05AC26EF9D45FACAD216590B876FBB09877E02"),
                lambda x: (x[0].transaction_info.merkle_component_hash, "0E814F8D301E90144F1F25384C05AC26EF9D45FACAD216590B876FBB09877E02"),
                lambda x: (x[0].signature, "C214F728EA91BB9947F843CB6FF59EB8D231DB652796D25D055E4D1D8E65BF67F8800B268257E9478418E1AA0D7C8DB451E82176437D21F11EB777384583230B"),
                lambda x: (x[0].signer.public_key, "A04335F99D9EE3787528A16C7A302F80D511E9CF71D97D95C2182E0EA75A1EF9"),
                lambda x: (x[0].version, 2),
                lambda x: (x[0].type, 16718),
                lambda x: (x[0].max_fee, 0),
                lambda x: (x[0].namespace_type, models.NamespaceType.ROOT_NAMESPACE),
                lambda x: (x[0].duration, 0),
                lambda x: (x[0].namespace_id, models.NamespaceId.create_from_hex('b1497f5fba651b4f')),
                lambda x: (x[0].namespace_name, 'cat'),
            ]
        },
        {
            'name': 'test_get_blockchain_height',
            'response': responses.CHAIN_HEIGHT["Ok"],
            'params': [],
            'method': 'get_blockchain_height',
            'validation': [
                lambda x: (x, 53577),
            ]
        },
        {
            'name': 'test_get_blockchain_score',
            'response': responses.CHAIN_SCORE["Ok"],
            'params': [],
            'method': 'get_blockchain_score',
            'validation': [
                lambda x: (isinstance(x, models.BlockchainScore), True),
                lambda x: (x.score, 0x791f69c466a3658),
                lambda x: (x.score_low, 0x791f69c466a3658),
                lambda x: (x.score_high, 0),
            ]
        },
        {
            'name': 'test_get_diagnostic_blocks_by_height_with_limit',
            'response': responses.DIAGNOSTIC_BLOCKS_INFO["Ok"],
            'params': [1, 5],
            'method': 'get_diagnostic_blocks_by_height_with_limit',
            'validation': [
                lambda x: (len(x), 5),
                lambda x: (x[0].hash, '22A2B807BF395CC9432DB4075B8A6D412EF7FD0892D266959D02D942C0F48576'),
                lambda x: (x[0].merkle_tree[0], '796159C97C02FB6F38BB7C07F9F367A5E7362090D4FDA34739979A6647E127D3'),
                lambda x: (x[1].hash, 'DF7539D4AC9F8B1DA736CB1F2BEFCD39521ECCDB927929307A1FAE0B1E60FB39'),
                lambda x: (x[2].hash, '9D004923FA3D31928BFB961E4D84E3A42A1C34F75DC3584EDB6E87520968FDDB'),
                lambda x: (x[3].hash, '5228EA55037FE6B5AFBB25B791194A12F9D7FA99CF3FAE1E6B99A147999B3FD5'),
                lambda x: (x[4].hash, '04628F15E89936912DCA6345D60E668F513D50E7FC6BAF3F1C723C92CFC4FED6'),
            ]
        },
        {
            'name': 'test_get_diagnostic_storage',
            'response': responses.DIAGNOSTIC_STORAGE["Ok"],
            'params': [],
            'method': 'get_diagnostic_storage',
            'validation': [
                lambda x: (isinstance(x, models.BlockchainStorageInfo), True),
                lambda x: (x.num_blocks, 53582),
                lambda x: (x.num_transactions, 25),
                lambda x: (x.num_accounts, 25),
            ]
        },
        {
            'name': 'test_get_merkle_by_hash_in_block',
            'response': responses.BLOCK_TRANSACTION_MERKLE["Ok"],
            'params': [1, '6C274716520ABCDCE0BB799CF6F82B64EBC9B954DBE3B14FD5767CD1A89970BE'],
            'method': 'get_merkle_by_hash_in_block',
            'validation': [
                lambda x: (isinstance(x, models.MerkleProofInfo), True),
                lambda x: (len(x.merkle_path), 6),
                lambda x: (isinstance(x.merkle_path[0], models.MerklePathItem), True),
                lambda x: (x.merkle_path[0].position, 2),
                lambda x: (x.merkle_path[0].hash, 'D41D8437B13EFEBCD9077A325B0604E4FF6691FDE13D6D46B318508EC09B8DA7'),
            ]
        },
        {
            'name': 'test_get_block_receipts',
            'response': responses.BLOCK_RECEIPTS["Ok"],
            'params': [25],
            'method': 'get_block_receipts',
            'validation': [
                lambda x: (isinstance(x, models.Statements), True),
                lambda x: (len(x.transaction_statements), 1),
                lambda x: (len(x.address_resolution_statements), 0),  # TODO: Add statements
                lambda x: (len(x.mosaic_resolution_statements), 0),  # TODO: Add statements
                lambda x: (x.transaction_statements[0].height, 25),
                lambda x: (isinstance(x.transaction_statements[0].source, models.Source), True),
                lambda x: (x.transaction_statements[0].source.primary_id, 0),
                lambda x: (x.transaction_statements[0].source.secondary_id, 0),
                lambda x: (len(x.transaction_statements[0].receipts), 1),
                lambda x: (isinstance(x.transaction_statements[0].receipts[0], models.Receipt), True),
                lambda x: (x.transaction_statements[0].receipts[0].type, models.ReceiptType.VALIDATE_FEE),
                lambda x: (x.transaction_statements[0].receipts[0].version, 1),
                lambda x: (isinstance(x.transaction_statements[0].receipts[0].account, models.PublicAccount), True),
                lambda x: (x.transaction_statements[0].receipts[0].account.public_key, '346E56F77F07B19D48B3AEF969EDB01F68A5AC9FAF8E5E007577D71BA66385FB'),
                lambda x: (isinstance(x.transaction_statements[0].receipts[0].mosaic, models.Mosaic), True),
                lambda x: (x.transaction_statements[0].receipts[0].mosaic.id, models.MosaicId(992621222383397347)),
                lambda x: (x.transaction_statements[0].receipts[0].mosaic.amount, 0),
            ]
        },
        {
            'name': 'test_get_diagnostic_server',
            'response': responses.DIAGNOSTIC_SERVER["Ok"],
            'params': [],
            'method': 'get_diagnostic_server',
            'validation': [
                lambda x: (isinstance(x, models.BlockchainServerInfo), True),
                lambda x: (x.rest_version, '1.0.16'),
                lambda x: (x.sdk_version, '0.7.16'),
            ]
        }
    ],
})
class TestBlockchainHTTP(harness.TestCase):
    pass
