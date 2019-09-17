from nem2 import client
from nem2 import models
from tests import harness
from tests import config


@harness.http_test_case({
    'clients': (client.MetadataHTTP, client.AsyncMetadataHTTP),
    'tests': [
		{
            'name': 'test_get_metadata',
            'params': ["d525ad41d95fcf29"],
            'method': 'get_metadata',
            'validation': [
                lambda x: (isinstance(x, models.AddressMetadataInfo), True),
            ]
        },
		{
            'name': 'test_get_metadatas',
            'params': [["d525ad41d95fcf29", "SCJW742TNBMMX2UO4DVKXGP6T3CO6XXR6ZRWMVU2"]],
            'method': 'get_metadatas',
            'validation': [
                lambda x: (len(x), 0),
            ]
        },
    ],
})
class TestMetadataHttp(harness.TestCase):
    pass
