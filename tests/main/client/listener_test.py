from nem2 import models
from tests import harness

BLOCK_VALIDATOR = [
    lambda x: (x.channel_name, 'block'),
    lambda x: (isinstance(x.message, models.BlockInfo), True),
    lambda x: (x.message.height >= 1, True),
]


@harness.mocked_listener_test_case({
    'tests': [
        {
            'name': 'test_new_block',
            'uid': 'A7Z3K5CZ3WMPMCI2IKHRCPWDHGJAYR76',
            'subscriptions': ['new_block'],
            'response': [
                '{"meta": {"hash": "04628F15E89936912DCA6345D60E668F513D50E7FC6BAF3F1C723C92CFC4FED6", "generationHash": "7CCDF81A60B0A03A3B30D715C5C7513916319C09215E22C67B0A81106FB21445", "totalFee": [0, 0], "subCacheMerkleRoots": [], "numTransactions": 31}, "block": {"signature": "82D8C518BF32CA9A8478451F79B7EEC69F11E6022AF7230CE21F230A09E51A0CEB169454CB4AD4499BC9C0769B468AB5A6DD716D00C977F16BF63DD1B0653305", "signer": "A04335F99D9EE3787528A16C7A302F80D511E9CF71D97D95C2182E0EA75A1EF9", "version": 2415919107, "type": 32835, "height": [1, 0], "timestamp": [0, 0], "difficulty": [276447232, 23283], "feeMultiplier": 0, "previousBlockHash": "0000000000000000000000000000000000000000000000000000000000000000", "blockTransactionsHash": "36822DF1CF1827915A8CDDF8A47EBBF1D1C55666DB1E8AC942C447D3D0E6D494", "blockReceiptsHash": "RMViDPTpgKd072qPgxmPVoabWcrmFs5v5EGS00GxiX0=", "stateHash": "C61C28E078298D6A508A649637EAC7D9D1E5F3813856EF9B7F1579866ACB570E", "beneficiaryPublicKey": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="}}',
                '{"meta": {"hash": "5228EA55037FE6B5AFBB25B791194A12F9D7FA99CF3FAE1E6B99A147999B3FD5", "generationHash": "662D0F2609835C5010081792400F78C67828A7CB21FC4E814B54278D8C672CAB", "totalFee": [0, 0], "subCacheMerkleRoots": ["796159C97C02FB6F38BB7C07F9F367A5E7362090D4FDA34739979A6647E127D3", "D54C1ED47A4585CA35AB57D8F5FE0C83A7DDBC401B2967C636977E70C3BC5A62", "AAFCC40F74636DCCDFE5EABD7FD7BEC5C0C960606E6FFD3BA2515603C4D11272", "0000000000000000000000000000000000000000000000000000000000000000", "0000000000000000000000000000000000000000000000000000000000000000", "0000000000000000000000000000000000000000000000000000000000000000", "0000000000000000000000000000000000000000000000000000000000000000"], "numTransactions": 0, "numStatements": 1}, "block": {"signature": "6043A1428BF3D492372393216F038385D240C7079CB579279B9B115E12287B572473D906604EDFBBD7F8AD0DDEE463D49CED58A5501C5E9F841635952E796B0C", "signer": "02B7BA49413A98C81C04B7CCB0C70177C5B9C0FB3452A3FF1C8EBDAEB06C85F3", "version": 2415919107, "type": 33091, "height": [2, 0], "timestamp": [2160665726, 22], "difficulty": [276447232, 23283], "feeMultiplier": 0, "previousBlockHash": "04628F15E89936912DCA6345D60E668F513D50E7FC6BAF3F1C723C92CFC4FED6", "blockTransactionsHash": "0000000000000000000000000000000000000000000000000000000000000000", "blockReceiptsHash": "jN2g4AQXQRB16MeneQZS2Mqocz971Jm1PxDc4+yUOj8=", "stateHash": "140E064D15B543FFBFE5B0046904430BF3C7F6C33964318F842343455D7E86F2", "beneficiaryPublicKey": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="}}',
                '{"meta": {"hash": "9D004923FA3D31928BFB961E4D84E3A42A1C34F75DC3584EDB6E87520968FDDB", "generationHash": "BC9D08EB944AC8474F2FC56CCD8D81E69280D01DD6ADDB32F3F1A02BE20640A9", "totalFee": [0, 0], "subCacheMerkleRoots": ["796159C97C02FB6F38BB7C07F9F367A5E7362090D4FDA34739979A6647E127D3", "D54C1ED47A4585CA35AB57D8F5FE0C83A7DDBC401B2967C636977E70C3BC5A62", "AAFCC40F74636DCCDFE5EABD7FD7BEC5C0C960606E6FFD3BA2515603C4D11272", "0000000000000000000000000000000000000000000000000000000000000000", "0000000000000000000000000000000000000000000000000000000000000000", "0000000000000000000000000000000000000000000000000000000000000000", "0000000000000000000000000000000000000000000000000000000000000000"], "numTransactions": 0, "numStatements": 1}, "block": {"signature": "B72210D77938A496BE2E70BE5AED709A5817C01D40E8DE4F9846302DA3A673CD48495E0AB933180567244DDAFFD3DA3251BC77FC66CA629841E472AC866DC20E", "signer": "02B7BA49413A98C81C04B7CCB0C70177C5B9C0FB3452A3FF1C8EBDAEB06C85F3", "version": 2415919107, "type": 33091, "height": [3, 0], "timestamp": [2160682747, 22], "difficulty": [3913347072, 22118], "feeMultiplier": 0, "previousBlockHash": "5228EA55037FE6B5AFBB25B791194A12F9D7FA99CF3FAE1E6B99A147999B3FD5", "blockTransactionsHash": "0000000000000000000000000000000000000000000000000000000000000000", "blockReceiptsHash": "jN2g4AQXQRB16MeneQZS2Mqocz971Jm1PxDc4+yUOj8=", "stateHash": "140E064D15B543FFBFE5B0046904430BF3C7F6C33964318F842343455D7E86F2", "beneficiaryPublicKey": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="}}',
                '{"meta": {"hash": "DF7539D4AC9F8B1DA736CB1F2BEFCD39521ECCDB927929307A1FAE0B1E60FB39", "generationHash": "6FEE2FD34A9AD542213289A5FC9383B990B283C87D289383462920E998B33A76", "totalFee": [0, 0], "subCacheMerkleRoots": ["796159C97C02FB6F38BB7C07F9F367A5E7362090D4FDA34739979A6647E127D3", "D54C1ED47A4585CA35AB57D8F5FE0C83A7DDBC401B2967C636977E70C3BC5A62", "AAFCC40F74636DCCDFE5EABD7FD7BEC5C0C960606E6FFD3BA2515603C4D11272", "0000000000000000000000000000000000000000000000000000000000000000", "0000000000000000000000000000000000000000000000000000000000000000", "0000000000000000000000000000000000000000000000000000000000000000", "0000000000000000000000000000000000000000000000000000000000000000"], "numTransactions": 0, "numStatements": 1}, "block": {"signature": "9F260A352607AE698A4B0BA8329B2FE75D5D2D70FF519DEE071B7CA8859D6AB57B34643DB587DFB3DACA66CB0D2ABB39EE515649509129AC42A189DBA8B90508", "signer": "02B7BA49413A98C81C04B7CCB0C70177C5B9C0FB3452A3FF1C8EBDAEB06C85F3", "version": 2415919107, "type": 33091, "height": [4, 0], "timestamp": [2160703757, 22], "difficulty": [4147176448, 21012], "feeMultiplier": 0, "previousBlockHash": "9D004923FA3D31928BFB961E4D84E3A42A1C34F75DC3584EDB6E87520968FDDB", "blockTransactionsHash": "0000000000000000000000000000000000000000000000000000000000000000", "blockReceiptsHash": "jN2g4AQXQRB16MeneQZS2Mqocz971Jm1PxDc4+yUOj8=", "stateHash": "140E064D15B543FFBFE5B0046904430BF3C7F6C33964318F842343455D7E86F2", "beneficiaryPublicKey": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="}}',
                '{"meta": {"hash": "22A2B807BF395CC9432DB4075B8A6D412EF7FD0892D266959D02D942C0F48576", "generationHash": "FA2885CDDFBEB4FDBC902CEC4B12C8EAA61AF2890CFC16B53B69CB8AD2A2D6E8", "totalFee": [0, 0], "subCacheMerkleRoots": ["796159C97C02FB6F38BB7C07F9F367A5E7362090D4FDA34739979A6647E127D3", "D54C1ED47A4585CA35AB57D8F5FE0C83A7DDBC401B2967C636977E70C3BC5A62", "AAFCC40F74636DCCDFE5EABD7FD7BEC5C0C960606E6FFD3BA2515603C4D11272", "0000000000000000000000000000000000000000000000000000000000000000", "0000000000000000000000000000000000000000000000000000000000000000", "0000000000000000000000000000000000000000000000000000000000000000", "0000000000000000000000000000000000000000000000000000000000000000"], "numTransactions": 0, "numStatements": 1}, "block": {"signature": "E645AF61B7386FEAD48655B01EB716D7A1E7CF014F97FE5DF5005EB8AE4350182FAF9C4134071278D8F51EC61829D9131C6C56B869539D8B8D0693F7124FFD0F", "signer": "02B7BA49413A98C81C04B7CCB0C70177C5B9C0FB3452A3FF1C8EBDAEB06C85F3", "version": 2415919107, "type": 33091, "height": [5, 0], "timestamp": [2160711765, 22], "difficulty": [1362837248, 19962], "feeMultiplier": 0, "previousBlockHash": "DF7539D4AC9F8B1DA736CB1F2BEFCD39521ECCDB927929307A1FAE0B1E60FB39", "blockTransactionsHash": "0000000000000000000000000000000000000000000000000000000000000000", "blockReceiptsHash": "jN2g4AQXQRB16MeneQZS2Mqocz971Jm1PxDc4+yUOj8=", "stateHash": "140E064D15B543FFBFE5B0046904430BF3C7F6C33964318F842343455D7E86F2", "beneficiaryPublicKey": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="}}',
            ],
            'validation': [BLOCK_VALIDATOR * 5],
        },
    ],
})
class TestListener(harness.TestCase):
    pass
