from xpx import client
from xpx import models
from tests import harness
from tests import responses


@harness.mocked_http_test_case({
    'clients': (client.AccountHTTP, client.AsyncAccountHTTP),
    'network_type': models.NetworkType.MIJIN_TEST,
    'tests': [
        {
            'name': 'test_get_account_info',
            'response': responses.ACCOUNT_INFO["Ok"],
            'params': [models.Address('SCBO3CAFOVAOGYBAHQKPUOGLAYWFLNJUFFCH3RYY')],
            'method': 'get_account_info',
            'validation': [
                lambda x: (x.public_key, '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808'),
                lambda x: (x.mosaics, []),
            ],
        },
        {
            'name': 'test_get_accounts_info',
            'response': responses.ACCOUNTS_INFO["Ok"],
            'params': [[models.Address('SCBO3CAFOVAOGYBAHQKPUOGLAYWFLNJUFFCH3RYY')]],
            'method': 'get_accounts_info',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].public_key, '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808'),
                lambda x: (x[0].mosaics, []),
            ],
        },
        #  TODO(ahuszagh) Add more examples...
        # get_account_property
        # get_account_properties
        {
            'name': 'test_get_multisig_account_info',
            'response': responses.MULTISIG_INFO["Ok"],
            'params': [models.Address('SA2AK4GEVSAX4NNG7KH4EGIXWNHMGEMWU7JT4RU5')],
            'method': 'get_multisig_account_info',
            'validation': [
                lambda x: (x.account.public_key, '9B1D7F4F4C2A0471EDBC78F95DE54B6E432887FC0C6E4CECA800089DAE2A4044'),
                lambda x: (x.min_approval, 2),
                lambda x: (x.min_removal, 2),
                lambda x: (len(x.cosignatories), 3),
                lambda x: (x.cosignatories[0].public_key, '6CB4CAAACCA7081C9E1471DF8F6512ABC99FEB86EFEE7862ED7259397C5FDBDD'),
                lambda x: (x.cosignatories[1].public_key, 'C5C55181284607954E56CD46DE85F4F3EF4CC713CC2B95000FA741998558D268'),
                lambda x: (x.cosignatories[2].public_key, 'CAE725538EBEBF7778257A442B4A48E116636580ED630AD5CB8D668DFF52A1A7'),
                lambda x: (len(x.multisig_accounts), 0),
            ],
        },
        {
            'name': 'test_get_multisig_account_graph_info',
            'response': responses.MULTISIG_GRAPH_INFO["Ok"],
            'params': [models.Address('SA2AK4GEVSAX4NNG7KH4EGIXWNHMGEMWU7JT4RU5')],
            'method': 'get_multisig_account_graph_info',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (len(x[0]), 1),
                lambda x: (x[0][0].account.public_key, '9b1d7f4f4c2a0471edbc78f95de54b6e432887fc0c6e4ceca800089dae2a4044'),
                lambda x: (x[0][0].min_approval, 2),
                lambda x: (x[0][0].min_removal, 2),
                lambda x: (len(x[0][0].cosignatories), 3),
                lambda x: (x[0][0].cosignatories[0].public_key, '6cb4caaacca7081c9e1471df8f6512abc99feb86efee7862ed7259397c5fdbdd'),
                lambda x: (x[0][0].cosignatories[1].public_key, 'c5c55181284607954e56cd46de85f4f3ef4cc713cc2b95000fa741998558d268'),
                lambda x: (x[0][0].cosignatories[2].public_key, 'cae725538ebebf7778257a442b4a48e116636580ed630ad5cb8d668dff52a1a7'),
                lambda x: (len(x[0][0].multisig_accounts), 0),
            ],
        },
        {
            'name': 'test_transactions',
            'response': responses.TRANSACTIONS["Ok"],
            'params': [models.PublicAccount.create_from_public_key('7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808', models.NetworkType.MIJIN_TEST)],
            'method': 'transactions',
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
            ],
        },
        {
            'name': 'test_incoming_transactions',
            'response': responses.TRANSACTIONS["Ok"],
            'params': [models.PublicAccount.create_from_public_key('7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808', models.NetworkType.MIJIN_TEST)],
            'method': 'incoming_transactions',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].version, 2),
                lambda x: (x[0].type, 16718),
            ],
        },
        {
            'name': 'test_outgoing_transactions',
            'response': responses.TRANSACTIONS["Ok"],
            'params': [models.PublicAccount.create_from_public_key('7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808', models.NetworkType.MIJIN_TEST)],
            'method': 'outgoing_transactions',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].version, 2),
                lambda x: (x[0].type, 16718),
            ],
        },
        {
            'name': 'test_outgoing_transactions',
            'response': responses.TRANSACTIONS["Ok"],
            'params': [models.PublicAccount.create_from_public_key('7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808', models.NetworkType.MIJIN_TEST)],
            'method': 'outgoing_transactions',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].version, 2),
                lambda x: (x[0].type, 16718),
            ],
        },
        {
            'name': 'test_unconfirmed_transactions',
            'response': responses.TRANSACTIONS["Ok"],
            'params': [models.PublicAccount.create_from_public_key('7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808', models.NetworkType.MIJIN_TEST)],
            'method': 'unconfirmed_transactions',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].version, 2),
                lambda x: (x[0].type, 16718),
            ],
        },
        {
            'name': 'test_aggregate_bonded_transactions',
            'response': responses.TRANSACTIONS["Ok"],
            'params': [models.PublicAccount.create_from_public_key('7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808', models.NetworkType.MIJIN_TEST)],
            'method': 'aggregate_bonded_transactions',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].version, 2),
                lambda x: (x[0].type, 16718),
            ],
        },
    ],
})
class TestAccountHTTP(harness.TestCase):
    pass
