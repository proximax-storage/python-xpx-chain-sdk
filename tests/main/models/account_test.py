from xpxchain import models
from xpxchain import util
from tests import harness


@harness.model_test_case({
    'type': models.Account,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'address': models.Address('SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG'),
        'public_key': '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
        'private_key': '97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca',
    },
})
class TestAccount(harness.TestCase):

    def test_properties(self):
        public_account = models.PublicAccount(self.model.address, self.model.public_key)
        self.assertEqual(self.model.network_type, self.network_type)
        self.assertEqual(self.model.public_account, public_account)

    @harness.ignore_warnings_test
    def test_create_from_private_key(self):
        value = self.type.create_from_private_key(self.data['private_key'], self.network_type)
        self.assertEqual(value, self.model)

    @harness.ignore_warnings_test
    def test_generate_new_account(self):
        def fake_entropy(size: int) -> bytes:
            return b'0' * size

        # try the random version
        value = self.type.generate_new_account(self.network_type)
        message = b'Hello World!'
        signature = value.sign_data(message)
        self.assertTrue(value.public_account.verify_signature(message, signature))

        # try with a deterministic version
        value = self.type.generate_new_account(self.network_type, fake_entropy)
        self.assertEqual(value.address.address, 'SA4PGCTZHFCTC5WHYSZCEJZPOO3X7OFBAHCMSL4U')
        self.assertEqual(value.public_key, 'dcedb3902b8fa33f8ced2c9ea62497ae4f43e8208cdedaf4d7cac50abc53ddac')
        self.assertEqual(value.private_key, '3030303030303030303030303030303030303030303030303030303030303030')
        signature = util.hexlify(value.sign_data(message))
        self.assertEqual(signature, 'bbe720fa06fe26f79896f5880baf7e8d112d796c648c56414e2079349baff54c5d46ab08115fad1865de2288a1eeecfaedc3143df14fc81841aec17fa8cba70e')
        self.assertTrue(value.public_account.verify_signature(message, signature))

    @harness.ignore_warnings_test
    def test_sign(self):
        transaction = 'bb000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        signed = util.hexlify(self.model.sign(transaction, '7B631D803F912B00DC0CBED3014BBD17A302BA50B99D233B9C2D9533B842ABDF'))
        self.assertEqual(signed, 'bb000000111f1e4ca0f97a1020e9339e9c21dddddd231a48c28d0b3eade6c9567d6092ee9a36490c2ea6482cd7cef7c4f07d49e5ba33d4b278bd4ff95e56e916f448890a1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7')

    @harness.ignore_warnings_test
    def test_sign_data(self):
        message = b'Hello World!'
        signature = util.hexlify(self.model.sign_data(message))
        self.assertEqual(signature, '40af0cb5a7a7533f07a4ba6f1cb2df64f2347feb1b2eaabb9374d28603d146497ea83d3d6ee15758d39c298b48f58e578cc42f36a373e15eef7412e0bd19a801')

    @harness.ignore_warnings_test
    def test_verify_signature(self):
        message = b'Hello World!'
        signature = '40af0cb5a7a7533f07a4ba6f1cb2df64f2347feb1b2eaabb9374d28603d146497ea83d3d6ee15758d39c298b48f58e578cc42f36a373e15eef7412e0bd19a801'
        self.assertTrue(self.model.verify_signature(message, signature))

    @harness.ignore_warnings_test
    def test_verify_transaction(self):
        payload = 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.assertTrue(self.model.verify_transaction(payload))

    def test_invalid_keys(self):
        with self.assertRaises(ValueError):
            self.type(self.data['address'], self.data['public_key'], '')
        with self.assertRaises(ValueError):
            self.type(self.data['address'], '', self.data['private_key'])


@harness.model_test_case({
    'type': models.AccountInfo,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        # 'meta': models.AccountMeta(1, '40af0cb5a7a7533f07a4ba6f1cb2df64f2347feb1b2eaabb93', '74d28603d146497ea83d3d6ee15758d39c298b48f58', 1, 'e578'),
        'meta': models.AccountMeta(),
        'address': models.Address('SCBO3CAFOVAOGYBAHQKPUOGLAYWFLNJUFFCH3RYY'),
        'address_height': 1,
        'public_key': '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808',
        'public_key_height': 1,
        'mosaics': [],
        'account_type': 0,
        'linked_account_key': '',
        'snapshots': [],
    },
    'dto': {
        'meta': {
            # 'height': [1, 0],
            # 'hash': '40af0cb5a7a7533f07a4ba6f1cb2df64f2347feb1b2eaabb93',
            # 'merkleComponentHash': '74d28603d146497ea83d3d6ee15758d39c298b48f58',
            # 'index': 1,
            # 'id': 'e578',
        },
        'account': {
            'address': '9082ed88057540e360203c14fa38cb062c55b53429447dc718',
            'addressHeight': [1, 0],
            'publicKey': '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808',
            'publicKeyHeight': [1, 0],
            'mosaics': [],
            'accountType': 0,
            'linkedAccountKey': '',
            'snapshots': [],
        },
    }
})
class TestAccountInfo(harness.TestCase):

    def test_properties(self):
        public_account = models.PublicAccount(self.model.address, self.model.public_key)
        self.assertEqual(self.model.public_account, public_account)


