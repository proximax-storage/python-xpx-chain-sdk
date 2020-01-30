from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config

@harness.http_test_case({
    'clients': (client.NamespaceHTTP, client.AsyncNamespaceHTTP),
    'tests': [
        {
            #/namespace/{namespaceId}
            'name': 'test_get_namespace',
            'params': [models.NamespaceId('prx.xpx')],
            'method': 'get_namespace',
            'validation': [
                lambda x: (isinstance(x, models.NamespaceInfo), True),
                lambda x: (x.owner.public_key, config.nemesis_signer_public_key),
            ]
        },
        {
            #/account/{accountId}/namespaces
            'name': 'test_get_namespaces_from_account',
            'params': [config.nemesis_signer.address],
            'method': 'get_namespaces_from_account',
            'validation': [
                lambda x: (len(x), 4),
                lambda x: (isinstance(x[0], models.NamespaceInfo), True),
            ]
        },
        {
            #/account/namespaces
            'name': 'test_get_namespaces_from_accounts',
            'params': [[config.nemesis_signer.address]],
            'method': 'get_namespaces_from_accounts',
            'validation': [
                lambda x: (len(x), 4),
                lambda x: (isinstance(x[0], models.NamespaceInfo), True),
            ]
        },
        {
            #/namespace/names
            'name': 'test_get_namespaces_name',
            'params': [[models.NamespaceId.create_from_hex('b16d77fd8b6fb3be')]],
            'method': 'get_namespaces_name',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].name, 'prx'),
            ]
        },
    ],
})
class TestNamespaceHttp(harness.TestCase):
    pass
