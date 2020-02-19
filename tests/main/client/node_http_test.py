from xpxchain import client
from xpxchain import models
from tests import harness
from tests import responses


@harness.mocked_http_test_case({
    'clients': (client.NodeHTTP, client.AsyncNodeHTTP),
    'network_type': models.NetworkType.MIJIN_TEST,
    'tests': [
        {
            'name': 'test_get_node_info',
            'response': responses.INFO["Ok"],
            'params': [],
            'method': 'get_node_info',
            'validation': [
                lambda x: (isinstance(x, models.NodeInfo), True),
                lambda x: (x.public_key, '460458B98E2BAA36A8E95DE9B320379E89898885B71CF0174E02F1324FAFFAC1'),
                lambda x: (x.port, 7900),
                lambda x: (x.network_identifier, models.NetworkType.MIJIN_TEST),
                lambda x: (x.version, 0),
                lambda x: (x.roles, 2),
                lambda x: (x.friendly_name, 'api-node-0'),
            ],
        },
        {
            'name': 'test_get_node_time',
            'response': responses.TIME["Ok"],
            'params': [],
            'method': 'get_node_time',
            'validation': [
                lambda x: (isinstance(x, models.NodeTime), True),
                lambda x: (x.send_timestamp, 122457123440),
                lambda x: (x.receive_timestamp, 122457123440),
            ],
        },
    ],
})
class TestConfigHTTP(harness.TestCase):
    pass
