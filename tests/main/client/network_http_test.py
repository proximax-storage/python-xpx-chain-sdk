from xpxchain import client
from xpxchain import models
from tests import harness
from tests import responses


@harness.mocked_http_test_case({
    'clients': (client.NetworkHTTP, client.AsyncNetworkHTTP),
    'network_type': models.NetworkType.MIJIN_TEST,
    'tests': [
        {
            'name': 'test_get_network_type',
            'response': responses.NETWORK_TYPE['MIJIN_TEST'],
            'params': [],
            'method': 'get_network_type',
            'validation': [
                lambda x: (x, models.NetworkType.MIJIN_TEST),
            ]
        },
    ],
})
class TestNetworkHTTP(harness.TestCase):
    pass
