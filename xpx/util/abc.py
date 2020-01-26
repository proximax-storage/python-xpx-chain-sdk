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
import enum
import typing

__all__ = [
    'AbstractMethodError',
    'Catbuffer',
    'DTO',
    'Object',
    'Model',
]

# TYPES

NetworkType = typing.TypeVar('NetworkType', bound=enum.IntEnum)
OptionalNetworkType = typing.Optional[NetworkType]
DTOType = typing.TypeVar('DTOType', bound='DTO')
CatbufferType = typing.TypeVar('CatbufferType', bound='Catbuffer')
ModelType = typing.TypeVar('ModelType', bound='Model')
DTOFormat = typing.TypeVar('DTOFormat', int, str, dict, list)

# EXCEPTIONS


class AbstractMethodError(NotImplementedError):
    pass


# MODELS

# typing.Generic defines a custom __new__, which causes enum
# to use it, rather than the data_type, as the constructor
# for the type. We can override the __new__ to call the correct
# type, however, we still return instances of that class with
# attributes of the data type built in. For example, for integers,
# we can still call __int__ to get the underlying value, however,
# __repr__, __eq__, and most other methods are overridden. This
# is especially problematic for str, since it effectively requires
# hacks to access the underlying value (which is true for everything).
# There are 2 possible solutions:
#   1. Define a new Generic base where `__new__`, `__init_subclass__`
#       are deleted from typing.Generic, so that mypy still checks types.
#   2. Define the base as Generic only when `typing.TYPE_CHECKING`.
#
# The latter is way less fragile, and if other tools start to break,
# the easy solution is to just remove `typing.Generic`, the optional
# type checks, rather than attempt to deconvolute complicated
# inheritance patterns. The condition should be on the invocation
# of mypy, since sphinx-doc will attempt to parse the actual source code.
#
# We define a new class, does not understand the base class from
# assignment as of '0.670'.
T = typing.TypeVar('T')
MYPY = False

if MYPY:

    class Object(typing.Generic[T]):
        """Transparent Generic subclass."""
        __slots__ = ()
else:

    class Object:
        """Class-indexable object that just returns objects."""
        __slots__ = ()

        def __class_getitem__(cls, params):
            return cls


