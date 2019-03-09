import datetime
import random

from nem2 import util
from nem2 import models
from tests import harness


def psuedo_entropy(size: int) -> bytes:
    return bytes([random.randint(0, 255) for _ in range(size)])


class TestAggregateTransactionInfo(harness.TestCase):

    def setUp(self):
        self.transaction_info = models.AggregateTransactionInfo(
            height=18160,
            index=0,
            id="5A0069D83F17CF0001777E56",
            aggregate_hash="3D28C804EDD07D5A728E5C5FFEC01AB07AFA5766AE6997B38526D36015A4D006",
            aggregate_id="5A0069D83F17CF0001777E55",
        )
        self.dto = {
            "height": [18160, 0],
            "aggregateHash": "3D28C804EDD07D5A728E5C5FFEC01AB07AFA5766AE6997B38526D36015A4D006",
            "aggregateId": "5A0069D83F17CF0001777E55",
            "index": 0,
            "id": "5A0069D83F17CF0001777E56"
        }

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.transaction_info.__dict__

    def test_to_dto(self):
        self.assertEqual(self.transaction_info.to_dto(), self.dto)

    def test_from_dto(self):
        value = models.AggregateTransactionInfo.from_dto(self.dto)
        self.assertEqual(value, self.transaction_info)


class TestDeadline(harness.TestCase):

    def setUp(self):
        self.datetime = datetime.datetime(2019, 3, 8, 0, 18, 57)
        self.dto = [1552004337, 0]

    def test_slots(self):
        value = models.Deadline(self.datetime)
        with self.assertRaises(TypeError):
            value.__dict__

    def test_create(self):
        with self.assertRaises(ValueError):
            models.Deadline.create(0)
        with self.assertRaises(ValueError):
            models.Deadline.create(-1)
        with self.assertRaises(ValueError):
            models.Deadline.create(24, models.ChronoUnit.HOURS)

        models.Deadline.create(2000, models.ChronoUnit.SECONDS)
        models.Deadline.create(200, models.ChronoUnit.MINUTES)
        models.Deadline.create(23, models.ChronoUnit.HOURS)

    def test_to_dto(self):
        value = models.Deadline(self.datetime)
        self.assertEqual(value.to_dto(), self.dto)
        self.assertEqual(value.toDto(), value.to_dto())

    def test_from_dto(self):
        value = models.Deadline.from_dto(self.dto)
        self.assertEqual(value.deadline, self.datetime)
        self.assertEqual(value, models.Deadline.fromDto(self.dto))


class TestHashType(harness.TestCase):

    def setUp(self):
        self.digest_64 = (
            models.HashType.SHA3_256,
            models.HashType.KECCAK_256,
            models.HashType.HASH_256
        )
        self.digest_40 = (models.HashType.HASH_160,)

    def test_validate(self):
        hash_40 = util.hexlify(psuedo_entropy(20))
        hash_64 = util.hexlify(psuedo_entropy(32))

        for enum in self.digest_64:
            self.assertFalse(enum.validate(hash_40))
            self.assertTrue(enum.validate(hash_64))

        for enum in self.digest_40:
            self.assertTrue(enum.validate(hash_40))
            self.assertFalse(enum.validate(hash_64))

        hash_40 = hash_40[:-1] + 'x'
        hash_64 = hash_64[:-1] + 'x'

        for enum in self.digest_64:
            self.assertFalse(enum.validate(hash_40))
            self.assertFalse(enum.validate(hash_64))

        for enum in self.digest_40:
            self.assertFalse(enum.validate(hash_40))
            self.assertFalse(enum.validate(hash_64))


class TestMessage(harness.TestCase):

    def test_create(self):
        with self.assertRaises(NotImplementedError):
            models.Message.create(b'Hello world!')

    def test_dto(self):
        with self.assertRaises(NotImplementedError):
            models.Message.from_dto(b'Hello world!')


class TestMessageType(harness.TestCase):

    def test_description(self):
        self.assertEqual(models.MessageType.PLAIN.description(), 'Plain message.')


class TestPlainMessage(harness.TestCase):

    def test_init(self):
        value = models.PlainMessage(b'Hello world!')
        self.assertEqual(value.type, models.MessageType.PLAIN)
        self.assertEqual(value.payload, b'Hello world!')

    def test_slots(self):
        value = models.PlainMessage.create(b'Hello world!')
        with self.assertRaises(TypeError):
            value.__dict__

    def test_create(self):
        value = models.PlainMessage.create(b'Hello world!')
        self.assertEqual(value.type, models.MessageType.PLAIN)
        self.assertEqual(value.payload, b'Hello world!')

    def test_to_dto(self):
        value = models.PlainMessage.create(b'Hello world!')
        self.assertEqual(value.to_dto(), '48656c6c6f20776f726c6421')

    def test_from_dto(self):
        value = models.PlainMessage.from_dto('48656c6c6f20776f726c6421')
        self.assertEqual(value.type, models.MessageType.PLAIN)
        self.assertEqual(value.payload, b'Hello world!')


