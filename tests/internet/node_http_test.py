from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config

@harness.http_test_case({
    'clients': (client.NodeHTTP, client.AsyncNodeHTTP),
    'tests': [
        {
            #/node/info
            'name': 'test_get_node_info',
            'params': [],
            'method': 'get_node_info',
            'validation': [
                lambda x: (isinstance(x, models.NodeInfo), True),
                lambda x: (x.public_key, config.api_node_public_key),
            ]
        },
        {
            #/node/time
            'name': 'test_get_node_time',
            'params': [],
            'method': 'get_node_time',
            'validation': [
                lambda x: (isinstance(x, models.NodeTime), True),
            ]
        },
    ],
})
class TestNodeHttp(harness.TestCase):
    pass
