from nem2 import client
from nem2 import models
from tests import harness
from tests import config

@harness.http_test_case({
    'clients': (client.AccountHTTP, client.AsyncAccountHTTP),
    'tests': [
        {
            #/account/{accountId}
            'name': 'test_get_account_info',
            'params': [models.Address(config.Recipient.address)],
            'method': 'get_account_info',
            'validation': [
                lambda x: (x.public_key, config.Recipient.public_key),
            ]
        },
        {
            #/account
            'name': 'test_get_accounts_info',
            'params': [[models.Address(config.Recipient.address)]],
            'method': 'get_accounts_info',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].public_key, config.Recipient.public_key),
            ]
        },
        {
            #/account/{publicKey}/transaction
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
            #/account/{publicKey}/transaction/incoming
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
            #/account/{publicKey}/transaction/outgoing
            'name': 'test_outgoing_transactions',
            'params': [models.PublicAccount(config.Sender.address, config.Sender.public_key)],
            'method': 'outgoing_transactions',
            'validation': [
                lambda x: (len(x), 0),
            ],
        },
        {
            #/account/{publicKey}/transaction/unconfirmed
            'name': 'test_unconfirmed_transactions',
            'params': [models.PublicAccount(config.Recipient.address, config.Recipient.public_key)],
            'method': 'unconfirmed_transactions',
            'validation': [
                lambda x: (len(x), 0),
            ],
        },
        {
            #/account/{publicKey}/transaction/partial
            'name': 'test_aggregate_bonded_transactions',
            'params': [models.PublicAccount(config.Recipient.address, config.Recipient.public_key)],
            'method': 'aggregate_bonded_transactions',
            'validation': [
                lambda x: (len(x), 0),
            ],
        },
        #TODO
        #/account/properties
        #TODO
        #/account/{accountId}/multisig
        #TODO
        #/account/{accountId}/multisig/graph
        #TODO
        #/account/names
        {
            #/account/{publicKey}/contracts
            'name': 'test_contracts',
            'params': [models.PublicAccount(config.Recipient.address, config.Recipient.public_key)],
            'method': 'contracts',
            'validation': [
                lambda x: (len(x), 0),
            ],
        },
    ],
})
class TestAccountHttp(harness.TestCase):
    pass
