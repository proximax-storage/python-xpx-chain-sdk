from xpxchain import client
from xpxchain import models
from tests import harness
from tests import responses


@harness.mocked_http_test_case({
    'clients': (client.ConfigHTTP, client.AsyncConfigHTTP),
    'network_type': models.NetworkType.MIJIN_TEST,
    'tests': [
        {
            'name': 'test_get_config',
            'response': responses.CONFIG["Ok"],
            'params': [100],
            'method': 'get_config',
            'validation': [
                lambda x: (isinstance(x, models.CatapultConfig), True),
                lambda x: (x.height, 1),
                lambda x: (x.network_config, 'config'),
                lambda x: (x.supported_entity_versions, 'versions'),
            ],
        },
        {
            'name': 'test_get_upgrade',
            'response': responses.UPGRADE["Ok"],
            'params': [100],
            'method': 'get_upgrade',
            'validation': [
                lambda x: (isinstance(x, models.CatapultUpgrade), True),
                lambda x: (isinstance(x.blockchain_upgrade, models.Upgrade), True),
                lambda x: (x.blockchain_upgrade.height, 1),
                lambda x: (x.blockchain_upgrade.blockchain_version, 17180000256),
            ],
        },
    ],
})
class TestConfigHTTP(harness.TestCase):
    pass
