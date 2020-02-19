from xpxchain import client
from xpxchain import models
from tests import harness
from tests import responses
from xpxchain import util


@harness.mocked_http_test_case({
    'clients': (client.MetadataHTTP, client.AsyncMetadataHTTP),
    'network_type': models.NetworkType.MIJIN_TEST,
    'tests': [
        {
            'name': 'test_get_account_metadata',
            'response': responses.ACCOUNT_METADATA["Ok"],
            'params': [models.PublicAccount.create_from_public_key('c55b4dfede7058a354aba9cff88dd6ba2d2006ab580bde849fb9d63481b462ab', models.NetworkType.MIJIN_TEST)],
            'method': 'get_account_metadata',
            'validation': [
                lambda x: (isinstance(x, models.AddressMetadataInfo), True),
                lambda x: (isinstance(x.metadata, models.AddressMetadata), True),
                lambda x: (x.metadata.metadata_type, models.MetadataType.ADDRESS),
                lambda x: (isinstance(x.metadata.metadata_id, models.Address), True),
                lambda x: (x.metadata.metadata_id.hex, '90ABBF4346E893A8EA4E420C6DBB9EBE9BE9180CD4056EAA28'),
                lambda x: (len(x.metadata.flds), 2),
                lambda x: (isinstance(x.metadata.flds[0], models.Field), True),
                lambda x: (x.metadata.flds[0].key, 'foo'),
                lambda x: (x.metadata.flds[0].value, 'bar'),
                lambda x: (x.metadata.flds[1].key, 'foo2'),
                lambda x: (x.metadata.flds[1].value, 'bar'),
            ],
        },
        {
            'name': 'test_get_mosaic_metadata',
            'response': responses.MOSAIC_METADATA["Ok"],
            'params': [models.MosaicId(util.u64_from_dto([1045581869, 105004269]))],
            'method': 'get_mosaic_metadata',
            'validation': [
                lambda x: (isinstance(x, models.MosaicMetadataInfo), True),
                lambda x: (isinstance(x.metadata, models.MosaicMetadata), True),
                lambda x: (x.metadata.metadata_type, models.MetadataType.MOSAIC),
                lambda x: (isinstance(x.metadata.metadata_id, models.MosaicId), True),
                lambda x: (x.metadata.metadata_id, models.MosaicId(util.u64_from_dto([1045581869, 105004269]))),
                lambda x: (len(x.metadata.flds), 2),
                lambda x: (isinstance(x.metadata.flds[0], models.Field), True),
                lambda x: (x.metadata.flds[0].key, 'foo'),
                lambda x: (x.metadata.flds[0].value, 'bar'),
                lambda x: (x.metadata.flds[1].key, 'foo2'),
                lambda x: (x.metadata.flds[1].value, 'bar'),
            ],
        },
        {
            'name': 'test_get_namespace_metadata',
            'response': responses.NAMESPACE_METADATA["Ok"],
            'params': [models.NamespaceId(util.u64_from_dto([130473079, 2260557970]))],
            'method': 'get_namespace_metadata',
            'validation': [
                lambda x: (isinstance(x, models.NamespaceMetadataInfo), True),
                lambda x: (isinstance(x.metadata, models.NamespaceMetadata), True),
                lambda x: (x.metadata.metadata_type, models.MetadataType.NAMESPACE),
                lambda x: (isinstance(x.metadata.metadata_id, models.NamespaceId), True),
                lambda x: (x.metadata.metadata_id, models.NamespaceId(util.u64_from_dto([130473079, 2260557970]))),
                lambda x: (len(x.metadata.flds), 2),
                lambda x: (isinstance(x.metadata.flds[0], models.Field), True),
                lambda x: (x.metadata.flds[0].key, 'foo'),
                lambda x: (x.metadata.flds[0].value, 'bar'),
                lambda x: (x.metadata.flds[1].key, 'foo2'),
                lambda x: (x.metadata.flds[1].value, 'bar'),
            ],
        },
        {
            'name': 'test_get_metadata',
            'response': responses.METADATA["Ok"],
            'params': [models.Address('SCV36Q2G5CJ2R2SOIIGG3O46X2N6SGAM2QCW5KRI')],
            'method': 'get_metadata',
            'validation': [
                lambda x: (isinstance(x, models.MetadataInfo), True),
                lambda x: (isinstance(x.metadata, models.AddressMetadata), True),
                lambda x: (x.metadata.metadata_type, models.MetadataType.ADDRESS),
                lambda x: (isinstance(x.metadata.metadata_id, models.Address), True),
                lambda x: (x.metadata.metadata_id.hex, '90ABBF4346E893A8EA4E420C6DBB9EBE9BE9180CD4056EAA28'),
                lambda x: (len(x.metadata.flds), 2),
                lambda x: (isinstance(x.metadata.flds[0], models.Field), True),
                lambda x: (x.metadata.flds[0].key, 'foo'),
                lambda x: (x.metadata.flds[0].value, 'bar'),
                lambda x: (x.metadata.flds[1].key, 'foo2'),
                lambda x: (x.metadata.flds[1].value, 'bar'),
            ],
        },
        {
            'name': 'test_get_metadatas',
            'response': responses.METADATAS["Ok"],
            'params': [[models.Address('SCV36Q2G5CJ2R2SOIIGG3O46X2N6SGAM2QCW5KRI')]],
            'method': 'get_metadatas',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (isinstance(x[0], models.MetadataInfo), True),
                lambda x: (isinstance(x[0].metadata, models.AddressMetadata), True),
                lambda x: (x[0].metadata.metadata_type, models.MetadataType.ADDRESS),
                lambda x: (isinstance(x[0].metadata.metadata_id, models.Address), True),
                lambda x: (x[0].metadata.metadata_id.hex, '90ABBF4346E893A8EA4E420C6DBB9EBE9BE9180CD4056EAA28'),
                lambda x: (len(x[0].metadata.flds), 2),
                lambda x: (isinstance(x[0].metadata.flds[0], models.Field), True),
                lambda x: (x[0].metadata.flds[0].key, 'foo'),
                lambda x: (x[0].metadata.flds[0].value, 'bar'),
                lambda x: (x[0].metadata.flds[1].key, 'foo2'),
                lambda x: (x[0].metadata.flds[1].value, 'bar'),
            ],
        },
    ],
})
class TestMetadataHTTP(harness.TestCase):
    pass
