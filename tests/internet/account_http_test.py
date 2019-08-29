from nem2 import client
from nem2 import models
from tests import harness
from tests import config

@harness.http_test_case({
    'clients': (client.AccountHTTP, client.AsyncAccountHTTP),
    'tests': [
        {
            'name': 'test_get_account_info',
            'params': [models.Address(config.address)],
            'method': 'get_account_info',
            'validation': [
                lambda x: (x.public_key, config.public_key),
            ]
        },
        {
            'name': 'test_get_accounts_info',
            'params': [[models.Address(config.address)]],
            'method': 'get_accounts_info',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].public_key, config.public_key),
            ]
        },
    ],
})
class TestAccountHttp(harness.TestCase):
    pass