class DTO(Object[DTOFormat]):
    """Future format of the DTO class."""

    __slots__ = ()

    @classmethod
    def validate_dto_required(
        cls: typing.Type[DTOType],
        data: dict,
        required_keys: set
    ) -> bool:
        """Validate the required keys of the DTO."""
        return set(data) & required_keys == required_keys

    @classmethod
    def validate_dto_all(
        cls: typing.Type[DTOType],
        data: dict,
        all_keys: set
    ) -> bool:
        """Validate all keys are known of the DTO."""
        if __debug__:
            # Only do in debug builds, since it might pose backwards-
            # compatibility issues in production.
            return not(set(data) - all_keys)
        return True

    @classmethod
    def validate_dto(
        cls: typing.Type[DTOType],
        data: DTOFormat
    ) -> bool:
        """
        Validate the DTO interchange format matches the object type.

        :param data: Data-transfer object.
        :return: If DTO was validated for type.
        """
        raise AbstractMethodError

    def to_dto(
        self: DTOType,
        network_type: OptionalNetworkType = None,
    ) -> DTOFormat:
        """
        Export model to DTO interchange format.

        :param network_type: (Optional) network type.
        :return: Model as DTO interchange format.
        """
        raise AbstractMethodError

    @classmethod
    def create_from_dto(
        cls: typing.Type[DTOType],
        data: DTOFormat,
        network_type: OptionalNetworkType = None,
    ) -> DTOType:
        """
        Load model from DTO interchange format.

        :param data: Data-transfer object.
        :param network_type: (Optional) network type.
        :return: Native model from DTO interchange format.
        """
        raise AbstractMethodError

    @classmethod
    def iter_to_dto(
        cls: typing.Type[DTOType],
        iterable: typing.Iterable[DTOType],
        network_type: OptionalNetworkType = None,
    ) -> typing.Generator[DTOFormat, None, None]:
        """
        Iteratively export models to DTO interchange format.

        :param iterable: Iterable yielding models.
        :param network_type: Network type.
        :return: Next model as DTO interchange format.
        """
        for model in iterable:
            yield model.to_dto(network_type)

    @classmethod
    def iter_from_dto(
        cls: typing.Type[DTOType],
        iterable: typing.Iterable[DTOFormat],
        network_type: OptionalNetworkType = None,
    ) -> typing.Generator[DTOType, None, None]:
        """
        Iteratively load models from DTO interchange format.

        :param iterable: Iterable yielding DTO objects.
        :param network_type: Network type.
        :return: Next native model from DTO interchange format.
        """
        for dto in iterable:
            yield cls.create_from_dto(dto, network_type)

    @classmethod
    def sequence_to_dto(
        cls: typing.Type[DTOType],
        sequence: typing.Sequence[DTOType],
        network_type: OptionalNetworkType = None,
    ) -> typing.Sequence[DTOFormat]:
        """
        Export sequence of models to DTO interchange format.

        :param sequence: Sequence of models.
        :param network_type: Network type.
        :return: List of models in DTO interchange format.
        """
        return list(cls.iter_to_dto(sequence, network_type))

    @classmethod
    def sequence_from_dto(
        cls: typing.Type[DTOType],
        sequence: typing.Sequence[DTOFormat],
        network_type: OptionalNetworkType = None,
    ) -> typing.Sequence[DTOType]:
        """
        Load list of models from DTO interchange format.

        :param sequence: Sequence of DTO objects.
        :param network_type: Network type.
        :return: List of native model from DTO interchange format.
        """
        return list(cls.iter_from_dto(sequence, network_type))


def is_same_classmethod(
    cls1: typing.Type,
    cls2: typing.Type,
    name: str,
) -> bool:
    """Check if two class methods are not the same instance."""

    clsmeth1 = getattr(cls1, name)
    clsmeth2 = getattr(cls2, name)
    return clsmeth1.__func__ is clsmeth2.__func__


