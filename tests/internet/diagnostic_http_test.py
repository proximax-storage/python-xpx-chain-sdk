from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config


@harness.http_test_case({
    'clients': (client.BlockchainHTTP, client.AsyncBlockchainHTTP),
    'tests': [
        {
            #/diagnostic/storage
            'name': 'test_get_diagnostic_storage',
            'params': [],
            'method': 'get_diagnostic_storage',
            'validation': [
                lambda x: (isinstance(x, models.BlockchainStorageInfo), True),
            ]
        },
        {
            #/diagnostic/server
            'name': 'test_get_diagnostic_server',
            'params': [],
            'method': 'get_diagnostic_server',
            'validation': [
                lambda x: (isinstance(x, models.BlockchainServerInfo), True),
            ]
        },
    ],
})
class TestDiagnosticHttp(harness.TestCase):
    pass
