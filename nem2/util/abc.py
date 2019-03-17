"""
    abc
    ===

    Abstract base classes for NEM models.

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

__all__ = [
    'AbstractMethodError',
    'Catbuffer',
    'DTO',
    'Model',
]

# EXCEPTIONS


class AbstractMethodError(NotImplementedError):
    pass


# MODELS


class DTO:
    """Future format of the DTO class."""

    __slots__ = ()

    def to_dto(self, network_type):
        raise AbstractMethodError

    def toDTO(self, network_type):
        return self.to_dto(network_type)

    @classmethod
    def from_dto(cls, data, network_type):
        raise AbstractMethodError

    @classmethod
    def fromDTO(cls, data, network_type):
        return cls.from_dto(data, network_type)


def is_same_classmethod(cls1, cls2, name):
    """Check if two class methods are not the same instance."""

    clsmeth1 = getattr(cls1, name)
    clsmeth2 = getattr(cls2, name)
    return clsmeth1.__func__ is clsmeth2.__func__


class Catbuffer:
    """
    Future format of the catbuffer class.

    Either `from_catbuffer` or `from_catbuffer_pair` needs to be specialized.
    If `CATBUFFER_SIZE` is present, `from_catbuffer` should be specialized,
    otherwise, `from_catbuffer_pair` should be specialized. If
    `CATBUFFER_SIZE` is present and neither function is specialized,
    it will lead to an `AssertionError`, or on optimized builds, a
    `RecursionError`.
    """

    __slots__ = ()
    CATBUFFER_SIZE: typing.ClassVar[int]

    def to_catbuffer(self, network_type):
        raise AbstractMethodError

    def toCatbuffer(self, network_type):
        return self.to_catbuffer(network_type)

    @classmethod
    def from_catbuffer(cls, data, network_type):
        assert not is_same_classmethod(cls, Catbuffer, 'from_catbuffer_pair')
        return cls.from_catbuffer_pair(data, network_type)[0]

    @classmethod
    def fromCatbuffer(cls, data, network_type):
        return cls.from_catbuffer(data, network_type)

    @classmethod
    def from_catbuffer_pair(cls, data, network_type):
        assert not is_same_classmethod(cls, Catbuffer, 'from_catbuffer')
        size = cls.CATBUFFER_SIZE
        inst = cls.from_catbuffer(data[:size], network_type)
        remaining = data[size:]
        return inst, remaining

    @classmethod
    def fromCatbufferPair(cls, data, network_type):
        return cls.from_catbuffer_pair(data, network_type)


class Model(DTO, Catbuffer):
    """Base class for NEM models."""

    __slots__ = ()
