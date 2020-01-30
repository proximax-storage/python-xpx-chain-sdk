import binascii
import string

from xpxchain import models
from tests import harness


class TestMosaic(harness.TestCase):

    @harness.randomize
    def test_valid(self, id: harness.U64, amount: harness.U64):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.Mosaic(models.MosaicId(id), amount)
        dto = model.to_dto(network_type)
        self.assertEqual(model, models.Mosaic.create_from_dto(dto, network_type))

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
        model = models.Mosaic(models.MosaicId(id), 1)
        dto = model.to_dto(network_type)
        self.assertEqual(model, models.Mosaic.create_from_dto(dto, network_type))

    @harness.randomize(id={'min_value': -1 << 32, 'max_value': -1})
    def test_invalid(self, id: int):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.Mosaic(models.MosaicId(id), 1)
        with self.assertRaises(ArithmeticError):
            model.to_dto(network_type)


class TestMosaicNonce(harness.TestCase):

    @harness.randomize(nonce={'fixed_length': 4})
    def test_valid_bytes(self, nonce: bytes):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.MosaicNonce(nonce)
        dto = model.to_dto(network_type)
        self.assertEqual(model, models.MosaicNonce.create_from_dto(dto, network_type))
        catbuffer = model.to_catbuffer(network_type)
        self.assertEqual(model, models.MosaicNonce.create_from_catbuffer(catbuffer, network_type))

    @harness.randomize(nonce={'letters': string.hexdigits, 'fixed_length': 8})
    def test_valid_str(self, nonce: str):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.MosaicNonce(nonce)
        dto = model.to_dto(network_type)
        self.assertEqual(model, models.MosaicNonce.create_from_dto(dto, network_type))
        catbuffer = model.to_catbuffer(network_type)
        self.assertEqual(model, models.MosaicNonce.create_from_catbuffer(catbuffer, network_type))

    @harness.randomize
    def test_valid_int(self, nonce: harness.U32):
        network_type = models.NetworkType.MIJIN_TEST
        model = models.MosaicNonce(nonce)
        dto = model.to_dto(network_type)
        self.assertEqual(model, models.MosaicNonce.create_from_dto(dto, network_type))
        catbuffer = model.to_catbuffer(network_type)
        self.assertEqual(model, models.MosaicNonce.create_from_catbuffer(catbuffer, network_type))

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


class TestMosaicProperties(harness.TestCase):

    @harness.randomize(divisibility={'min_value': 0, 'max_value': 6})
    def test_create(
        self,
        supply_mutable: bool,
        transferable: bool,
        levy_mutable: bool,
        divisibility: int,
        duration: harness.U64,
    ):
        properties = models.MosaicProperties.create(
            supply_mutable=supply_mutable,
            transferable=transferable,
            levy_mutable=levy_mutable,
            divisibility=divisibility,
            duration=duration,
        )
        self.assertEqual(properties.supply_mutable, supply_mutable)
        self.assertEqual(properties.transferable, transferable)
        self.assertEqual(properties.levy_mutable, levy_mutable)
        self.assertLessEqual(properties.flags, 7)
        self.assertEqual(properties.divisibility, divisibility)
        self.assertEqual(properties.duration, duration)
        self.assertEqual(properties, models.MosaicProperties.create_from_dto(properties.to_dto()))

    @harness.randomize(divisibility={'min_value': 7, 'max_value': 1 << 31})
    def test_invalid_divisibility(self, divisibility: int):
        with self.assertRaises(ValueError):
            models.MosaicProperties.create(divisibility=divisibility)
        with self.assertRaises(ValueError):
            models.MosaicProperties.create(divisibility=-divisibility)


# TODO(ahuszagh) Add supply type...
# TODO(ahuszagh) Add network currency type...
# TODO(ahuszagh) Add network harvest type...
