from nem2 import client
from nem2 import models
from tests import harness
from tests import responses


@harness.mocked_http_test_case({
    'clients': (client.AccountHTTP, client.AsyncAccountHTTP),
    'network_type': models.NetworkType.MIJIN_TEST,
    'tests': [
        {
            'name': 'test_get_account_info',
            'response': responses.ACCOUNT_INFO["Ok"],
            'params': [models.Address('SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM')],
            'method': 'get_account_info',
            'validation': [
                lambda x: (x.public_key, '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808'),
                lambda x: (x.mosaics, []),
            ]
        },
        {
            'name': 'test_get_accounts_info',
            'response': responses.ACCOUNTS_INFO["Ok"],
            'params': [[models.Address('SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM')]],
            'method': 'get_accounts_info',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].public_key, '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808'),
                lambda x: (x[0].mosaics, []),
            ]
        },
        #  TODO(ahuszagh) Add more examples...
        # get_account_property
        # get_account_properties
        # get_multisig_account_info
        # get_multisig_account_graph_info
        # transactions
        # incoming_transactions
        # outgoing_transactions
        # unconfirmed_transactions
        # aggregate_bonded_transactions
    ],
})
class TestAccountHTTP(harness.TestCase):
    pass
