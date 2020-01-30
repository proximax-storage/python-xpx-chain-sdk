from xpxchain.util import bit
from tests import harness


class BitTest(harness.TestCase):

    def test_set(self):
        x: int = 0b10110010
        y: int = 0b01001101

        self.assertEqual(bit.set(x, 0), 0b10110011)
        self.assertEqual(bit.set(x, 1), 0b10110010)
        self.assertEqual(bit.set(x, 2), 0b10110110)
        self.assertEqual(bit.set(x, 3), 0b10111010)
        self.assertEqual(bit.set(x, 4), 0b10110010)
        self.assertEqual(bit.set(x, 5), 0b10110010)
        self.assertEqual(bit.set(x, 6), 0b11110010)
        self.assertEqual(bit.set(x, 7), 0b10110010)

        self.assertEqual(bit.set(y, 0), 0b01001101)
        self.assertEqual(bit.set(y, 1), 0b01001111)
        self.assertEqual(bit.set(y, 2), 0b01001101)
        self.assertEqual(bit.set(y, 3), 0b01001101)
        self.assertEqual(bit.set(y, 4), 0b01011101)
        self.assertEqual(bit.set(y, 5), 0b01101101)
        self.assertEqual(bit.set(y, 6), 0b01001101)
        self.assertEqual(bit.set(y, 7), 0b11001101)

    def test_clear(self):
        x: int = 0b10110010
        y: int = 0b01001101

        self.assertEqual(bit.clear(x, 0), 0b10110010)
        self.assertEqual(bit.clear(x, 1), 0b10110000)
        self.assertEqual(bit.clear(x, 2), 0b10110010)
        self.assertEqual(bit.clear(x, 3), 0b10110010)
        self.assertEqual(bit.clear(x, 4), 0b10100010)
        self.assertEqual(bit.clear(x, 5), 0b10010010)
        self.assertEqual(bit.clear(x, 6), 0b10110010)
        self.assertEqual(bit.clear(x, 7), 0b00110010)

        self.assertEqual(bit.clear(y, 0), 0b01001100)
        self.assertEqual(bit.clear(y, 1), 0b01001101)
        self.assertEqual(bit.clear(y, 2), 0b01001001)
        self.assertEqual(bit.clear(y, 3), 0b01000101)
        self.assertEqual(bit.clear(y, 4), 0b01001101)
        self.assertEqual(bit.clear(y, 5), 0b01001101)
        self.assertEqual(bit.clear(y, 6), 0b00001101)
        self.assertEqual(bit.clear(y, 7), 0b01001101)

    def test_assign(self):
        x: int = 0b10110010
        y: int = 0b01001101

        self.assertEqual(bit.set(x, 0), bit.assign(x, 0, True))
        self.assertEqual(bit.clear(x, 0), bit.assign(x, 0, False))
        self.assertEqual(bit.set(y, 0), bit.assign(y, 0, True))
        self.assertEqual(bit.clear(y, 0), bit.assign(y, 0, False))

    def test_toggle(self):
        x: int = 0b10110010
        y: int = 0b01001101

        self.assertEqual(bit.toggle(x, 0), 0b10110011)
        self.assertEqual(bit.toggle(x, 1), 0b10110000)
        self.assertEqual(bit.toggle(x, 2), 0b10110110)
        self.assertEqual(bit.toggle(x, 3), 0b10111010)
        self.assertEqual(bit.toggle(x, 4), 0b10100010)
        self.assertEqual(bit.toggle(x, 5), 0b10010010)
        self.assertEqual(bit.toggle(x, 6), 0b11110010)
        self.assertEqual(bit.toggle(x, 7), 0b00110010)

        self.assertEqual(bit.toggle(y, 0), 0b01001100)
        self.assertEqual(bit.toggle(y, 1), 0b01001111)
        self.assertEqual(bit.toggle(y, 2), 0b01001001)
        self.assertEqual(bit.toggle(y, 3), 0b01000101)
        self.assertEqual(bit.toggle(y, 4), 0b01011101)
        self.assertEqual(bit.toggle(y, 5), 0b01101101)
        self.assertEqual(bit.toggle(y, 6), 0b00001101)
        self.assertEqual(bit.toggle(y, 7), 0b11001101)

    def test_get(self):
        x: int = 0b10110010
        y: int = 0b01001101

        self.assertEqual(bit.get(x, 0), 0)
        self.assertEqual(bit.get(x, 1), 1)
        self.assertEqual(bit.get(x, 2), 0)
        self.assertEqual(bit.get(x, 3), 0)
        self.assertEqual(bit.get(x, 4), 1)
        self.assertEqual(bit.get(x, 5), 1)
        self.assertEqual(bit.get(x, 6), 0)
        self.assertEqual(bit.get(x, 7), 1)

        self.assertEqual(bit.get(y, 0), 1)
        self.assertEqual(bit.get(y, 1), 0)
        self.assertEqual(bit.get(y, 2), 1)
        self.assertEqual(bit.get(y, 3), 1)
        self.assertEqual(bit.get(y, 4), 0)
        self.assertEqual(bit.get(y, 5), 0)
        self.assertEqual(bit.get(y, 6), 1)
        self.assertEqual(bit.get(y, 7), 0)
