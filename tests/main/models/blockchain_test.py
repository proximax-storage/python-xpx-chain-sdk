import copy

from nem2 import models
from tests.harness import TestCase


class TestBlockInfo(TestCase):

    def setUp(self):
        self.hash = "3A2D7D82D9B7F2C12E1CD549BC0C515A9150698EC0ADBF94121AB5D1730CEAA1"
        self.generation_hash = "80BB92D88ED9908CFD33E85E10DAA716F055C61997BEF3F2F6F711B5F3B66986"
        self.total_fee = 0
        self.num_transactions = 25
        self.signature = "A9BB70EDB0E04A83829F3A32BA0C1361FD8E317243DF748EE00FA8A0E52D4A6793B41752A29FDD10407B1FAC96259AC0D6B489F7CC4ADF960B69103FF51D5A01"
        self.public_key = "7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808"
        self.network_type = models.NetworkType.MIJIN_TEST
        self.signer = models.PublicAccount.create_from_public_key(self.public_key, self.network_type)
        self.version = 36867
        self.type = 32835
        self.height = 1
        self.timestamp = 0
        self.difficulty = 100000000000000
        self.previous_block_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        self.block_transactions_hash = "54B187F7D6B1D45F133F06706566E832A9F325F1E62FE927C0B5C65DAC8A2C56"
        self.merkle_tree = [
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
        ]
        self.block_info = models.BlockInfo(
            hash=self.hash,
            generation_hash=self.generation_hash,
            total_fee=self.total_fee,
            num_transactions=self.num_transactions,
            signature=self.signature,
            signer=self.signer,
            network_type=self.network_type,
            version=self.version,
            type=self.type,
            height=self.height,
            timestamp=self.timestamp,
            difficulty=self.difficulty,
            previous_block_hash=self.previous_block_hash,
            block_transactions_hash=self.block_transactions_hash,
            merkle_tree=self.merkle_tree,
        )

    def test_properties(self):
        self.assertEqual(self.block_info.hash, self.hash)
        self.assertEqual(self.block_info.generation_hash, self.generation_hash)
        self.assertEqual(self.block_info.total_fee, self.total_fee)
        self.assertEqual(self.block_info.num_transactions, self.num_transactions)
        self.assertEqual(self.block_info.signature, self.signature)
        self.assertEqual(self.block_info.signer, self.signer)
        self.assertEqual(self.block_info.network_type, self.network_type)
        self.assertEqual(self.block_info.version, self.version)
        self.assertEqual(self.block_info.type, self.type)
        self.assertEqual(self.block_info.height, self.height)
        self.assertEqual(self.block_info.timestamp, self.timestamp)
        self.assertEqual(self.block_info.difficulty, self.difficulty)
        self.assertEqual(self.block_info.previous_block_hash, self.previous_block_hash)
        self.assertEqual(self.block_info.block_transactions_hash, self.block_transactions_hash)
        self.assertEqual(self.block_info.merkle_tree, self.merkle_tree)

    def test_eq(self):
        bi1 = copy.copy(self.block_info)
        bi2 = copy.copy(bi1)
        bi3 = copy.copy(bi2)
        bi3._num_transactions += 1

        self.assertTrue(bi1 == bi1)
        self.assertTrue(bi1 == bi2)
        self.assertFalse(bi1 == bi3)
        self.assertTrue(bi2 == bi2)
        self.assertFalse(bi2 == bi3)
        self.assertTrue(bi3 == bi3)

    def test_to_dto(self):
        dto = self.block_info.to_dto()
        self.assertIn("merkleTree", dto['meta'])
        self.assertEqual(dto, {
            'meta': {
                'hash': self.hash,
                'generationHash': self.generation_hash,
                'totalFee': [0, 0],
                'numTransactions': self.num_transactions,
                'merkleTree': self.merkle_tree,
            },
            'block': {
                'signature': self.signature,
                'signer': self.public_key,
                'version': self.version,
                'type': self.type,
                'height': [1, 0],
                'timestamp': [0, 0],
                'difficulty': [276447232, 23283],
                'previousBlockHash': self.previous_block_hash,
                'blockTransactionsHash': self.block_transactions_hash,
            },
        })

        self.block_info._merkle_tree = None
        dto = self.block_info.to_dto()
        self.assertNotIn("merkleTree", dto['meta'])

    def test_from_dto(self):
        dto = self.block_info.to_dto()
        self.assertEqual(self.block_info, models.BlockInfo.from_dto(dto))

        self.block_info._merkle_tree = None
        dto = self.block_info.to_dto()
        self.assertEqual(self.block_info, models.BlockInfo.from_dto(dto))


class TestBlockchainScore(TestCase):
    # TODO(ahuszagh) Implement
    pass


class TestBlockchainStorageInfo(TestCase):
    # TODO(ahuszagh) Implement
    pass


class TestNetworkType(TestCase):

    def setUp(self):
        self.main_net = models.NetworkType.MAIN_NET
        self.test_net = models.NetworkType.TEST_NET
        self.mijin = models.NetworkType.MIJIN
        self.mijin_test = models.NetworkType.MIJIN_TEST

    def test_values(self):
        self.assertEqual(self.main_net, 0x68)
        self.assertEqual(self.test_net, 0x98)
        self.assertEqual(self.mijin, 0x60)
        self.assertEqual(self.mijin_test, 0x90)

    def test_description(self):
        self.assertEqual(self.main_net.description(), "Main network")
        self.assertEqual(self.test_net.description(), "Test network")
        self.assertEqual(self.mijin.description(), "Mijin network")
        self.assertEqual(self.mijin_test.description(), "Mijin test network")

    def test_identifier(self):
        self.assertEqual(self.main_net.identifier(), b"N")
        self.assertEqual(self.test_net.identifier(), b"T")
        self.assertEqual(self.mijin.identifier(), b"M")
        self.assertEqual(self.mijin_test.identifier(), b"S")

    def test_create_from_identifier(self):

        def create(address: str):
            return models.NetworkType.create_from_identifier(address)

        self.assertEqual(self.main_net, create(b"N"))
        self.assertEqual(self.test_net, create(b"T"))
        self.assertEqual(self.mijin, create(b"M"))
        self.assertEqual(self.mijin_test, create(b"S"))

        with self.assertRaises(KeyError):
            create(b"F")

    def test_create_from_raw_address(self):

        def create(address: str):
            return models.NetworkType.create_from_raw_address(address)

        self.assertEqual(self.main_net, create("ND5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54"))
        self.assertEqual(self.test_net, create("TD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54"))
        self.assertEqual(self.mijin, create("MD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54"))
        self.assertEqual(self.mijin_test, create("SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54"))

        with self.assertRaises(KeyError):
            create("FD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54")
