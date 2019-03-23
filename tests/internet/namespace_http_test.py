from nem2 import client
from nem2 import models
from tests import harness


@harness.http_test_case({
    'clients': (client.NamespaceHTTP, client.AsyncNamespaceHTTP),
    'tests': [
        {
            'name': 'test_get_namespaces_from_account',
            'params': [models.Address('SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM')],
            'method': 'get_namespaces_from_account',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].meta_id, '5C7C07005CC1FE000176FA2B'),
            ]
        },
        {
            'name': 'test_get_namespaces_from_accounts',
            'params': [[models.Address('SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM')]],
            'method': 'get_namespaces_from_accounts',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].meta_id, '5C7C07005CC1FE000176FA2B'),
            ]
        },
        {
            'name': 'test_get_namespace_names',
            'params': [[models.NamespaceId.from_hex('84b3552d375ffa4b')]],
            'method': 'get_namespace_names',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].name, 'nem'),
            ]
        },
        {
            'name': 'test_get_namespace',
            'params': [models.NamespaceId.from_hex('84b3552d375ffa4b')],
            'method': 'get_namespace',
            'validation': [
                lambda x: (x.meta_id, '5C7C07005CC1FE000176FA2B'),
            ]
        },
    ],
})
class TestNamespaceHttp(harness.TestCase):
    pass
