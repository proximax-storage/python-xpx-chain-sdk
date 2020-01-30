from xpxchain import models
from tests import harness


@harness.model_test_case({
    'type': models.BlockInfo,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'hash': '04628F15E89936912DCA6345D60E668F513D50E7FC6BAF3F1C723C92CFC4FED6',
        'generation_hash': '7CCDF81A60B0A03A3B30D715C5C7513916319C09215E22C67B0A81106FB21445',
        'total_fee': 0,
        'num_transactions': 31,
        'num_statements': 0,
        'signature': '82D8C518BF32CA9A8478451F79B7EEC69F11E6022AF7230CE21F230A09E51A0CEB169454CB4AD4499BC9C0769B468AB5A6DD716D00C977F16BF63DD1B0653305',
        'network_type': models.NetworkType.MIJIN_TEST,
        'signer': models.PublicAccount(
            public_key='A04335F99D9EE3787528A16C7A302F80D511E9CF71D97D95C2182E0EA75A1EF9',
            address=models.Address('SAHCS4U27RLSCD7N6XWR4KV2M4VEQY2OCXMEZN3H'),
        ),
        'version': models.TransactionVersion.TRANSFER,
        'type': models.BlockType.GENESIS,
        'height': 1,
        'timestamp': 0,
        'difficulty': 100000000000000,
        'fee_multiplier': 0,
        'previous_block_hash': '0000000000000000000000000000000000000000000000000000000000000000',
        'block_transactions_hash': '36822DF1CF1827915A8CDDF8A47EBBF1D1C55666DB1E8AC942C447D3D0E6D494',
        'block_receipts_hash': 'RMViDPTpgKd072qPgxmPVoabWcrmFs5v5EGS00GxiX0=',
        'state_hash': 'C61C28E078298D6A508A649637EAC7D9D1E5F3813856EF9B7F1579866ACB570E',
        'fee_interest': 0,
        'fee_interest_denominator': 0,
    },
    'dto': {
        'meta': {
            'hash': '04628F15E89936912DCA6345D60E668F513D50E7FC6BAF3F1C723C92CFC4FED6',
            'generationHash': '7CCDF81A60B0A03A3B30D715C5C7513916319C09215E22C67B0A81106FB21445',
            'subCacheMerkleRoots': [],
            'totalFee': [0, 0],
            'numTransactions': 31,
            'numStatements': 0,
        },
        'block': {
            'signature': '82D8C518BF32CA9A8478451F79B7EEC69F11E6022AF7230CE21F230A09E51A0CEB169454CB4AD4499BC9C0769B468AB5A6DD716D00C977F16BF63DD1B0653305',
            'signer': 'A04335F99D9EE3787528A16C7A302F80D511E9CF71D97D95C2182E0EA75A1EF9',
            'version': 2415919107,
            'type': 0x8043,
            'height': [1, 0],
            'timestamp': [0, 0],
            'difficulty': [276447232, 23283],
            'feeMultiplier': 0,
            'previousBlockHash': '0000000000000000000000000000000000000000000000000000000000000000',
            'blockTransactionsHash': '36822DF1CF1827915A8CDDF8A47EBBF1D1C55666DB1E8AC942C447D3D0E6D494',
            'blockReceiptsHash': 'RMViDPTpgKd072qPgxmPVoabWcrmFs5v5EGS00GxiX0=',
            'stateHash': 'C61C28E078298D6A508A649637EAC7D9D1E5F3813856EF9B7F1579866ACB570E',
            'feeInterest': 0,
            'feeInterestDenominator': 0
        },
    },
})
class TestBlockInfo(harness.TestCase):

    def test_with_tree(self):
        merkle_tree = [
            "796159C97C02FB6F38BB7C07F9F367A5E7362090D4FDA34739979A6647E127D3",
            "D54C1ED47A4585CA35AB57D8F5FE0C83A7DDBC401B2967C636977E70C3BC5A62",
            "AAFCC40F74636DCCDFE5EABD7FD7BEC5C0C960606E6FFD3BA2515603C4D11272",
            "0000000000000000000000000000000000000000000000000000000000000000",
            "0000000000000000000000000000000000000000000000000000000000000000",
            "0000000000000000000000000000000000000000000000000000000000000000",
            "0000000000000000000000000000000000000000000000000000000000000000"
        ]
        block_info = self.model.replace(merkle_tree=merkle_tree)
        dto = self.dto.copy()
        dto['meta']['subCacheMerkleRoots'] = merkle_tree

        self.assertEqual(dto, block_info.to_dto(self.network_type))
        self.assertEqual(block_info, self.type.create_from_dto(dto, self.network_type))


