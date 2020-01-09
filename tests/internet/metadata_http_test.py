from nem2 import client
from nem2 import models
from tests import harness
from tests import config


@harness.http_test_case({
    'clients': (client.MetadataHTTP, client.AsyncMetadataHTTP),
    'tests': [
    ],
})
class TestMetadataHttp(harness.TestCase):
    pass
