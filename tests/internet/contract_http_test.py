from xpxchain import client
from xpxchain import models
from tests import harness
from tests import config


@harness.http_test_case({
    'clients': (client.ContractHTTP, client.AsyncContractHTTP),
    'tests': [
    ],
})
class TestContractHttp(harness.TestCase):
    pass
