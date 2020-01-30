from xpxchain import models
from xpxchain import util
from xpxchain.models.transaction.recipient import Recipient
from tests import harness


class TestRecipient(harness.TestCase):

    def setUp(self):
        self.network_type = models.NetworkType.MIJIN_TEST
        self.address = models.Address("SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54")
        self.namespace_id = models.NamespaceId(0x84b3552d375ffa4b)
        self.address_dto = '90fa39ec47e05600afa74308a7ea607d145e371b5f4f1447bc'
        self.namespace_dto = '914bfa5f372d55b38400000000000000000000000000000000'
        self.address_catbuffer = util.unhexlify(self.address_dto)
        self.namespace_catbuffer = util.unhexlify(self.namespace_dto)

    def test_to_dto(self):
        self.assertEqual(self.address_dto, Recipient.to_dto(self.address, self.network_type))
        self.assertEqual(self.namespace_dto, Recipient.to_dto(self.namespace_id, self.network_type))

    def test_from_dto(self):
        self.assertEqual(self.address, Recipient.create_from_dto(self.address_dto, self.network_type))
        self.assertEqual(self.namespace_id, Recipient.create_from_dto(self.namespace_dto, self.network_type))

    def test_to_catbuffer(self):
        self.assertEqual(self.address_catbuffer, Recipient.to_catbuffer(self.address, self.network_type))
        self.assertEqual(self.namespace_catbuffer, Recipient.to_catbuffer(self.namespace_id, self.network_type))

    def test_create_from_catbuffer(self):
        self.assertEqual(self.address, Recipient.create_from_catbuffer(self.address_catbuffer, self.network_type))
        self.assertEqual(self.namespace_id, Recipient.create_from_catbuffer(self.namespace_catbuffer, self.network_type))
