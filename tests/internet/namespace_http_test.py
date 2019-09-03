from nem2 import client
from nem2 import models
from tests import harness


@harness.http_test_case({
    'clients': (client.NamespaceHTTP, client.AsyncNamespaceHTTP),
    'tests': [
        {
            'name': 'test_get_namespaces_from_account',
            'params': [models.Address('SARNASAS2BIAB6LMFA3FPMGBPGIJGK6IJETM3ZSP')],
            'method': 'get_namespaces_from_account',
            'validation': [
                lambda x: (len(x), 3),
                lambda x: (x[0].meta_id, '5D62745F8E825C00011B7CB6'),
            ]
        },
        {
            'name': 'test_get_namespaces_from_accounts',
            'params': [[models.Address('SARNASAS2BIAB6LMFA3FPMGBPGIJGK6IJETM3ZSP')]],
            'method': 'get_namespaces_from_accounts',
            'validation': [
                lambda x: (len(x), 3),
                lambda x: (x[0].meta_id, '5D62745F8E825C00011B7CB6'),
            ]
        },
        {
            'name': 'test_get_namespaces_name',
            'params': [[models.NamespaceId.create_from_hex('b16d77fd8b6fb3be')]],
            'method': 'get_namespaces_name',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].name, 'prx'),
            ]
        },
        {
            'name': 'test_get_namespace',
            'params': [models.NamespaceId.create_from_hex('b16d77fd8b6fb3be')],
            'method': 'get_namespace',
            'validation': [
                lambda x: (x.meta_id, '5D62745F8E825C00011B7CB5'),
            ]
        },
    ],
})
class TestNamespaceHttp(harness.TestCase):
    pass