@harness.enum_test_case({
    'type': models.BlockType,
    'enums': [
        models.BlockType.GENESIS,
        models.BlockType.NEMESIS,
        models.BlockType.REGULAR,
    ],
    'values': [
        0x8043,
        0x8043,
        0x8143,
    ],
    'descriptions': [
        'Genesis',
        'Genesis',
        'Regular',
    ],
    'dto': [
        0x8043,
        0x8043,
        0x8143,
    ],
    'catbuffer': [
        b'C\x80',
        b'C\x80',
        b'C\x81',
    ],
})
class TestBlockType(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.BlockchainScore,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'score': 554597137692201874146690593473,
    },
    'dto': {
        'scoreLow': [2781082305, 27425266],
        'scoreHigh': [5, 7],
    },
})
class TestBlockchainScore(harness.TestCase):

    def test_properties(self):
        self.assertEqual(self.model.score_low, 117790623335183041)
        self.assertEqual(self.model.score_high, 30064771077)


@harness.model_test_case({
    'type': models.BlockchainStorageInfo,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'num_blocks': 11459,
        'num_transactions': 25,
        'num_accounts': 25,
    },
    'dto': {
        'numBlocks': 11459,
        'numTransactions': 25,
        'numAccounts': 25,
    },
})
class TestBlockchainStorageInfo(harness.TestCase):
    pass


@harness.enum_test_case({
    'type': models.NetworkType,
    'enums': [
        models.NetworkType.MAIN_NET,
        models.NetworkType.TEST_NET,
        models.NetworkType.MIJIN,
        models.NetworkType.MIJIN_TEST,
    ],
    'values': [
        0xb8,
        0xa8,
        0x60,
        0x90,
    ],
    'descriptions': [
        "Main network",
        "Test network",
        "Mijin network",
        "Mijin test network",
    ],
    'dto': [
        0xb8,
        0xa8,
        0x60,
        0x90,
    ],
    'catbuffer': [
        b'\xb8',
        b'\xa8',
        b'\x60',
        b'\x90',
    ],
    'custom': [
        {
            'name': 'test_identifier',
            'callback': lambda self, x: x.identifier(),
            'results': [b'X', B'V', b'M', b'S'],
        },
        {
            'name': 'test_create_from_identifier',
            'callback': lambda self, x: self.type.create_from_identifier(x),
            'inputs': [b'X', b'V', b'M', b'S'],
        },
        {
            'name': 'test_create_from_raw_address',
            'callback': lambda self, x: self.type.create_from_raw_address(x),
            'inputs': [
                'XD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54',
                'VD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54',
                'MD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54',
                'SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54',
            ],
        },
        {
            'name': 'test_create_from_invalid_identifier',
            'callback': lambda self, x: self.type.create_from_identifier(x),
            'inputs': [b'F'],
            'results': [KeyError],
        },
        {
            'name': 'test_create_from_invalid_raw_address',
            'callback': lambda self, x: self.type.create_from_raw_address(x),
            'inputs': ['FD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54'],
            'results': [KeyError],
        },
    ],
})
class TestNetworkType(harness.TestCase):
    pass
