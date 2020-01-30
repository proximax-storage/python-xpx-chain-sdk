from xpxchain import client
from xpxchain import models
from tests import harness
from tests import responses


@harness.mocked_http_test_case({
    'clients': (client.NamespaceHTTP, client.AsyncNamespaceHTTP),
    'network_type': models.NetworkType.MIJIN_TEST,
    'tests': [
        {
            'name': 'test_get_namespace',
            'response': responses.NAMESPACE['nem'],
            'params': [models.NamespaceId.create_from_hex('84b3552d375ffa4b')],
            'method': 'get_namespace',
            'validation': [
                lambda x: (x.active, True),
                lambda x: (x.index, 0),
                lambda x: (x.meta_id, '5C7C07005CC1FE000176FA2B'),
                lambda x: (x.type, models.NamespaceType.ROOT_NAMESPACE),
                lambda x: (x.depth, 1),
                lambda x: (x.levels[0].encoded, '4bfa5f372d55b384'),
                lambda x: (x.parent_id, models.NamespaceId(0)),
                lambda x: (x.owner.address.address, 'SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM'),
                lambda x: (x.owner.public_key, '7A562888C7AE1E082579951D6D93BF931DE979360ACCA4C4085D754E5E122808'),
                lambda x: (x.start_height, 1),
                lambda x: (x.end_height, 18446744073709551615),
                lambda x: (x.alias, models.EmptyAlias()),
            ]
        },
        {
            'name': 'test_get_namespaces_name',
            'response': responses.NAMESPACE_NAMES['nem'],
            'params': [[models.NamespaceId.create_from_hex('84b3552d375ffa4b')]],
            'method': 'get_namespaces_name',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].namespace_id.encoded, '4bfa5f372d55b384'),
                lambda x: (x[0].name, 'nem'),
            ]
        },
        {
            'name': 'test_get_namespaces_from_account',
            'response': responses.NAMESPACES["nem"],
            'params': [models.Address('SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM')],
            'method': 'get_namespaces_from_account',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].meta_id, '5C7C07005CC1FE000176FA2B'),
            ]
        },
        {
            'name': 'test_get_namespaces_from_accounts',
            'response': responses.NAMESPACES["nem"],
            'params': [[models.Address('SD3MA6SM7GWRX4DEJVAZEGFXF7G7D36MA6TMSIBM')]],
            'method': 'get_namespaces_from_accounts',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (x[0].meta_id, '5C7C07005CC1FE000176FA2B'),
            ]
        },
        {
            'name': 'test_get_linked_mosaic_id',
            'response': responses.NAMESPACE["nem"],
            'params': [models.NamespaceId.create_from_hex("84b3552d375ffa4b")],
            'method': 'get_linked_mosaic_id',
            'error': ValueError,
        },
        {
            'name': 'test_get_linked_address',
            'response': responses.NAMESPACE["nem"],
            'params': [models.NamespaceId.create_from_hex("84b3552d375ffa4b")],
            'method': 'get_linked_address',
            'error': ValueError,
        },
    ],
})
class TestNamespaceHTTP(harness.TestCase):
    pass
