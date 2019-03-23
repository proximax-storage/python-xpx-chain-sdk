from nem2 import client
from nem2 import models
from tests import harness


@harness.http_test_case({
    'clients': (client.AccountHTTP, client.AsyncAccountHTTP),
    'tests': [
        {
            'name': 'test_get_account_info',
            'params': [models.Address('SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM')],
            'method': 'get_account_info',
            'validation': [
                lambda x: (x.public_key, '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808'),
            ]
        },
        {
            'name': 'test_get_accounts_info',
            'params': [[models.Address('SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM')]],
            'method': 'get_accounts_info',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].public_key, '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808'),
            ]
        },
    ],
})
class TestAccountHttp(harness.TestCase):
    pass