class Catbuffer(Object):
    """
    Future format of the catbuffer class.

    Either `create_from_catbuffer` or `create_from_catbuffer_pair` needs
    to be specialized. If `CATBUFFER_SIZE` is present, `create_from_catbuffer`
    should be specialized, otherwise, `create_from_catbuffer_pair` should
    be specialized. If `CATBUFFER_SIZE` is present and neither function
    is specialized, it will lead to an `AssertionError`, or on optimized
    builds, a `RecursionError`.
    """

    __slots__ = ()
    CATBUFFER_SIZE: typing.ClassVar[int]

    def to_catbuffer(
        self: CatbufferType,
        network_type: OptionalNetworkType = None,
    ) -> bytes:
        """
        Export model to catbuffer interchange format.

        :param network_type: (Optional) network type.
        :return: Model as catbuffer interchange format.
        """
        raise AbstractMethodError

    @classmethod
    def create_from_catbuffer(
        cls: typing.Type[CatbufferType],
        data: bytes,
        network_type: OptionalNetworkType = None,
    ) -> CatbufferType:
        """
        Load model from catbuffer interchange format.

        If `CATBUFFER_SIZE` is defined, you should override this
        method, and `create_from_catbuffer_pair` will be automatically
        defined. Otherwise, override `create_from_catbuffer_pair`.

        :param network_type: (Optional) network type.
        :return: Native model from catbuffer interchange format.
        """
        assert not is_same_classmethod(cls, Catbuffer, 'create_from_catbuffer_pair')
        return cls.create_from_catbuffer_pair(data, network_type)[0]

    @classmethod
    def create_from_catbuffer_pair(
        cls: typing.Type[CatbufferType],
        data: bytes,
        network_type: OptionalNetworkType = None,
    ) -> typing.Tuple[CatbufferType, bytes]:
        """
        Load model from catbuffer interchange format.

        If `CATBUFFER_SIZE` is not defined, you should override this
        method, and `create_from_catbuffer` will be automatically defined.
        Otherwise, override `create_from_catbuffer`.

        :param network_type: (Optional) network type.
        :return: Model and remaining bytes leftover.
        """
        assert not is_same_classmethod(cls, Catbuffer, 'create_from_catbuffer')
        size = cls.CATBUFFER_SIZE
        inst = cls.create_from_catbuffer(data[:size], network_type)
        remaining = data[size:]
        return inst, remaining

    @classmethod
    def iter_to_catbuffer(
        cls: typing.Type[CatbufferType],
        iterable: typing.Iterable[CatbufferType],
        network_type,
    ) -> typing.Generator[bytes, None, None]:
        """
        Iteratively export models to catbuffer interchange format.

        :param iterable: Iterable yielding models.
        :param network_type: Network type.
        :return: Next model as catbuffer interchange format.
        """
        for model in iterable:
            yield model.to_catbuffer(network_type)

    @classmethod
    def iter_from_catbuffer(
        cls: typing.Type[CatbufferType],
        data: bytes,
        count: int,
        network_type,
    ) -> typing.Generator[CatbufferType, None, None]:
        """
        Iteratively load models from catbuffer interchange format.

        :param data: Raw data as catbuffer interchange format.
        :param count: Number of models to load.
        :param network_type: Network type.
        :return: Next native model from catbuffer interchange format.
        """
        for value, data in cls.iter_from_catbuffer_pair(data, count, network_type):
            yield value

    @classmethod
    def iter_from_catbuffer_pair(
        cls: typing.Type[CatbufferType],
        data: bytes,
        count: int,
        network_type,
    ) -> typing.Generator[typing.Tuple[CatbufferType, bytes], None, None]:
        """
        Iteratively load models from catbuffer interchange format.

        :param data: Raw data as catbuffer interchange format.
        :param count: Number of models to load.
        :param network_type: Network type.
        :return: Next native model and input bytes leftover.
        """
        for _ in range(count):
            value, data = cls.create_from_catbuffer_pair(data, network_type)
            yield value, data

    @classmethod
    def sequence_to_catbuffer(
        cls: typing.Type[CatbufferType],
        sequence: typing.Sequence[CatbufferType],
        network_type,
    ) -> bytes:
        """
        Export sequence of models to catbuffer interchange format.

        :param sequence: Sequence of models.
        :param network_type: Network type.
        :return: Concatenated bytes from each model exported to catbuffer.
        """
        return b''.join(cls.iter_to_catbuffer(sequence, network_type))

    @classmethod
    def sequence_from_catbuffer(
        cls: typing.Type[CatbufferType],
        data: bytes,
        count: int,
        network_type,
    ) -> typing.Sequence[CatbufferType]:
        """
        Load list of models from catbuffer interchange format.

        :param data: Raw data as catbuffer interchange format.
        :param count: Number of models to load.
        :param network_type: Network type.
        :return: List of native models.
        """
        return cls.sequence_from_catbuffer_pair(data, count, network_type)[0]

    @classmethod
    def sequence_from_catbuffer_pair(
        cls: typing.Type[CatbufferType],
        data: bytes,
        count: int,
        network_type,
    ) -> typing.Tuple[typing.Sequence[CatbufferType], bytes]:
        """
        Load list of models from catbuffer interchange format.

        :param data: Raw data as catbuffer interchange format.
        :param count: Number of models to load.
        :param network_type: Network type.
        :return: List of native models and input bytes leftover.
        """
        result = []
        iterable = cls.iter_from_catbuffer_pair(data, count, network_type)
        for value, data in iterable:
            result.append(value)
        return result, data


class Model(DTO, Catbuffer):
    """Base class for NEM models."""

    __slots__ = ()
