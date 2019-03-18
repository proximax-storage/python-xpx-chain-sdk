import datetime
import random

from nem2 import util
from nem2 import models
from tests import harness


def psuedo_entropy(size: int) -> bytes:
    return bytes([random.randint(0, 255) for _ in range(size)])


class TestAddressAliasTransaction(harness.TestCase):
    pass        # TODO(ahuszagh) Implement


class TestAddressAliasInnerTransaction(harness.TestCase):
    pass        # TODO(ahuszagh) Implement


class TestAggregateTransactionCosignature(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.signature = '5780C8DF9D46BA2BCF029DCC5D3BF55FE1CB5BE7ABCF30387C4637DDEDFC2152703CA0AD95F21BB9B942F3CC52FCFC2064C7B84CF60D1A9E69195F1943156C07'
        self.public_key = 'A5F82EC8EBB341427B6785C8111906CD0DF18838FB11B51CE0E18B5E79DFF630'
        self.signer = models.PublicAccount.create_from_public_key(self.public_key, self.network_type)
        self.cosignature = models.AggregateTransactionCosignature(self.signature, self.signer)
        self.dto = {
            'signature': self.signature,
            'signer': self.public_key,
        }

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.cosignature.__dict__

    def test_to_dto(self):
        self.assertEqual(self.cosignature.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.cosignature, models.AggregateTransactionCosignature.from_dto(self.dto, self.network_type))


class TestAggregateTransactionInfo(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
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
        self.assertEqual(self.transaction_info.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.transaction_info, models.AggregateTransactionInfo.from_dto(self.dto, self.network_type))


class TestAliasTransaction(harness.TestCase):
    pass        # TODO(ahuszagh) Implement


class TestCosignatureSignedTransaction(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.parent_hash = '671653C94E2254F2A23EFEDB15D67C38332AED1FBD24B063C0A8E675582B6A96'
        self.signature = '939673209A13FF82397578D22CC96EB8516A6760C894D9B7535E3A1E068007B9255CFA9A914C97142A7AE18533E381C846B69D2AE0D60D1DC8A55AD120E2B606'
        self.signer = '7681ED5023141D9CDCF184E5A7B60B7D466739918ED5DA30F7E71EA7B86EFF2D'
        self.cosignature = models.CosignatureSignedTransaction(self.parent_hash, self.signature, self.signer)
        self.dto = {
            'parentHash': self.parent_hash,
            'signature': self.signature,
            'signer': self.signer,
        }

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.cosignature.__dict__

    def test_to_dto(self):
        self.assertEqual(self.cosignature.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.cosignature, models.CosignatureSignedTransaction.from_dto(self.dto, self.network_type))


class TestDeadline(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.datetime = datetime.datetime(2019, 3, 8, 0, 18, 57)
        self.deadline = models.Deadline(self.datetime)
        self.dto = [1552004337, 0]
        self.catbuffer = b'\xf1\xb4\x81\\\x00\x00\x00\x00'

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.deadline.__dict__

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
        self.assertEqual(self.deadline.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.deadline, models.Deadline.from_dto(self.dto, self.network_type))


class TestHashType(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.digest_64 = (
            models.HashType.SHA3_256,
            models.HashType.KECCAK_256,
            models.HashType.HASH_256
        )
        self.digest_40 = (models.HashType.HASH_160,)
        self.hash = models.HashType.SHA3_256
        self.dto = 0
        self.catbuffer = b'\x00'

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

    def test_to_dto(self):
        self.assertEqual(self.hash.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.hash, models.HashType.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.hash.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.hash, models.HashType.from_catbuffer(self.catbuffer, self.network_type))


class TestInnnerTransaction(harness.TestCase):

    def test_catbuffer_size_shared(self):
        self.assertEqual(models.InnerTransaction.catbuffer_size_shared(), 40)


class TestMessage(harness.TestCase):

    def test_create(self):
        with self.assertRaises(NotImplementedError):
            models.Message.create(b'Hello world!')

    def test_dto(self):
        with self.assertRaises(NotImplementedError):
            models.Message.from_dto(b'Hello world!', models.NetworkType.MIJIN_TEST)


class TestMessageType(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.plain = models.MessageType.PLAIN
        self.dto = 0
        self.catbuffer = b'\x00'

    def test_description(self):
        self.assertEqual(self.plain.description(), 'Plain message.')

    def test_to_dto(self):
        self.assertEqual(self.plain.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.plain, models.MessageType.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.plain.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.plain, models.MessageType.from_catbuffer(self.catbuffer, self.network_type))


class TestMosaicAliasTransaction(harness.TestCase):
    pass        # TODO(ahuszagh) Implement


class TestMosaicAliasInnerTransaction(harness.TestCase):
    pass        # TODO(ahuszagh) Implement


class TestMultisigCosignatoryModificationType(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.add = models.MultisigCosignatoryModificationType.ADD
        self.remove = models.MultisigCosignatoryModificationType.REMOVE
        self.dto = 0
        self.catbuffer = b'\x00'

    def test_description(self):
        self.assertEqual(self.add.description(), 'Add cosignatory.')
        self.assertEqual(self.remove.description(), 'Remove cosignatory.')

    def test_to_dto(self):
        self.assertEqual(self.add.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.add, models.MultisigCosignatoryModificationType.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.add.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.add, models.MultisigCosignatoryModificationType.from_catbuffer(self.catbuffer, self.network_type))


class TestPlainMessage(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.message = models.PlainMessage(b'Hello world!')
        self.dto = '48656c6c6f20776f726c6421'
        self.catbuffer = b'Hello world!'

    def test_init(self):
        self.assertEqual(self.message.type, models.MessageType.PLAIN)
        self.assertEqual(self.message.payload, b'Hello world!')

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.message.__dict__

    def test_create(self):
        self.assertEqual(self.message.type, models.MessageType.PLAIN)
        self.assertEqual(self.message.payload, b'Hello world!')

    def test_to_dto(self):
        self.assertEqual(self.message.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.message, models.PlainMessage.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.message.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.message, models.PlainMessage.from_catbuffer(self.catbuffer, self.network_type))


class TestSecretProofTransaction(harness.TestCase):

    def setUp(self):
        self.deadline = models.Deadline(datetime.datetime(2019, 3, 8, 0, 18, 57))
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
        private_key = "97131746d864f4c9001b1b86044d765ba08d7fddc7a0fb3abbc8d111aa26cdca"
        network_type = models.NetworkType.MIJIN_TEST
        self.signer = models.Account.create_from_private_key(private_key, network_type)
        # TODO(ahuszagh)
        # Is embedded correct?
        self.catbuffer = 'bb000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.payload = 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.hash = 'd8949c87755cfd2c003fec4e1bd4aadb00b3f4838fc5ce7ffeded9385805fcdd'
        self.embedded = '6b0000001b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd5895501905242009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'

    def test_init(self):
        self.assertEqual(self.transaction.deadline, self.deadline)
        self.assertEqual(self.transaction.hash_type, self.hash_type)
        self.assertEqual(self.transaction.secret, self.secret)
        self.assertEqual(self.transaction.proof, self.proof)
        self.assertEqual(self.transaction.network_type, self.network_type)

    def test_catbuffer(self):
        catbuffer = self.transaction.to_catbuffer()
        self.assertEqual(self.catbuffer, util.hexlify(catbuffer))

    def test_sign_with(self):
        signed_transaction = self.transaction.sign_with(self.signer)
        self.assertEqual(util.hexlify(signed_transaction.payload), self.payload)
        self.assertEqual(signed_transaction.hash, self.hash)
        self.assertEqual(signed_transaction.signer, self.signer.public_key)
        self.assertEqual(signed_transaction.type, models.TransactionType.SECRET_PROOF)
        self.assertEqual(signed_transaction.network_type, self.signer.network_type)

    def test_to_aggregate(self):
        inner = self.transaction.to_aggregate(self.signer.public_account)
        catbuffer = inner.to_catbuffer()
        self.assertEqual(self.embedded, util.hexlify(catbuffer))

        with self.assertRaises(TypeError):
            inner.__dict__


class TestSecretProofInnerTransaction(harness.TestCase):
    pass        # TODO(ahuszagh) Implement


class TestSignedTransaction(harness.TestCase):

    def setUp(self):
        self.payload = 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.hash = 'd8949c87755cfd2c003fec4e1bd4aadb00b3f4838fc5ce7ffeded9385805fcdd'
        self.signer = '1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955'
        self.type = models.TransactionType.SECRET_PROOF
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transaction = models.SignedTransaction(self.payload, self.hash, self.signer, self.type, self.network_type)

    def test_init(self):
        self.assertEqual(self.transaction.payload, self.payload)
        self.assertEqual(self.transaction.hash, self.hash)
        self.assertEqual(self.transaction.signer, self.signer)
        self.assertEqual(self.transaction.type, self.type)
        self.assertEqual(self.transaction.network_type, self.network_type)


class TestTransaction(harness.TestCase):

    def test_transaction_hash(self):
        hash = 'd8949c87755cfd2c003fec4e1bd4aadb00b3f4838fc5ce7ffeded9385805fcdd'
        transaction = 'bb000000d0092d8eaf91c07069eeef6651cd313e792b27d2cb31473ceaac40f78ee2121acb5f665826083b87b374c9eb67aefef6b8cf74f0298820a9143b34055e15900c1b153f8b76ef60a4bfe152f4de3698bd230bac9dc239d4e448715aa46bd58955019052420000000000000000f1b4815c00000000009b3155b37159da50aa52d5967c509b410f5a36a3b1e31ecb5ac76675d79b4a5e2000b778a39a3663719dfc5e48c9d78431b1e45c2af9df538782bf199c189dabeac7'
        self.assertEqual(hash, models.Transaction.transaction_hash(transaction))

    def test_catbuffer_size_shared(self):
        self.assertEqual(models.Transaction.catbuffer_size_shared(), 120)


class TestTransactionAnnounceResponse(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.response = models.TransactionAnnounceResponse('Hello world!')
        self.dto = {'message': 'Hello world!'}

    def test_slots(self):
        with self.assertRaises(TypeError):
            self.response.__dict__

    def test_to_dto(self):
        self.assertEqual(self.response.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.response, models.TransactionAnnounceResponse.from_dto(self.dto, self.network_type))


class TestTransactionInfo(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
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
        self.assertEqual(self.transaction_info.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.transaction_info, models.TransactionInfo.from_dto(self.dto, self.network_type))


class TestTransactionStatus(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
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
        self.assertEqual(self.transaction_status.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.transaction_status, models.TransactionStatus.from_dto(self.dto, self.network_type))


class TestTransactionStatusError(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.hash = "B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5"
        self.status = "Success"
        self.deadline = models.Deadline.from_timestamp(1)
        self.error = models.TransactionStatusError(self.hash, self.status, self.deadline)
        self.dto = {
            "hash": "B2635223DB45CFBB4E21CDFC359FE7F222A6E5F6000C99CA9E729DB02E6661F5",
            "status": "Success",
            "deadline": [1, 0],
        }

    def test_to_dto(self):
        self.assertEqual(self.error.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.error, models.TransactionStatusError.from_dto(self.dto, self.network_type))


class TestTransactionStatusGroup(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.failed = models.TransactionStatusGroup.FAILED
        self.unconfirmed = models.TransactionStatusGroup.UNCONFIRMED
        self.confirmed = models.TransactionStatusGroup.CONFIRMED

    def test_description(self):
        self.assertEqual(self.failed.description(), 'Transaction failed.')

    def test_to_dto(self):
        self.assertEqual(self.failed.to_dto(self.network_type), "failed")
        self.assertEqual(self.unconfirmed.to_dto(self.network_type), "unconfirmed")
        self.assertEqual(self.confirmed.to_dto(self.network_type), "confirmed")

    def test_from_dto(self):
        self.assertEqual(self.failed, models.TransactionStatusGroup.from_dto("failed", self.network_type))


class TestTransactionType(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transfer = models.TransactionType.TRANSFER
        self.dto = 0x4154
        self.catbuffer = b'\x54\x41'

    def test_description(self):
        self.assertEqual(self.transfer.description(), "Transfer Transaction transaction type.")

    def test_to_dto(self):
        self.assertEqual(self.transfer.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.transfer, models.TransactionType.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.transfer.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.transfer, models.TransactionType.from_catbuffer(self.catbuffer, self.network_type))


class TestTransactionVersion(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.transfer = models.TransactionVersion.TRANSFER
        self.dto = 3
        self.catbuffer = b'\x03'

    def test_to_dto(self):
        self.assertEqual(self.transfer.to_dto(self.network_type), self.dto)

    def test_from_dto(self):
        self.assertEqual(self.transfer, models.TransactionVersion.from_dto(self.dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.transfer.to_catbuffer(self.network_type), self.catbuffer)

    def test_from_catbuffer(self):
        self.assertEqual(self.transfer, models.TransactionVersion.from_catbuffer(self.catbuffer, self.network_type))


class TestTransferTransaction(harness.TestCase):
    pass        # TODO(ahuszagh) Implement


class TestTransferInnerTransaction(harness.TestCase):
    pass        # TODO(ahuszagh) Implement
