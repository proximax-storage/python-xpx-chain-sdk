from nem2 import client
from nem2 import models
from tests import harness
from tests import config

@harness.http_test_case({
    'clients': (client.TransactionHTTP, client.AsyncTransactionHTTP),
    'tests': [
        {
            #/transaction/{transactionId}
            'name': 'test_get_transaction',
            'params': [config.Transaction.hash],
            'method': 'get_transaction',
            'validation': [
                lambda x: (isinstance(x, models.Transaction), True),
            ]
        },
        {
            #/transaction/{transactionId}
            'name': 'test_get_transactions',
            'params': [[config.Transaction.hash, '024C08B8767FCA0DCF7B631EC2631D9575FFB84E8E5EFA7C656B18FB1A1F34E8']],
            'method': 'get_transactions',
            'validation': [
                lambda x: (len(x), 2),
                lambda x: (isinstance(x[0], models.Transaction), True),
            ]
        },
        {
            #/transaction/{hash}/status
            'name': 'test_get_transaction_status',
            'params': [config.Transaction.hash],
            'method': 'get_transaction_status',
            'validation': [
                lambda x: (isinstance(x, models.TransactionStatus), True),
            ]
        },
        {
            #/transaction/statuses
            'name': 'test_get_transaction_statuses',
            'params': [[config.Transaction.hash, '024C08B8767FCA0DCF7B631EC2631D9575FFB84E8E5EFA7C656B18FB1A1F34E8']],
            'method': 'get_transaction_statuses',
            'validation': [
                lambda x: (len(x), 2),
                lambda x: (isinstance(x[0], models.TransactionStatus), True),
            ]
        },
    ],
})
class TestTransactionHttp(harness.TestCase):
    pass
