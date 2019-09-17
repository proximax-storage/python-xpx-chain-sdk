from nem2 import client
from nem2 import models
from tests import harness
from tests import config


@harness.http_test_case({
    'clients': (client.ContractHTTP, client.AsyncContractHTTP),
    'tests': [
#        {
#            'name': 'test_get_contract',
#            'params': [config.Contract.hash],
#            'method': 'get_contract',
#            'validation': [
#                lambda x: (isinstance(x, models.Contract), True),
#            ]
#        },
#		{
#			#TODO
#            #/account/contracts
#            'name': 'test_get_contracts_by_public_keys',
#            'params': [models.Contract(contract_id)],
#            'method': 'get_contracts_by_public_keys',
#            'validation': [
#                lambda x: (len(x), 0),
#            ]
#        },
		{
            'name': 'test_get_contracts',
            'params': [[models.Address(config.Recipient.address)]],
            'method': 'get_contracts',
            'validation': [
                lambda x: (len(x), 0),
            ]
        },
    ],
})
class TestContractHttp(harness.TestCase):
    pass