@harness.model_test_case({
    'type': models.AccountMeta,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        # 'height': 1,
        # 'hash': '40af0cb5a7a7533f07a4ba6f1cb2df64f2347feb1b2eaabb93',
        # 'merkle_component_hash': '74d28603d146497ea83d3d6ee15758d39c298b48f58',
        # 'index': 1,
        # 'id': 'e578',
    },
    'dto': {
        # 'height': [1, 0],
        # 'hash': '40af0cb5a7a7533f07a4ba6f1cb2df64f2347feb1b2eaabb93',
        # 'merkleComponentHash': '74d28603d146497ea83d3d6ee15758d39c298b48f58',
        # 'index': 1,
        # 'id': 'e578',
    },
    'eq': False,
})
class TestAccountMeta(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.AccountProperty,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'property_type': models.PropertyType.ALLOW_ADDRESS,
        'values': [
            models.Address('SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG'),
            models.Address('SCBO3CAFOVAOGYBAHQKPUOGLAYWFLNJUFFCH3RYY'),
        ],
    },
    'dto': {
        'propertyType': 0x01,
        'values': [
            '902891202271567A65166877A647D8A5FFD3BBE630AB925E46',
            '9082ED88057540E360203C14FA38CB062C55B53429447DC718',
        ],
    },
})
class TestAccountProperty(harness.TestCase):
    # TODO(ahuszagh) Check when stabilized.
    pass

    # TODO(ahuszagh)
    #   Need to test a lot of other variants.
    #       Mosaic
    #       Transaction
    #       Ensure the address is correct.


@harness.model_test_case({
    'type': models.AccountProperties,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'address': models.Address('SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG'),
        'properties': [
            models.AccountProperty(models.PropertyType.ALLOW_ADDRESS, []),
        ],
    },
    'dto': {
        'accountProperties': {
            'address': '902891202271567A65166877A647D8A5FFD3BBE630AB925E46',
            'properties': [
                {
                    'propertyType': 0x01,
                    'values': [],
                },
            ],
        }
    },
})
class TestAccountProperties(harness.TestCase):
    # TODO(ahuszagh) Check when stabilized.
    pass


@harness.model_test_case({
    'type': models.Address,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'address': 'SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54',
    },
    'extras': {
        'plain': 'SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54',
        'pretty': 'SD5DT3-CH4BLA-BL5HIM-EKP2TA-PUKF4N-Y3L5HR-IR54',
        'encoded': b'\x90\xfa9\xecG\xe0V\x00\xaf\xa7C\x08\xa7\xea`}\x14^7\x1b_O\x14G\xbc',
        'public_key': '7D08373CFFE4154E129E04F0827E5F3D6907587E348757B0F87D2F839BF88246',
        'invalid': 'SD5DT3-CH4BLA-BL5HIM-EKP2TA-PUKF4N-Y3L5HR-IR55'
    }
})
class TestAddress(harness.TestCase):

    def test_properties(self):
        self.assertEqual(self.model.network_type, self.network_type)
        self.assertEqual(self.model.encoded, self.extras['encoded'])

    def test_create_from_raw_address(self):
        self.assertEqual(self.model, self.type.create_from_raw_address(self.extras['pretty']))

    def test_create_from_encoded(self):
        self.assertEqual(self.model, self.type.create_from_encoded(self.extras['encoded']))

    def test_create_from_public_key(self):
        public_key = self.extras['public_key']

        value = self.type.create_from_public_key(public_key, models.NetworkType.MAIN_NET)
        self.assertEqual(value.address, 'XD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L4X2EMBY')

        value = self.type.create_from_public_key(public_key, models.NetworkType.TEST_NET)
        self.assertEqual(value.address, 'VD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L4UGKOZU')

        value = self.type.create_from_public_key(public_key, models.NetworkType.MIJIN)
        self.assertEqual(value.address, 'MD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L4R2R2JH')

        value = self.type.create_from_public_key(public_key, models.NetworkType.MIJIN_TEST)
        self.assertEqual(value.address, 'SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54')

    def test_plain(self):
        self.assertEqual(self.model.plain(), self.extras['plain'])

    def test_pretty(self):
        self.assertEqual(self.model.pretty(), self.extras['pretty'])

    def test_is_valid(self):
        self.assertTrue(self.type.create_from_raw_address(self.extras['plain']).is_valid())
        self.assertTrue(self.type.create_from_raw_address(self.extras['pretty']).is_valid())
        self.assertFalse(self.type.create_from_raw_address(self.extras['invalid']).is_valid())

    def test_invalid_address(self):
        with self.assertRaises(ValueError):
            self.type('')
        with self.assertRaises(ValueError):
            self.type.create_from_encoded('')
        with self.assertRaises(ValueError):
            self.type.create_from_public_key('', self.network_type)


