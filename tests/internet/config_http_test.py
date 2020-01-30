from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config


@harness.http_test_case({
    'clients': (client.ConfigHTTP, client.AsyncConfigHTTP),
    'tests': [
        {
            'name': 'test_get_config',
            'params': [100,],
            'method': 'get_config',
            'validation': [
                lambda x: (isinstance(x, models.CatapultConfig), True),
            ]
        },
    ],
})
class TestConfigHttp(harness.TestCase):
    pass
