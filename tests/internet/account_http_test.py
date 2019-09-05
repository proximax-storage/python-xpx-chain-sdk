from nem2 import client
from nem2 import models
from tests import harness
from tests import config

@harness.http_test_case({
    'clients': (client.AccountHTTP, client.AsyncAccountHTTP),
    'tests': [
        {
            'name': 'test_get_account_info',
            'params': [models.Address(config.Recipient.address)],
            'method': 'get_account_info',
            'validation': [
                lambda x: (x.public_key, config.Recipient.public_key),
            ]
        },
        {
            'name': 'test_get_accounts_info',
            'params': [[models.Address(config.Recipient.address)]],
            'method': 'get_accounts_info',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].public_key, config.Recipient.public_key),
            ]
        },
        {
            'name': 'test_account_transactions',
            'params': [models.PublicAccount(config.Recipient.address, config.Recipient.public_key)],
            'method': 'transactions',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].recipient.address, config.Recipient.address),
                lambda x: (x[0].type, 16724),
            ]
        },
        {
            'name': 'test_incoming_transactions',
            'params': [models.PublicAccount(config.Recipient.address, config.Recipient.public_key)],
            'method': 'incoming_transactions',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].recipient.address, config.Recipient.address),
                lambda x: (x[0].type, 16724),
            ],
        },
        {
            'name': 'test_outgoing_transactions',
            'params': [models.PublicAccount(config.Sender.address, config.Sender.public_key)],
            'method': 'outgoing_transactions',
            'validation': [
                lambda x: (len(x), 0),
            ],
        },
        {
            'name': 'test_unconfirmed_transactions',
            'params': [models.PublicAccount(config.Recipient.address, config.Recipient.public_key)],
            'method': 'unconfirmed_transactions',
            'validation': [
                lambda x: (len(x), 0),
            ],
        },
        {
            'name': 'test_aggregate_bonded_transactions',
            'params': [models.PublicAccount(config.Recipient.address, config.Recipient.public_key)],
            'method': 'aggregate_bonded_transactions',
            'validation': [
                lambda x: (len(x), 0),
            ],
        },
    ],
})
class TestAccountHttp(harness.TestCase):
    pass
