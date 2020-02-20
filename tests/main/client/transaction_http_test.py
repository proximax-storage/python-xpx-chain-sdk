from xpxchain import client
from xpxchain import models
from tests import harness
from tests import responses
from xpxchain import util


@harness.mocked_http_test_case({
    'clients': (client.TransactionHTTP, client.AsyncTransactionHTTP),
    'network_type': models.NetworkType.MIJIN_TEST,
    'tests': [
        {
            'name': 'test_get_transaction',
            'response': responses.TRANSACTION["Ok"],
            'params': ['47490969DB1960AD8565E67700C47FE41BBE07C6F490A66D3001AC46B6684600'],
            'method': 'get_transaction',
            'validation': [
                lambda x: (isinstance(x, models.Transaction), True),
                lambda x: (isinstance(x, models.TransferTransaction), True),
                lambda x: (isinstance(x.type, models.TransactionType), True),
                lambda x: (x.type, models.TransactionType.TRANSFER),
                lambda x: (isinstance(x.network_type, models.NetworkType), True),
                lambda x: (x.network_type, models.NetworkType.MIJIN_TEST),
                lambda x: (x.version, models.TransactionVersion.TRANSFER),
                lambda x: (isinstance(x.deadline, models.Deadline), True),
                lambda x: (x.deadline, models.Deadline.create_from_timestamp(util.u64_from_dto([2208860662, 28]))),
                lambda x: (x.max_fee, 41750),
                lambda x: (x.signature, '3A6D4A8EE69C509F7D020C5DBCD3B7E9610B0571F2C7F14229D900A85D51E41EB52BCBEFFD1D95CB40C996540657DBA33090E27A3AA5E0D71F727A055B6D5403'),
                lambda x: (isinstance(x.signer, models.PublicAccount), True),
                lambda x: (x.signer.public_key, '0EB448D07C7CCB312989AC27AA052738FF589E2F83973F909B506B450DC5C4E2'),
                lambda x: (isinstance(x.transaction_info, models.TransactionInfo), True),
                lambda x: (x.transaction_info.height, 158158),
                lambda x: (x.transaction_info.hash, '47490969DB1960AD8565E67700C47FE41BBE07C6F490A66D3001AC46B6684600'),
                lambda x: (x.transaction_info.id, '5E4A463F6466D3000169F159'),
                lambda x: (x.transaction_info.index, 0),
                lambda x: (x.transaction_info.merkle_component_hash, '47490969DB1960AD8565E67700C47FE41BBE07C6F490A66D3001AC46B6684600'),
                lambda x: (isinstance(x.recipient, models.Address), True),
                lambda x: (x.recipient.hex, '90C9102514E6A3893E53A5E06365E1074462E3BB1AF4F36529'),
                lambda x: (len(x.mosaics), 1),
                lambda x: (isinstance(x.mosaics[0], models.Mosaic), True),
                lambda x: (isinstance(x.mosaics[0].id, models.MosaicId), True),
                lambda x: (int(x.mosaics[0].id), 992621222383397347),
                lambda x: (x.mosaics[0].amount, 10000000),
                lambda x: (isinstance(x.message, models.Message), True),
                lambda x: (isinstance(x.message.type, models.MessageType), True),
                lambda x: (x.message.type, models.MessageType.PLAIN),
                lambda x: (x.message.payload, b''),
            ],
        },
        {
            'name': 'test_get_transactions',
            'response': responses.TRANSACTIONS["Ok"],
            'params': [['47490969DB1960AD8565E67700C47FE41BBE07C6F490A66D3001AC46B6684600']],
            'method': 'get_transactions',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (isinstance(x[0], models.Transaction), True),
                lambda x: (isinstance(x[0], models.TransferTransaction), True),
            ],
        },
        {
            'name': 'test_get_transaction_status',
            'response': responses.TRANSACTION_STATUS["Ok"],
            'params': ['135B65FF4E9E90E2F3283D75E2AD3D45EC46729013786841E32904D5134FD2B9'],
            'method': 'get_transaction_status',
            'validation': [
                lambda x: (isinstance(x, models.TransactionStatus), True),
                lambda x: (isinstance(x.group, models.TransactionStatusGroup), True),
                lambda x: (x.group, models.TransactionStatusGroup.CONFIRMED),
                lambda x: (x.status, 'Success'),
                lambda x: (x.hash, '135B65FF4E9E90E2F3283D75E2AD3D45EC46729013786841E32904D5134FD2B9'),
                lambda x: (isinstance(x.deadline, models.Deadline), True),
                lambda x: (x.deadline, models.Deadline.create_from_timestamp(util.u64_from_dto([2208867673, 28]))),
                lambda x: (x.height, 158159),
            ],
        },
        {
            'name': 'test_get_transaction_statuses',
            'response': responses.TRANSACTION_STATUSES["Ok"],
            'params': [['135B65FF4E9E90E2F3283D75E2AD3D45EC46729013786841E32904D5134FD2B9']],
            'method': 'get_transaction_statuses',
            'validation': [
                lambda x: (len(x), 1),
                lambda x: (isinstance(x[0], models.TransactionStatus), True),
            ],
        },
        {
            'name': 'test_announce',
            'response': responses.ANNOUNCE["Ok"],
            'params': [
                models.SignedTransaction(
                    payload='a70000004b94...',
                    hash='135B65FF4E9E90E2F3283D75E2AD3D45EC46729013786841E32904D5134FD2B9',
                    signer='0EB448D07C7CCB312989AC27AA052738FF589E2F83973F909B506B450DC5C4E2',
                    type=models.TransactionType.TRANSFER,
                    network_type=models.NetworkType.MIJIN_TEST,
                )
            ],
            'method': 'announce',
            'validation': [
                lambda x: (isinstance(x, models.TransactionAnnounceResponse), True),
                lambda x: (x.message, 'packet 9 was pushed to the network via /transaction'),
            ],
        },
        {
            'name': 'test_announce_partial',
            'response': responses.ANNOUNCE_PARTIAL["Ok"],
            'params': [
                models.SignedTransaction(
                    payload='a70000004b94...',
                    hash='135B65FF4E9E90E2F3283D75E2AD3D45EC46729013786841E32904D5134FD2B9',
                    signer='0EB448D07C7CCB312989AC27AA052738FF589E2F83973F909B506B450DC5C4E2',
                    type=models.TransactionType.TRANSFER,
                    network_type=models.NetworkType.MIJIN_TEST,
                )
            ],
            'method': 'announce_partial',
            'validation': [
                lambda x: (isinstance(x, models.TransactionAnnounceResponse), True),
                lambda x: (x.message, 'packet 500 was pushed to the network via /transaction/partial'),
            ],
        },
        {
            'name': 'test_announce_cosignature',
            'response': responses.ANNOUNCE_COSIGNATURE["Ok"],
            'params': [
                models.CosignatureSignedTransaction(
                    parent_hash='135B65FF4E9E90E2F3283D75E2AD3D45EC46729013786841E32904D5134FD2B9',
                    signature='3A6D4A8EE69C509F7D020C5DBCD3B7E9610B0571F2C7F14229D900A85D51E41EB52BCBEFFD1D95CB40C996540657DBA33090E27A3AA5E0D71F727A055B6D5403',
                    signer='0EB448D07C7CCB312989AC27AA052738FF589E2F83973F909B506B450DC5C4E2',
                )
            ],
            'method': 'announce_cosignature',
            'validation': [
                lambda x: (isinstance(x, models.TransactionAnnounceResponse), True),
                lambda x: (x.message, 'packet 501 was pushed to the network via /transaction/cosignature'),
            ],
        },
    ],
})
class TestTransactionHTTP(harness.TestCase):
    pass
