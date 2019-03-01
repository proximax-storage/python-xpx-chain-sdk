from nem2.models import blockchain
from tests.harness import TestCase


class TestNetworkType(TestCase):

    def setUp(self):
        self.main_net = blockchain.NetworkType.MAIN_NET
        self.test_net = blockchain.NetworkType.TEST_NET
        self.mijin = blockchain.NetworkType.MIJIN
        self.mijin_test = blockchain.NetworkType.MIJIN_TEST

    def test_values(self):
        self.assertEqual(self.main_net, 0x68)
        self.assertEqual(self.test_net, 0x98)
        self.assertEqual(self.mijin, 0x60)
        self.assertEqual(self.mijin_test, 0x90)

    def test_description(self):
        self.assertEqual(self.main_net.description(), "Main network")
        self.assertEqual(self.test_net.description(), "Test network")
        self.assertEqual(self.mijin.description(), "Mijin network")
        self.assertEqual(self.mijin_test.description(), "Mijin test network")

    def test_identifier(self):
        self.assertEqual(self.main_net.identifier(), b"N")
        self.assertEqual(self.test_net.identifier(), b"T")
        self.assertEqual(self.mijin.identifier(), b"M")
        self.assertEqual(self.mijin_test.identifier(), b"S")

    def test_create_from_identifier(self):

        def create(address: str):
            return blockchain.NetworkType.create_from_identifier(address)

        self.assertEqual(self.main_net, create(b"N"))
        self.assertEqual(self.test_net, create(b"T"))
        self.assertEqual(self.mijin, create(b"M"))
        self.assertEqual(self.mijin_test, create(b"S"))

        with self.assertRaises(KeyError):
            create(b"F")

    def test_create_from_raw_address(self):

        def create(address: str):
            return blockchain.NetworkType.create_from_raw_address(address)

        self.assertEqual(self.main_net, create("ND5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54"))
        self.assertEqual(self.test_net, create("TD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54"))
        self.assertEqual(self.mijin, create("MD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54"))
        self.assertEqual(self.mijin_test, create("SD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54"))

        with self.assertRaises(KeyError):
            create("FD5DT3CH4BLABL5HIMEKP2TAPUKF4NY3L5HRIR54")
