from nem2 import client
from nem2 import models
from tests import harness


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
