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

    def __format__(self, format_spec: str):
        return int(self).__format__(format_spec)

    @classmethod
    def from_hex(cls, data: str):
        """
        Create instance of class from hex string.

        :param data: Hex-encoded ID data (with or without '0x' prefix).
        """
        return cls(int(data, 16))


@documentation.inherit_doc
class U8Mixin(abc.Model):
    """Mixin for classes wrapping 8-bit integer types."""

    __slots__ = ()
    CATBUFFER_SIZE: typing.ClassVar[int] = stdint.U8_BYTES

    def to_dto(self, network_type=None) -> stdint.U8DTOType:
        asint: int = int(self)      # type: ignore
        return stdint.u8_to_dto(asint)

    @classmethod
    def from_dto(cls, data: stdint.U8DTOType, network_type=None):
        asint = stdint.u8_from_dto(data)
        return cls(asint)           # type: ignore

    def to_catbuffer(self, network_type=None) -> bytes:
        asint: int = int(self)      # type: ignore
        return stdint.u8_to_catbuffer(asint)

    @classmethod
    def from_catbuffer(cls, data: bytes, network_type=None):
        size = cls.CATBUFFER_SIZE
        asint = stdint.u8_from_catbuffer(data[:size])
        return cls(asint)           # type: ignore


@documentation.inherit_doc
class U16Mixin(abc.Model):
    """Mixin for classes wrapping 16-bit integer types."""

    __slots__ = ()
    CATBUFFER_SIZE: typing.ClassVar[int] = stdint.U16_BYTES

    def to_dto(self, network_type=None) -> stdint.U16DTOType:
        asint: int = int(self)      # type: ignore
        return stdint.u16_to_dto(asint)

    @classmethod
    def from_dto(cls, data: stdint.U16DTOType, network_type=None):
        asint = stdint.u16_from_dto(data)
        return cls(asint)           # type: ignore

    def to_catbuffer(self, network_type=None) -> bytes:
        asint: int = int(self)      # type: ignore
        return stdint.u16_to_catbuffer(asint)

    @classmethod
    def from_catbuffer(cls, data: bytes, network_type=None):
        size = cls.CATBUFFER_SIZE
        asint = stdint.u16_from_catbuffer(data[:size])
        return cls(asint)           # type: ignore


@documentation.inherit_doc
class U32Mixin(abc.Model):
    """Mixin for classes wrapping 32-bit integer types."""

    __slots__ = ()
    CATBUFFER_SIZE: typing.ClassVar[int] = stdint.U32_BYTES

    def to_dto(self, network_type=None) -> stdint.U32DTOType:
        asint: int = int(self)      # type: ignore
        return stdint.u32_to_dto(asint)

    @classmethod
    def from_dto(cls, data: stdint.U32DTOType, network_type=None):
        asint = stdint.u32_from_dto(data)
        return cls(asint)           # type: ignore

    def to_catbuffer(self, network_type=None) -> bytes:
        asint: int = int(self)      # type: ignore
        return stdint.u32_to_catbuffer(asint)

    @classmethod
    def from_catbuffer(cls, data: bytes, network_type=None):
        size = cls.CATBUFFER_SIZE
        asint = stdint.u32_from_catbuffer(data[:size])
        return cls(asint)           # type: ignore


@documentation.inherit_doc
class U64Mixin(abc.Model):
    """Mixin for classes wrapping 64-bit integer types."""

    __slots__ = ()
    CATBUFFER_SIZE: typing.ClassVar[int] = stdint.U64_BYTES

    def to_dto(self, network_type=None) -> stdint.U64DTOType:
        asint: int = int(self)      # type: ignore
        return stdint.u64_to_dto(asint)

    @classmethod
    def from_dto(cls, data: stdint.U64DTOType, network_type=None):
        asint = stdint.u64_from_dto(data)
        return cls(asint)           # type: ignore

    def to_catbuffer(self, network_type=None) -> bytes:
        asint: int = int(self)      # type: ignore
        return stdint.u64_to_catbuffer(asint)

    @classmethod
    def from_catbuffer(cls, data: bytes, network_type=None):
        size = cls.CATBUFFER_SIZE
        asint = stdint.u64_from_catbuffer(data[:size])
        return cls(asint)           # type: ignore


@documentation.inherit_doc
class U128Mixin(abc.Model):
    """Mixin for classes wrapping 128-bit integer types."""

    __slots__ = ()
    CATBUFFER_SIZE: typing.ClassVar[int] = stdint.U128_BYTES

    def to_dto(self, network_type=None) -> stdint.U128DTOType:
        asint: int = int(self)      # type: ignore
        return stdint.u128_to_dto(asint)

    @classmethod
    def from_dto(cls, data: stdint.U128DTOType, network_type=None):
        asint = stdint.u128_from_dto(data)
        return cls(asint)           # type: ignore

    def to_catbuffer(self, network_type=None) -> bytes:
        asint: int = int(self)      # type: ignore
        return stdint.u128_to_catbuffer(asint)

    @classmethod
    def from_catbuffer(cls, data: bytes, network_type=None):
        size = cls.CATBUFFER_SIZE
        asint = stdint.u128_from_catbuffer(data[:size])
        return cls(asint)           # type: ignore
