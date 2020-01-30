from xpxchain import util
from tests import harness


class TestUMixin(harness.TestCase):

    def test_u8mixin(self):
        class Mixin(util.U8Mixin, int):
            __slots__ = ()

        value = Mixin(0x7F)
        dto = 0x7F
        catbuffer = b'\x7f'
        self.assertEqual(value.to_dto(None), dto)
        self.assertEqual(Mixin.create_from_dto(dto, None), value)
        self.assertEqual(value.to_catbuffer(None), catbuffer)
        self.assertEqual(Mixin.create_from_catbuffer(catbuffer, None), value)

    def test_u16mixin(self):
        class Mixin(util.U16Mixin, int):
            __slots__ = ()

        value = Mixin(0x7FFF)
        dto = 0x7FFF
        catbuffer = b'\xff\x7f'
        self.assertEqual(value.to_dto(None), dto)
        self.assertEqual(Mixin.create_from_dto(dto, None), value)
        self.assertEqual(value.to_catbuffer(None), catbuffer)
        self.assertEqual(Mixin.create_from_catbuffer(catbuffer, None), value)

    def test_u32mixin(self):
        class Mixin(util.U32Mixin, int):
            __slots__ = ()

        value = Mixin(0x7FFFFFFF)
        dto = 0x7FFFFFFF
        catbuffer = b'\xff\xff\xff\x7f'
        self.assertEqual(value.to_dto(None), dto)
        self.assertEqual(Mixin.create_from_dto(dto, None), value)
        self.assertEqual(value.to_catbuffer(None), catbuffer)
        self.assertEqual(Mixin.create_from_catbuffer(catbuffer, None), value)

    def test_u64mixin(self):
        class Mixin(util.U64Mixin, int):
            __slots__ = ()

        value = Mixin(0x7FFFFFFFFFFFFFFF)
        dto = [0xFFFFFFFF, 0x7FFFFFFF]
        catbuffer = b'\xff\xff\xff\xff\xff\xff\xff\x7f'
        self.assertEqual(value.to_dto(None), dto)
        self.assertEqual(Mixin.create_from_dto(dto, None), value)
        self.assertEqual(value.to_catbuffer(None), catbuffer)
        self.assertEqual(Mixin.create_from_catbuffer(catbuffer, None), value)

    def test_u128mixin(self):
        class Mixin(util.U128Mixin, int):
            __slots__ = ()

        value = Mixin(0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)
        dto = [[0xFFFFFFFF, 0xFFFFFFFF], [0xFFFFFFFF, 0x7FFFFFFF]]
        catbuffer = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x7f'
        self.assertEqual(value.to_dto(None), dto)
        self.assertEqual(Mixin.create_from_dto(dto, None), value)
        self.assertEqual(value.to_catbuffer(None), catbuffer)
        self.assertEqual(Mixin.create_from_catbuffer(catbuffer, None), value)
