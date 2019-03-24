from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


@harness.mocked_http_test_case({
    'clients': (client.BlockchainHTTP, client.AsyncBlockchainHTTP),
    'network_type': models.NetworkType.MIJIN_TEST,
    'tests': [
        {
            'name': 'test_get_block_by_height',
            'response': responses.BLOCK_INFO["Ok"],
            'params': [models.Address('SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM')],
            'method': 'get_block_by_height',
            'validation': [
                lambda x: (x.hash, '3A2D7D82D9B7F2C12E1CD549BC0C515A9150698EC0ADBF94121AB5D1730CEAA1'),
                lambda x: (x.generation_hash, '80BB92D88ED9908CFD33E85E10DAA716F055C61997BEF3F2F6F711B5F3B66986'),
                lambda x: (x.total_fee, 0),
                lambda x: (x.num_transactions, 25),
                lambda x: (x.signature, "A9BB70EDB0E04A83829F3A32BA0C1361FD8E317243DF748EE00FA8A0E52D4A6793B41752A29FDD10407B1FAC96259AC0D6B489F7CC4ADF960B69103FF51D5A01"),
                lambda x: (x.signer.public_key, "7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808"),
                lambda x: (x.network_type, models.NetworkType.MIJIN_TEST),
                lambda x: (x.version, 3),
                lambda x: (x.type, 32835),
                lambda x: (x.height, 1),
                lambda x: (x.timestamp, 0),
                lambda x: (x.difficulty, 100000000000000),
                lambda x: (x.previous_block_hash, "0000000000000000000000000000000000000000000000000000000000000000"),
                lambda x: (x.block_transactions_hash, "54B187F7D6B1D45F133F06706566E832A9F325F1E62FE927C0B5C65DAC8A2C56"),
                lambda x: (x.merkle_tree[0], "smNSI9tFz7tOIc38NZ/n8iKm5fYADJnKnnKdsC5mYfU="),
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
    ],
})
class TestBlockchainHTTP(harness.TestCase):
    pass
