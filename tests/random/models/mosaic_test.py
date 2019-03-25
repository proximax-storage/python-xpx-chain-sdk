import binascii
import string

from nem2 import models
from tests import harness


class TestMosaic(harness.TestCase):

    @harness.randomize
    def test_valid(self, id: harness.U64, amount: harness.U64):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.Mosaic(models.MosaicId(id), amount)
        dto = model.to_dto(network_type)
        self.assertEqual(model, models.Mosaic.from_dto(dto, network_type))

    @harness.randomize(
        id={'min_value': -1 << 32, 'max_value': -1},
        amount={'min_value': -1 << 32, 'max_value': -1},
    )
    def test_invalid(self, id: int, amount: int):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.Mosaic(models.MosaicId(id), amount)
        with self.assertRaises(ArithmeticError):
            model.to_dto(network_type)


class TestMosaicId(harness.TestCase):

    @harness.randomize
    def test_valid(self, id: harness.U64):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.MosaicId(id)
        dto = model.to_dto(network_type)
        self.assertEqual(model, models.MosaicId.from_dto(dto, network_type))

    @harness.randomize(id={'min_value': -1 << 32, 'max_value': -1})
    def test_invalid(self, id: int):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.MosaicId(id)
        with self.assertRaises(ArithmeticError):
            model.to_dto(network_type)


class TestMosaicName(harness.TestCase):

    @harness.randomize(nonce={'fixed_length': 4})
    def test_valid_bytes(self, nonce: bytes):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.MosaicNonce(nonce)
        dto = model.to_dto(network_type)
        self.assertEqual(model, models.MosaicNonce.from_dto(dto, network_type))
        catbuffer = model.to_catbuffer(network_type)
        self.assertEqual(model, models.MosaicNonce.from_catbuffer(catbuffer, network_type))

    @harness.randomize(nonce={'letters': string.hexdigits, 'fixed_length': 8})
    def test_valid_str(self, nonce: str):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.MosaicNonce(nonce)
        dto = model.to_dto(network_type)
        self.assertEqual(model, models.MosaicNonce.from_dto(dto, network_type))
        catbuffer = model.to_catbuffer(network_type)
        self.assertEqual(model, models.MosaicNonce.from_catbuffer(catbuffer, network_type))

    @harness.randomize
    def test_valid_int(self, nonce: harness.U32):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.MosaicNonce(nonce)
        dto = model.to_dto(network_type)
        self.assertEqual(model, models.MosaicNonce.from_dto(dto, network_type))
        catbuffer = model.to_catbuffer(network_type)
        self.assertEqual(model, models.MosaicNonce.from_catbuffer(catbuffer, network_type))

    @harness.randomize(nonce={'min_length': 0, 'max_length': 3})
    def test_invalid_bytes(self, nonce: bytes):
        with self.assertRaises(ValueError):
            models.MosaicNonce(nonce)

    @harness.randomize(nonce={'letters': string.hexdigits, 'min_length': 0, 'max_length': 7})
    def test_invalid_str(self, nonce: str):
        with self.assertRaises((ValueError, binascii.Error)):
            models.MosaicNonce(nonce)

    @harness.randomize(nonce={'min_value': -1 << 32, 'max_value': -1})
    def test_invalid_int(self, nonce: int):
        with self.assertRaises(OverflowError):
            models.MosaicNonce(nonce)

# TODO(ahuszagh) Add mosaic properties after stabilized.
