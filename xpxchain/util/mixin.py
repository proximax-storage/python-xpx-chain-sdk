"""
    mixin
    =====

    Mixins classes.

    License
    -------

    Copyright 2019 NEM

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from __future__ import annotations
import typing

from . import abc
from . import documentation
from . import stdint

__all__ = [
    'EnumMixin',
    'IntMixin',
    'U8Mixin',
    'U16Mixin',
    'U32Mixin',
    'U64Mixin',
    'U128Mixin',
]

IntMixinType = typing.TypeVar('IntMixinType', bound='IntMixin')
U8MixinType = typing.TypeVar('U8MixinType', bound='U8Mixin')
U16MixinType = typing.TypeVar('U16MixinType', bound='U16Mixin')
U32MixinType = typing.TypeVar('U32MixinType', bound='U32Mixin')
U64MixinType = typing.TypeVar('U64MixinType', bound='U64Mixin')
U128MixinType = typing.TypeVar('U128MixinType', bound='U128Mixin')


class EnumMixin:
    """Mixin defining shared methods for enumerations."""

    __slots__ = ()

    def description(self) -> str:
        """Describe enumerated values in detail."""
        raise abc.AbstractMethodError


class IntMixin:
    """Mixin for classes that can be interpreted as integers."""

    __slots__ = ()

    def __int__(self) -> int:
        raise abc.AbstractMethodError

    def __index__(self) -> int:
        return self.__int__()

    def __format__(self, format_spec: str) -> str:
        return int(self).__format__(format_spec)

    @classmethod
    def create_from_hex(
        cls: typing.Type[IntMixinType],
        data: str
    ) -> IntMixinType:
        """
        Create instance of class from hex string.

        :param data: Hex-encoded ID data (with or without '0x' prefix).
        """

        # Assumes the number is encoded as if a 0x{hex} literal.
        # Same as the NEM2 library.
        return cls(int(data, 16))   # type: ignore


@documentation.inherit_doc
class U8Mixin(abc.Model):
    """Mixin for classes wrapping 8-bit integer types."""

    __slots__ = ()
    CATBUFFER_SIZE: typing.ClassVar[int] = stdint.U8_BYTES

    @classmethod
    def validate_dto(
        cls: typing.Type[U8MixinType],
        data: stdint.U8DTOType
    ) -> bool:
        """Validate the data-transfer object."""
        return isinstance(data, int) and 0 <= data < (1 << 8)

    def to_dto(
        self: U8MixinType,
        network_type: abc.OptionalNetworkType = None,
    ) -> stdint.U8DTOType:
        asint: int = int(self)      # type: ignore
        return stdint.u8_to_dto(asint)

    @classmethod
    def create_from_dto(
        cls: typing.Type[U8MixinType],
        data: stdint.U8DTOType,
        network_type: abc.OptionalNetworkType = None,
    ) -> U8MixinType:
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        asint = stdint.u8_from_dto(data)
        return cls(asint)           # type: ignore

    def to_catbuffer(
        self: U8MixinType,
        network_type: abc.OptionalNetworkType = None,
    ) -> bytes:
        asint: int = int(self)      # type: ignore
        return stdint.u8_to_catbuffer(asint)

    @classmethod
    def create_from_catbuffer(
        cls: typing.Type[U8MixinType],
        data: bytes,
        network_type: abc.OptionalNetworkType = None,
    ) -> U8MixinType:
        size = cls.CATBUFFER_SIZE
        asint = stdint.u8_from_catbuffer(data[:size])
        return cls(asint)           # type: ignore


@documentation.inherit_doc
class U16Mixin(abc.Model):
    """Mixin for classes wrapping 16-bit integer types."""

    __slots__ = ()
    CATBUFFER_SIZE: typing.ClassVar[int] = stdint.U16_BYTES

    @classmethod
    def validate_dto(
        cls: typing.Type[U16MixinType],
        data: stdint.U16DTOType
    ) -> bool:
        """Validate the data-transfer object."""
        return isinstance(data, int) and 0 <= data < (1 << 16)

    def to_dto(
        self: U16MixinType,
        network_type: abc.OptionalNetworkType = None,
    ) -> stdint.U16DTOType:
        asint: int = int(self)      # type: ignore
        return stdint.u16_to_dto(asint)

    @classmethod
    def create_from_dto(
        cls: typing.Type[U16MixinType],
        data: stdint.U16DTOType,
        network_type: abc.OptionalNetworkType = None,
    ) -> U16MixinType:
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        asint = stdint.u16_from_dto(data)
        return cls(asint)           # type: ignore

    def to_catbuffer(
        self: U16MixinType,
        network_type: abc.OptionalNetworkType = None,
    ) -> bytes:
        asint: int = int(self)      # type: ignore
        return stdint.u16_to_catbuffer(asint)

    @classmethod
    def create_from_catbuffer(
        cls: typing.Type[U16MixinType],
        data: bytes,
        network_type: abc.OptionalNetworkType = None,
    ) -> U16MixinType:
        size = cls.CATBUFFER_SIZE
        asint = stdint.u16_from_catbuffer(data[:size])
        return cls(asint)           # type: ignore


@documentation.inherit_doc
class U32Mixin(abc.Model):
    """Mixin for classes wrapping 32-bit integer types."""

    __slots__ = ()
    CATBUFFER_SIZE: typing.ClassVar[int] = stdint.U32_BYTES

    @classmethod
    def validate_dto(
        cls: typing.Type[U32MixinType],
        data: stdint.U32DTOType
    ) -> bool:
        """Validate the data-transfer object."""
        return isinstance(data, int) and 0 <= data < (1 << 32)

    def to_dto(
        self,
        network_type: abc.OptionalNetworkType = None,
    ) -> stdint.U32DTOType:
        asint: int = int(self)      # type: ignore
        return stdint.u32_to_dto(asint)

    @classmethod
    def create_from_dto(
        cls: typing.Type[U32MixinType],
        data: stdint.U32DTOType,
        network_type: abc.OptionalNetworkType = None,
    ) -> U32MixinType:
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        asint = stdint.u32_from_dto(data)
        return cls(asint)           # type: ignore

    def to_catbuffer(
        self: U32MixinType,
        network_type: abc.OptionalNetworkType = None,
    ) -> bytes:
        asint: int = int(self)      # type: ignore
        return stdint.u32_to_catbuffer(asint)

    @classmethod
    def create_from_catbuffer(
        cls: typing.Type[U32MixinType],
        data: bytes,
        network_type: abc.OptionalNetworkType = None,
    ) -> U32MixinType:
        size = cls.CATBUFFER_SIZE
        asint = stdint.u32_from_catbuffer(data[:size])
        return cls(asint)           # type: ignore


@documentation.inherit_doc
class U64Mixin(abc.Model):
    """Mixin for classes wrapping 64-bit integer types."""

    __slots__ = ()
    CATBUFFER_SIZE: typing.ClassVar[int] = stdint.U64_BYTES

    @classmethod
    def validate_dto(
        cls: typing.Type[U64MixinType],
        data: stdint.U64DTOType
    ) -> bool:
        """Validate the data-transfer object."""
        return len(data) == 2 and all(U32Mixin.validate_dto(i) for i in data)

    def to_dto(
        self: U64Mixin,
        network_type: abc.OptionalNetworkType = None,
    ) -> stdint.U64DTOType:
        asint: int = int(self)      # type: ignore
        return stdint.u64_to_dto(asint)

    @classmethod
    def create_from_dto(
        cls: typing.Type[U64MixinType],
        data: stdint.U64DTOType,
        network_type: abc.OptionalNetworkType = None,
    ) -> U64MixinType:
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        asint = stdint.u64_from_dto(data)
        return cls(asint)           # type: ignore

    def to_catbuffer(
        self: U64Mixin,
        network_type: abc.OptionalNetworkType = None,
    ) -> bytes:
        asint: int = int(self)      # type: ignore
        return stdint.u64_to_catbuffer(asint)

    @classmethod
    def create_from_catbuffer(
        cls: typing.Type[U64MixinType],
        data: bytes,
        network_type: abc.OptionalNetworkType = None,
    ) -> U64MixinType:
        size = cls.CATBUFFER_SIZE
        asint = stdint.u64_from_catbuffer(data[:size])
        return cls(asint)           # type: ignore


@documentation.inherit_doc
class U128Mixin(abc.Model):
    """Mixin for classes wrapping 128-bit integer types."""

    __slots__ = ()
    CATBUFFER_SIZE: typing.ClassVar[int] = stdint.U128_BYTES

    @classmethod
    def validate_dto(
        cls: typing.Type[U128MixinType],
        data: stdint.U128DTOType
    ) -> bool:
        """Validate the data-transfer object."""
        return len(data) == 2 and all(U64Mixin.validate_dto(i) for i in data)

    def to_dto(
        self: U128MixinType,
        network_type: abc.OptionalNetworkType = None,
    ) -> stdint.U128DTOType:
        asint: int = int(self)      # type: ignore
        return stdint.u128_to_dto(asint)

    @classmethod
    def create_from_dto(
        cls: typing.Type[U128MixinType],
        data: stdint.U128DTOType,
        network_type: abc.OptionalNetworkType = None,
    ) -> U128MixinType:
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        asint = stdint.u128_from_dto(data)
        return cls(asint)           # type: ignore

    def to_catbuffer(
        self: U128MixinType,
        network_type: abc.OptionalNetworkType = None,
    ) -> bytes:
        asint: int = int(self)      # type: ignore
        return stdint.u128_to_catbuffer(asint)

    @classmethod
    def create_from_catbuffer(
        cls: typing.Type[U128MixinType],
        data: bytes,
        network_type: abc.OptionalNetworkType = None,
    ) -> U128MixinType:
        size = cls.CATBUFFER_SIZE
        asint = stdint.u128_from_catbuffer(data[:size])
        return cls(asint)           # type: ignore
