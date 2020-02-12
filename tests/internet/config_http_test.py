from xpxchain import client
from xpxchain import models
from tests import harness


@harness.http_test_case({
    'clients': (client.ConfigHTTP, client.AsyncConfigHTTP),
    'tests': [
        {
            'name': 'test_get_config',
            'params': [100, ],
            'method': 'get_config',
            'validation': [
                lambda x: (isinstance(x, models.CatapultConfig), True),
            ]
        },
        {
            'name': 'test_get_upgrade',
            'params': [100, ],
            'method': 'get_upgrade',
            'validation': [
                lambda x: (isinstance(x, models.CatapultUpgrade), True),
            ]
        },
    ],
})
class TestConfigHttp(harness.TestCase):
    pass