class TestSecretProofTransaction(harness.TestCase):

    def setUp(self):
        self.deadline = models.Deadline.create()
        self.hash_type = models.HashType.SHA3_256
        self.proof = 'b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.secret = util.hashlib.sha3_256(util.unhexlify(self.proof)).hexdigest()
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transaction = models.SecretProofTransaction.create(
            deadline=self.deadline,
            hash_type=self.hash_type,
            secret=self.secret,
            proof=self.proof,
            network_type=self.network_type,
        )
        # TODO(ahuszagh) Need the signer...
        self.catbuffer = b''

    def test_init(self):
        self.assertEqual(self.transaction.deadline, self.deadline)
        self.assertEqual(self.transaction.hash_type, self.hash_type)
        self.assertEqual(self.transaction.secret, self.secret)
        self.assertEqual(self.transaction.proof, self.proof)
        self.assertEqual(self.transaction.network_type, self.network_type)

#    def test_catbuffer(self):
#        import pdb; pdb.set_trace()
#        catbuffer = self.transaction.to_catbuffer()


class TestTransactionAnnounceResponse(harness.TestCase):

    def setUp(self):
        self.response = models.TransactionAnnounceResponse('Hello world!')
        self.dto = {'message': 'Hello world!'}

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.response.__dict__

    def test_to_dto(self):
        self.assertEqual(self.response.to_dto(), self.dto)

    def test_from_dto(self):
        value = models.TransactionAnnounceResponse.from_dto(self.dto)
        self.assertEqual(value, self.response)


class TestTransactionInfo(harness.TestCase):

    def setUp(self):
        self.transaction_info = models.TransactionInfo(
            height=1,
            index=0,
            id="5C7C06FF5CC1FE000176FA12",
            hash="B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
            merkle_component_hash="B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
        )
        self.dto = {
            "height": [1, 0],
            "hash": "B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
            "merkleComponentHash": "B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
            "index": 0,
            "id": "5C7C06FF5CC1FE000176FA12"
        }

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.transaction_info.__dict__

    def test_init(self):
        models.TransactionInfo(1, 0, "5C7C06FF5CC1FE000176FA12")
        models.TransactionInfo(1, 0, "5C7C06FF5CC1FE000176FA12", None)
        models.TransactionInfo(1, 0, "5C7C06FF5CC1FE000176FA12", None, None)

    def test_to_dto(self):
        self.assertEqual(self.transaction_info.to_dto(), self.dto)

    def test_from_dto(self):
        value = models.TransactionInfo.from_dto(self.dto)
        self.assertEqual(value, self.transaction_info)


class TestTransactionStatus(harness.TestCase):

    def setUp(self):
        self.transaction_status = models.TransactionStatus(
            group=models.TransactionStatusGroup.CONFIRMED,
            status="Success",
            hash="B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
            deadline=models.Deadline.from_timestamp(1),
            height=1
        )
        self.dto = {
            "group": "confirmed",
            "status": "Success",
            "hash": "B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
            "deadline": [1, 0],
            "height": [1, 0]
        }

    def test_to_dto(self):
        self.assertEqual(self.transaction_status.to_dto(), self.dto)

    def test_from_dto(self):
        value = models.TransactionStatus.from_dto(self.dto)
        self.assertEqual(value, self.transaction_status)


class TestTransactionStatusGroup(harness.TestCase):

    def setUp(self):
        self.failed = models.TransactionStatusGroup.FAILED
        self.unconfirmed = models.TransactionStatusGroup.UNCONFIRMED
        self.confirmed = models.TransactionStatusGroup.CONFIRMED

    def test_description(self):
        self.assertEqual(self.failed.description(), 'Transaction failed.')

    def test_to_dto(self):
        self.assertEqual(self.failed.to_dto(), "failed")
        self.assertEqual(self.unconfirmed.to_dto(), "unconfirmed")
        self.assertEqual(self.confirmed.to_dto(), "confirmed")

    def test_from_dto(self):
        value = models.TransactionStatusGroup.from_dto("failed")
        self.assertEqual(self.failed, value)


class TestTransactionType(harness.TestCase):

    def setUp(self):
        self.transfer = models.TransactionType.TRANSFER

    def test_description(self):
        self.assertEqual(self.transfer.description(), "Transfer Transaction transaction type.")
