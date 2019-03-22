from nem2 import models
from nem2 import util
from tests import harness


@harness.model_test_case({
    'type': models.BlockInfo,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'hash': '3A2D7D82D9B7F2C12E1CD549BC0C515A9150698EC0ADBF94121AB5D1730CEAA1',
        'generation_hash': '80BB92D88ED9908CFD33E85E10DAA716F055C61997BEF3F2F6F711B5F3B66986',
        'total_fee': 0,
        'num_transactions': 25,
        'signature': 'A9BB70EDB0E04A83829F3A32BA0C1361FD8E317243DF748EE00FA8A0E52D4A6793B41752A29FDD10407B1FAC96259AC0D6B489F7CC4ADF960B69103FF51D5A01',
        'network_type': models.NetworkType.MIJIN_TEST,
        'signer': models.PublicAccount(
            public_key='7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808',
            address=models.Address('SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM'),
        ),
        'version': models.TransactionVersion.TRANSFER,
        'type': models.BlockType.GENESIS,
        'height': 1,
        'timestamp': 0,
        'difficulty': 100000000000000,
        'previous_block_hash': '0000000000000000000000000000000000000000000000000000000000000000',
        'block_transactions_hash': '54B187F7D6B1D45F133F06706566E832A9F325F1E62FE927C0B5C65DAC8A2C56',
        'merkle_tree': [
            'smNSI9tFz7tOIc38NZ/n8iKm5fYADJnKnnKdsC5mYfU=',
            '0wAq1E2aVrhZbQzhXHda/mZS+MxbtwCseUdrH1pTQmY=',
            '7F314nG7XL0T5evPw/pkvJLs1Y8APVEpX8hGakN8Vqo=',
            'DfP+q85s9NdjSnY400nkRZMXAo0Fd0AonTpgieYINX4=',
            'hDMp1kh6NVLHUKGungYALNawXe9vYBbNepIl1aOl5fc=',
            'cp0vfQ50vNIcXCJLYgCECodmNYvNJxS3ntty8INDWBE=',
            '1CTjoLygIYqDwfCR2hZ3GIKxnOdFsuHomLp7K+42lIA=',
            'Fg5TASHe8irhV7Ti9muiCkOXJHyjBnHAtl8k8ryjuTQ=',
            '44dGybx4J7nb7cRHj4SZEkK4ByOqh/N90tdccgnevYg=',
            'aslXDYB1AScnHbVKYLyGT1S7cOnlQ6R9kGiO94N5P8Y=',
            'yKEPn7Y+e5/5hII57vS6C8biw/HBKfjSQFIhWGtwxZQ=',
            'mVwU0/fcPSFe/RNfXLaE9Q6tTmssF+b6218f6UcxB1Y=',
            'u/jxfF6n0kAUTBRgVbfSpzabUsIpEXdZMBWkBNNKp2E=',
            'Ihc3uaPu/VJfaLERgP3BnPQdq+k7+ruMWTdAD2/8euY=',
            'O+kPQFqaR5/QhD/P/QUhUMaLgyOgSLYXmMCOVzOsOV0=',
            'Y5A7AxlEuWUz8W6is+TQmc/X37VsQB4eCFkzhcTwVTA=',
            '4dul0LY1q2RnRfxxd8aIWCcrHsffDiycSGYZdZbM0VI=',
            'yZ8DByioqTEQAsJTZ3NWTXeY3QZhuq2023YufYuQZAI=',
            '+Zl6pcbM+Y4619/YLvVaP/jHq3lk9pVCbIhHR6IMowU=',
            'g9NlCogPuLYqFWtyGOEuoWg0sbJ6+hvST9lhLAOuEy0=',
            'DR9UV+B9i1s3RyGmT2qyotbB9B3oYUWnIh/GzKJJuS0=',
            'HsyC6rNJr0DcVTZXWbiiz4Hew+wAVA9qDQSNfJiS09g=',
            'zastrgvHxx6/cDmNXxVuhtp8iZHEkkGkFNY+Z6gX/Is=',
            'aPK8DQCPH5gNzox4Jiw4qTnf9B6mQgmSBLl+fm3wNhI=',
            'rrDI3kbhAZB8ga5EgAd1sVqsdg0tA7cqLw2ePTCGIRg=',
            'rrDI3kbhAZB8ga5EgAd1sVqsdg0tA7cqLw2ePTCGIRg=',
            'HkOmQAq7Vh21etgkdEBwmmwyzEWtISsSN4PE8KYzjOk=',
            'qCFc1leqvoJS10+WvWSXw5nNrMD0l81+dYyCXtyD3tI=',
            'Q5vurzMaMGFUhNI86kevy3FxNYJxmmOCC5+76o5NE9o=',
            'hiu5WjCZ4hlwCwSYggUITNKcI6jMHrssL3lgTm0/cFM=',
            'l7Ixx1WRLWZSKavafNigjq44XwIyJF+EYllTIjQGWpo=',
            'nwLD6piQ+fKm1rC5Op2T99sV3Yc0b7qZ4IrDKjWkgz8=',
            '9oWJi0OyFs7qG+SpiTTY8RJjltOCMnqQswSdsK/C3iQ=',
            'q4vBxFdO4oFSJCkDGc2xEPOeJ0fc3Z46rNkGMNsVJJ0=',
            'xgondbHJ8OboS5egn2QkmSpTC9s+96y9/H9rthw5eoA=',
            '2zXMQLIZ6PrdfUiL2s6N8T722/iq1IVdMqmD/EGPPMQ=',
            'xykMSurZ42tmuxWUhscA6Al3dQsaTFL5P+kmHscVstY=',
            'pWhN2jX8qTIuX4BIiXp8bnwh922RojG2z2AQkC4rhI4=',
            'Om93dUKeTFPm6nab3+qc+jWecZ4L2tHNLqz2Dee/jg8=',
            'Om93dUKeTFPm6nab3+qc+jWecZ4L2tHNLqz2Dee/jg8=',
            'PwLlJswanhwAc7NwrtfbGkhOVqSdmOdYUKoz+PbjgZM=',
            'eBQd4h/8qL6XpxskGL+LjQAfrQz4MHiSQnKtPCi5Jc8=',
            'mpTQcHi/5eup/V2Kvh3b7ZzTHf/vXpFreqEnnz3qiSQ=',
            'cszQiT3FMzYCT0XCgtpi34mZZk2nYfJseem2kEhlx4M=',
            'O4eeFzXVt6XfVXHSLSMSJzksrSwlsifQEALEDs/ZJQI=',
            'BK6b5AfzAfkRZ3Zy5UCM75cvRA+VoIfP85QBtQ1Sy60=',
            'AJf7pTD6VRSgRsALN3TOnJG7uVYmZPdaWc+hxEj3MD0=',
            'AJf7pTD6VRSgRsALN3TOnJG7uVYmZPdaWc+hxEj3MD0=',
            'okKBsiKgTOK+it2+O+tvjdXncFGuAPUOuN8d+OJZNbQ=',
            '3OO/l7J0CguQhKtUclUNbcpwhNgMA4k1cCskucprGho=',
            '1IXe1OxirevzjvS8h47QTNOkYPYm+V3SZWbtva1+gKk=',
            '0q+A8Sjo4MkWFgfxrJjkcMPqOELKoMois363ViFicQM=',
            '3+cU5i7aN7gS5c7IPom9ABMfloevx6/ebk8hdJbIfJk=',
            'f/KJxlcSk0j1+5r/TbMKNbcDHaOVZbcXKUtbCv9RpCU=',
            'VLGH99ax1F8TPwZwZWboMqnzJfHmL+knwLXGXayKLFY='
        ],
    },
    'dto': {
        'meta': {
            'hash': '3A2D7D82D9B7F2C12E1CD549BC0C515A9150698EC0ADBF94121AB5D1730CEAA1',
            'generationHash': '80BB92D88ED9908CFD33E85E10DAA716F055C61997BEF3F2F6F711B5F3B66986',
            'totalFee': [0, 0],
            'numTransactions': 25,
            'merkleTree': [
                'smNSI9tFz7tOIc38NZ/n8iKm5fYADJnKnnKdsC5mYfU=',
                '0wAq1E2aVrhZbQzhXHda/mZS+MxbtwCseUdrH1pTQmY=',
                '7F314nG7XL0T5evPw/pkvJLs1Y8APVEpX8hGakN8Vqo=',
                'DfP+q85s9NdjSnY400nkRZMXAo0Fd0AonTpgieYINX4=',
                'hDMp1kh6NVLHUKGungYALNawXe9vYBbNepIl1aOl5fc=',
                'cp0vfQ50vNIcXCJLYgCECodmNYvNJxS3ntty8INDWBE=',
                '1CTjoLygIYqDwfCR2hZ3GIKxnOdFsuHomLp7K+42lIA=',
                'Fg5TASHe8irhV7Ti9muiCkOXJHyjBnHAtl8k8ryjuTQ=',
                '44dGybx4J7nb7cRHj4SZEkK4ByOqh/N90tdccgnevYg=',
                'aslXDYB1AScnHbVKYLyGT1S7cOnlQ6R9kGiO94N5P8Y=',
                'yKEPn7Y+e5/5hII57vS6C8biw/HBKfjSQFIhWGtwxZQ=',
                'mVwU0/fcPSFe/RNfXLaE9Q6tTmssF+b6218f6UcxB1Y=',
                'u/jxfF6n0kAUTBRgVbfSpzabUsIpEXdZMBWkBNNKp2E=',
                'Ihc3uaPu/VJfaLERgP3BnPQdq+k7+ruMWTdAD2/8euY=',
                'O+kPQFqaR5/QhD/P/QUhUMaLgyOgSLYXmMCOVzOsOV0=',
                'Y5A7AxlEuWUz8W6is+TQmc/X37VsQB4eCFkzhcTwVTA=',
                '4dul0LY1q2RnRfxxd8aIWCcrHsffDiycSGYZdZbM0VI=',
                'yZ8DByioqTEQAsJTZ3NWTXeY3QZhuq2023YufYuQZAI=',
                '+Zl6pcbM+Y4619/YLvVaP/jHq3lk9pVCbIhHR6IMowU=',
                'g9NlCogPuLYqFWtyGOEuoWg0sbJ6+hvST9lhLAOuEy0=',
                'DR9UV+B9i1s3RyGmT2qyotbB9B3oYUWnIh/GzKJJuS0=',
                'HsyC6rNJr0DcVTZXWbiiz4Hew+wAVA9qDQSNfJiS09g=',
                'zastrgvHxx6/cDmNXxVuhtp8iZHEkkGkFNY+Z6gX/Is=',
                'aPK8DQCPH5gNzox4Jiw4qTnf9B6mQgmSBLl+fm3wNhI=',
                'rrDI3kbhAZB8ga5EgAd1sVqsdg0tA7cqLw2ePTCGIRg=',
                'rrDI3kbhAZB8ga5EgAd1sVqsdg0tA7cqLw2ePTCGIRg=',
                'HkOmQAq7Vh21etgkdEBwmmwyzEWtISsSN4PE8KYzjOk=',
                'qCFc1leqvoJS10+WvWSXw5nNrMD0l81+dYyCXtyD3tI=',
                'Q5vurzMaMGFUhNI86kevy3FxNYJxmmOCC5+76o5NE9o=',
                'hiu5WjCZ4hlwCwSYggUITNKcI6jMHrssL3lgTm0/cFM=',
                'l7Ixx1WRLWZSKavafNigjq44XwIyJF+EYllTIjQGWpo=',
                'nwLD6piQ+fKm1rC5Op2T99sV3Yc0b7qZ4IrDKjWkgz8=',
                '9oWJi0OyFs7qG+SpiTTY8RJjltOCMnqQswSdsK/C3iQ=',
                'q4vBxFdO4oFSJCkDGc2xEPOeJ0fc3Z46rNkGMNsVJJ0=',
                'xgondbHJ8OboS5egn2QkmSpTC9s+96y9/H9rthw5eoA=',
                '2zXMQLIZ6PrdfUiL2s6N8T722/iq1IVdMqmD/EGPPMQ=',
                'xykMSurZ42tmuxWUhscA6Al3dQsaTFL5P+kmHscVstY=',
                'pWhN2jX8qTIuX4BIiXp8bnwh922RojG2z2AQkC4rhI4=',
                'Om93dUKeTFPm6nab3+qc+jWecZ4L2tHNLqz2Dee/jg8=',
                'Om93dUKeTFPm6nab3+qc+jWecZ4L2tHNLqz2Dee/jg8=',
                'PwLlJswanhwAc7NwrtfbGkhOVqSdmOdYUKoz+PbjgZM=',
                'eBQd4h/8qL6XpxskGL+LjQAfrQz4MHiSQnKtPCi5Jc8=',
                'mpTQcHi/5eup/V2Kvh3b7ZzTHf/vXpFreqEnnz3qiSQ=',
                'cszQiT3FMzYCT0XCgtpi34mZZk2nYfJseem2kEhlx4M=',
                'O4eeFzXVt6XfVXHSLSMSJzksrSwlsifQEALEDs/ZJQI=',
                'BK6b5AfzAfkRZ3Zy5UCM75cvRA+VoIfP85QBtQ1Sy60=',
                'AJf7pTD6VRSgRsALN3TOnJG7uVYmZPdaWc+hxEj3MD0=',
                'AJf7pTD6VRSgRsALN3TOnJG7uVYmZPdaWc+hxEj3MD0=',
                'okKBsiKgTOK+it2+O+tvjdXncFGuAPUOuN8d+OJZNbQ=',
                '3OO/l7J0CguQhKtUclUNbcpwhNgMA4k1cCskucprGho=',
                '1IXe1OxirevzjvS8h47QTNOkYPYm+V3SZWbtva1+gKk=',
                '0q+A8Sjo4MkWFgfxrJjkcMPqOELKoMois363ViFicQM=',
                '3+cU5i7aN7gS5c7IPom9ABMfloevx6/ebk8hdJbIfJk=',
                'f/KJxlcSk0j1+5r/TbMKNbcDHaOVZbcXKUtbCv9RpCU=',
                'VLGH99ax1F8TPwZwZWboMqnzJfHmL+knwLXGXayKLFY='
            ],
        },
        'block': {
            'signature': 'A9BB70EDB0E04A83829F3A32BA0C1361FD8E317243DF748EE00FA8A0E52D4A6793B41752A29FDD10407B1FAC96259AC0D6B489F7CC4ADF960B69103FF51D5A01',
            'signer': '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808',
            'version': 36867,
            'type': 0x8043,
            'height': [1, 0],
            'timestamp': [0, 0],
            'difficulty': [276447232, 23283],
            'previousBlockHash': '0000000000000000000000000000000000000000000000000000000000000000',
            'blockTransactionsHash': '54B187F7D6B1D45F133F06706566E832A9F325F1E62FE927C0B5C65DAC8A2C56',
        },
    },
})
class TestBlockInfo(harness.TestCase):

    def test_treeless(self):
        block_info = self.model.replace(merkle_tree=None)
        dto = self.dto.copy()
        del dto['meta']['merkleTree']

        self.assertEqual(dto, block_info.to_dto(self.network_type))
        self.assertEqual(block_info, self.type.from_dto(dto, self.network_type))



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
        0x68,
        0x98,
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
        0x68,
        0x98,
        0x60,
        0x90,
    ],
    'catbuffer': [
        b'h',
        b'\x98',
        b'`',
        b'\x90',
    ],
    'custom': [
        {
            'name': 'test_identifier',
            'callback': lambda self, x: x.identifier(),
            'results': [b'N', B'T', b'M', b'S'],
        },
        {
            'name': 'test_create_from_identifier',
            'callback': lambda self, x: self.type.create_from_identifier(x),
            'inputs': [b'N', b'T', b'M', b'S'],
        },
        {
            'name': 'test_create_from_raw_address',
            'callback': lambda self, x: self.type.create_from_raw_address(x),
            'inputs': [
                'ND5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54',
                'TD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54',
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