@harness.model_test_case({
    'type': models.MultisigAccountGraphInfo,
    'network_type': models.NetworkType.MIJIN_TEST,
    # Not a dataclass, has no fields or replace methods.
    'fields': False,
    'replace': False,
    'data': {
        0: [
            models.MultisigAccountInfo(
                account=models.PublicAccount(
                    address=models.Address(address='SA2AK4GEVSAX4NNG7KH4EGIXWNHMGEMWU7JT4RU5'),
                    public_key='9b1d7f4f4c2a0471edbc78f95de54b6e432887fc0c6e4ceca800089dae2a4044'
                ),
                min_approval=2,
                min_removal=2,
                cosignatories=[
                    models.PublicAccount(
                        address=models.Address(address='SD5M23VRSNS3AI3NPFUFCIQQTQW2G4L5BLDLMLAJ'),
                        public_key='6cb4caaacca7081c9e1471df8f6512abc99feb86efee7862ed7259397c5fdbdd'
                    ),
                    models.PublicAccount(
                        address=models.Address(address='SBI7LMDC7Y4TDMU3BFNLR7KC7TBACCXBUZ6ZAO6F'),
                        public_key='c5c55181284607954e56cd46de85f4f3ef4cc713cc2b95000fa741998558d268'
                    ),
                    models.PublicAccount(
                        address=models.Address(address='SCSVO5XVNM4AICUEYXMUNEQSW5RUNUOVDLYHBCFM'),
                        public_key='cae725538ebebf7778257a442b4a48e116636580ed630ad5cb8d668dff52a1a7'
                    ),
                ],
                multisig_accounts=[],
            ),
        ],
    },
    'dto': [
        {
            'level': 0,
            'multisigEntries': [
                {
                    'multisig': {
                        'account': '9b1d7f4f4c2a0471edbc78f95de54b6e432887fc0c6e4ceca800089dae2a4044',
                        'accountAddress': '90340570c4ac817e35a6fa8fc21917b34ec31196a7d33e469d',
                        'minApproval': 2,
                        'minRemoval': 2,
                        'cosignatories': [
                            '6cb4caaacca7081c9e1471df8f6512abc99feb86efee7862ed7259397c5fdbdd',
                            'c5c55181284607954e56cd46de85f4f3ef4cc713cc2b95000fa741998558d268',
                            'cae725538ebebf7778257a442b4a48e116636580ed630ad5cb8d668dff52a1a7'
                        ],
                        'multisigAccounts': []
                    },
                },
            ],
        },
    ],
})
class TestMultisigAccountGraphInfo(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.MultisigAccountInfo,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'account': models.PublicAccount.create_from_public_key('9b1d7f4f4c2a0471edbc78f95de54b6e432887fc0c6e4ceca800089dae2a4044', models.NetworkType.MIJIN_TEST),
        'min_approval': 2,
        'min_removal': 2,
        'cosignatories': [
            models.PublicAccount.create_from_public_key('6cb4caaacca7081c9e1471df8f6512abc99feb86efee7862ed7259397c5fdbdd', models.NetworkType.MIJIN_TEST),
            models.PublicAccount.create_from_public_key('c5c55181284607954e56cd46de85f4f3ef4cc713cc2b95000fa741998558d268', models.NetworkType.MIJIN_TEST),
            models.PublicAccount.create_from_public_key('cae725538ebebf7778257a442b4a48e116636580ed630ad5cb8d668dff52a1a7', models.NetworkType.MIJIN_TEST),
        ],
        'multisig_accounts': [],
    },
    'dto': {
        'multisig': {
            'account': '9b1d7f4f4c2a0471edbc78f95de54b6e432887fc0c6e4ceca800089dae2a4044',
            'accountAddress': '90340570c4ac817e35a6fa8fc21917b34ec31196a7d33e469d',
            'minApproval': 2,
            'minRemoval': 2,
            'cosignatories': [
                '6cb4caaacca7081c9e1471df8f6512abc99feb86efee7862ed7259397c5fdbdd',
                'c5c55181284607954e56cd46de85f4f3ef4cc713cc2b95000fa741998558d268',
                'cae725538ebebf7778257a442b4a48e116636580ed630ad5cb8d668dff52a1a7'
            ],
            'multisigAccounts': [],
        },
    },
})
class TestMultisigAccountInfo(harness.TestCase):

    def test_is_multisig(self):
        self.assertTrue(self.model.is_multisig())

    def test_has_cosigner(self):
        for account in self.data['cosignatories']:
            self.assertTrue(self.model.has_cosigner(account))
        for account in self.data['multisig_accounts']:
            self.assertFalse(self.model.has_cosigner(account))
        self.assertFalse(self.model.has_cosigner(self.model.account))

    def test_is_cosigner_of_multisig_account(self):
        for account in self.data['cosignatories']:
            self.assertFalse(self.model.is_cosigner_of_multisig_account(account))
        for account in self.data['multisig_accounts']:
            self.assertTrue(self.model.is_cosigner_of_multisig_account(account))
        self.assertFalse(self.model.is_cosigner_of_multisig_account(self.model.account))


