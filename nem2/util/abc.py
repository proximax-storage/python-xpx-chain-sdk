"""
    abc
    ====

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

import abc
import enum
from .format import InterchangeFormat


class Dto(abc.ABC):
    """
    Classes that can be converted to and from DTO format.

    NEM defines the DTO as a JSON-like format, which is similar to that
    defined in nem2-library-js, with a few notable differences.

        1. Python has native support for 64-bit integers, requiring
            no intermediate array.
    """

    @abc.abstractmethod
    def to_dto(self):
        """Convert object to DTO-serializable data."""

    def toDto(self):
        return self.to_dto()

    @classmethod
    @abc.abstractmethod
    def from_dto(cls, data):
        """Create object from DTO-serializable data."""

    @classmethod
    def fromDto(cls, data):
        return cls.from_dto(data)


class Catbuffer(abc.ABC):
    """Classes that can be converted to and from catbuffer."""

    @abc.abstractmethod
    def to_catbuffer(self):
        """Serialize object to catbuffer interchange format."""

    def toCatbuffer(self):
        return self.to_catbuffer()

    @classmethod
    @abc.abstractmethod
    def from_catbuffer(cls, data: bytes):
        """Deserialize object from catbuffer interchange format."""

    @classmethod
    def fromCatbuffer(cls, data):
        return cls.from_catbuffer(data)


class Model(Dto, Catbuffer):
    """Base class for NEM models."""

    def serialize(self, format: InterchangeFormat):
        """Serialize data to interchange format."""

        return format.serialize(self)

    @classmethod
    def deserialize(cls, data, format: InterchangeFormat):
        """Deserialize data from interchange format."""

        return format.deserialize(data, cls)
