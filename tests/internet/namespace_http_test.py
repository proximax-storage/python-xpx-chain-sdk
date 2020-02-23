from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config


class TestNamespaceHttp(harness.TestCase):
    
    def test_get_namespace(self):
        with client.NamespaceHTTP(config.ENDPOINT) as http:
            info = http.get_namespace(models.NamespaceId('prx.xpx'))
            self.assertEqual(isinstance(info, models.NamespaceInfo), True)
            self.assertEqual(info.owner.public_key, config.nemesis.public_key.upper())
    
    def test_get_namespaces_from_account(self):
        with client.NamespaceHTTP(config.ENDPOINT) as http:
            info = http.get_namespaces_from_account(config.nemesis.address)
            self.assertEqual(len(info), 4)
            self.assertEqual(isinstance(info[0], models.NamespaceInfo), True)
    
    def test_get_namespaces_from_accounts(self):
        with client.NamespaceHTTP(config.ENDPOINT) as http:
            info = http.get_namespaces_from_accounts([config.nemesis.address])
            self.assertEqual(len(info), 4)
            self.assertEqual(isinstance(info[0], models.NamespaceInfo), True)
    
    def test_get_namespaces_name(self):
        with client.NamespaceHTTP(config.ENDPOINT) as http:
            info = http.get_namespaces_name([models.NamespaceId.create_from_hex('b16d77fd8b6fb3be')])
            self.assertEqual(len(info), 1)
            self.assertEqual(info[0].name, 'prx')
