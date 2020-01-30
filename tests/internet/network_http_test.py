from xpxchain import client
from xpxchain import models
from tests import harness


@harness.http_test_case({
    'clients': (client.NetworkHTTP, client.AsyncNetworkHTTP),
    'tests': [
        {
            #/network
            'name': 'test_get_network_type',
            'params': [],
            'method': 'get_network_type',
            'validation': [
                lambda x: (isinstance(x, models.NetworkType), True),
                lambda x: (x, models.NetworkType.MIJIN_TEST),
            ]
        },
    ],
})
class TestNetworkHttp(harness.TestCase):
    pass