@harness.enum_test_case({
    'type': models.PropertyModificationType,
    'enums': [
        models.PropertyModificationType.ADD,
        models.PropertyModificationType.REMOVE,
    ],
    'values': [
        0x00,
        0x01,
    ],
    'descriptions': [
        "Add property to account",
        "Remove property from account",
    ],
    'dto': [
        0x00,
        0x01,
    ],
    'catbuffer': [
        b'\x00',
        b'\x01',
    ],
})
class TestPropertyModificationType(harness.TestCase):
    pass


@harness.enum_test_case({
    'type': models.PropertyType,
    'enums': [
        models.PropertyType.ALLOW_ADDRESS,
        models.PropertyType.ALLOW_MOSAIC,
        models.PropertyType.ALLOW_TRANSACTION,
        models.PropertyType.SENTINEL,
        models.PropertyType.BLOCK_ADDRESS,
        models.PropertyType.BLOCK_MOSAIC,
        models.PropertyType.BLOCK_TRANSACTION,
    ],
    'values': [
        0x01,
        0x02,
        0x04,
        0x05,
        0x81,
        0x82,
        0x84,
    ],
    'descriptions': [
        "The property type is an address.",
        "The property type is a mosaic id.",
        "The property type is a transaction type.",
        "Property type sentinel.",
        "The property type is a blocking address operation.",
        "The property type is a blocking mosaic id operation.",
        "The property type is a blocking transaction type operation.",
    ],
    'dto': [
        0x01,
        0x02,
        0x04,
        0x05,
        0x81,
        0x82,
        0x84,
    ],
    'catbuffer': [
        b'\x01',
        b'\x02',
        b'\x04',
        b'\x05',
        b'\x81',
        b'\x82',
        b'\x84',
    ],
})
class TestPropertyType(harness.TestCase):
    pass


@harness.model_test_case({
    'type': models.PublicAccount,
    'network_type': models.NetworkType.MIJIN_TEST,
    'data': {
        'public_key': '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955',
        'address': models.Address('SAUJCIBCOFLHUZIWNB32MR6YUX75HO7GGCVZEXSG'),
    },
    'extras': {
        'message': b'Hello World!',
        'signature': '40af0cb5a7a7533f07a4ba6f1cb2df64f2347feb1b2eaabb9374d28603d146497ea83d3d6ee15758d39c298b48f58e578cc42f36a373e15eef7412e0bd19a801',
        'payload': 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7',
    }
})
class TestPublicAccount(harness.TestCase):

    def test_invalid_public_key(self):
        with self.assertRaises(ValueError):
            self.type(self.data['address'], '')

    def test_properties(self):
        self.assertEqual(self.model.network_type, self.network_type)

    def test_create_from_public_key(self):
        self.assertEqual(self.model, self.type.create_from_public_key(self.data['public_key'], self.network_type))

    @harness.ignore_warnings_test
    def test_verify_signature(self):
        self.assertTrue(self.model.verify_signature(self.extras['message'], self.extras['signature']))
        self.assertFalse(self.model.verify_signature(self.extras['message'], '0' * 128))
        with self.assertRaises(ValueError):
            self.assertTrue(self.model.verify_signature(self.extras['message'], ''))

    @harness.ignore_warnings_test
    def test_verify_transaction(self):
        self.assertTrue(self.model.verify_transaction(self.extras['payload']))
