from nem2 import models
from nem2.util import InterchangeFormat
from tests.harness import TestCase


class TestMosaicId(TestCase):

    def test_init(self):
        value = models.MosaicId(5)
        self.assertEqual(value.id, 5)

    def test_properties(self):
        value = models.MosaicId(5)
        self.assertEqual(value.id, 5)

        with self.assertRaises(AttributeError):
            value.id = 10

    def test_int(self):
        value = models.MosaicId(5)
        self.assertEqual(int(value), 5)

    def test_index(self):
        value = models.MosaicId(5)
        self.assertEqual(hex(value), "0x5")

    def test_repr(self):
        value = models.MosaicId(5)
        self.assertEqual(repr(value), "MosaicId(id=5)")

    def test_str(self):
        value = models.MosaicId(5)
        self.assertEqual(str(value), "MosaicId(id=5)")

    def test_eq(self):
        id1 = models.MosaicId(5)
        id2 = models.MosaicId(5)
        id3 = models.MosaicId(8)

        self.assertTrue(id1 == id1)
        self.assertTrue(id1 == id2)
        self.assertFalse(id1 == id3)
        self.assertTrue(id2 == id2)
        self.assertFalse(id2 == id3)
        self.assertTrue(id3 == id3)

    def test_to_dto(self):
        value = models.MosaicId(5)
        self.assertEqual(value.to_dto(), 5)

    def test_from_dto(self):
        value = models.MosaicId.from_dto(5)
        self.assertEqual(value.id, 5)

    def test_to_catbuffer(self):
        value = models.MosaicId(5)
        self.assertEqual(value.to_catbuffer(), b"\x05\x00\x00\x00\x00\x00\x00\x00")

    def test_from_catbuffer(self):
        value = models.MosaicId.from_catbuffer(b"\x05\x00\x00\x00\x00\x00\x00\x00")
        self.assertEqual(value.id, 5)

    def test_serialize(self):
        value = models.MosaicId(5)
        self.assertEqual(value.serialize(InterchangeFormat.DTO), value.to_dto())
        self.assertEqual(value.serialize(InterchangeFormat.CATBUFFER), value.to_catbuffer())

    def test_deserialize(self):
        value = models.MosaicId(5)
        self.assertEqual(models.MosaicId.deserialize(value.to_dto(), InterchangeFormat.DTO), value)
        self.assertEqual(models.MosaicId.deserialize(value.to_catbuffer(), InterchangeFormat.CATBUFFER), value)


class TestMosaic(TestCase):

    def test_init(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(value.id, models.MosaicId(5))
        self.assertEqual(value.amount, 1000)

    def test_properties(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(value.id, models.MosaicId(5))
        self.assertEqual(value.amount, 1000)

        with self.assertRaises(AttributeError):
            value.id = models.MosaicId(10)
        with self.assertRaises(AttributeError):
            value.id.id = 10
        with self.assertRaises(AttributeError):
            value.amount = 10

    def test_repr(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(repr(value), "Mosaic(id=MosaicId(id=5), amount=1000)")

    def test_str(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(str(value), "Mosaic(id=MosaicId(id=5), amount=1000)")

    def test_eq(self):
        m1 = models.Mosaic(models.MosaicId(5), 1000)
        m2 = models.Mosaic(models.MosaicId(5), 1000)
        m3 = models.Mosaic(models.MosaicId(5), 500)
        m4 = models.Mosaic(models.MosaicId(10), 1000)

        self.assertTrue(m1 == m1)
        self.assertTrue(m1 == m2)
        self.assertFalse(m1 == m3)
        self.assertFalse(m1 == m4)
        self.assertTrue(m2 == m2)
        self.assertFalse(m2 == m3)
        self.assertFalse(m2 == m4)
        self.assertTrue(m3 == m3)
        self.assertFalse(m3 == m4)
        self.assertTrue(m4 == m4)

    def test_to_dto(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(value.to_dto(), {'amount': 1000, 'id': 5})

    def test_from_dto(self):
        value = models.Mosaic.from_dto({'amount': 1000, 'id': 5})
        self.assertEqual(value.id, models.MosaicId(5))
        self.assertEqual(value.amount, 1000)

    def test_to_catbuffer(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(value.to_catbuffer(), b"\x05\x00\x00\x00\x00\x00\x00\x00\xe8\x03\x00\x00\x00\x00\x00\x00")

    def test_from_catbuffer(self):
        value = models.Mosaic.from_catbuffer(b"\x05\x00\x00\x00\x00\x00\x00\x00\xe8\x03\x00\x00\x00\x00\x00\x00")
        self.assertEqual(value.id, models.MosaicId(5))
        self.assertEqual(value.amount, 1000)

    def test_serialize(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(value.serialize(InterchangeFormat.DTO), value.to_dto())
        self.assertEqual(value.serialize(InterchangeFormat.CATBUFFER), value.to_catbuffer())

    def test_deserialize(self):
        value = models.Mosaic(models.MosaicId(5), 1000)
        self.assertEqual(models.Mosaic.deserialize(value.to_dto(), InterchangeFormat.DTO), value)
        self.assertEqual(models.Mosaic.deserialize(value.to_catbuffer(), InterchangeFormat.CATBUFFER), value)
