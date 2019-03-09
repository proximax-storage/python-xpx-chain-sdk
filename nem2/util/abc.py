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

from .format import InterchangeFormat

__all__ = [
    'Dto',
    'Catbuffer',
    'Model',
]

# MODELS
# ------


class Dto:
    """Future format of the DTO class."""

    __slots__ = ()

    def to_dto(self):
        """Convert object to DTO-serializable data."""
        raise NotImplementedError

    def toDto(self):
        return self.to_dto()

    @classmethod
    def from_dto(cls, data):
        """Create object from DTO-serializable data."""
        raise NotImplementedError

    @classmethod
    def fromDto(cls, data):
        return cls.from_dto(data)


class Catbuffer:
    """Future format of the catbuffer class."""

    __slots__ = ()

    def to_catbuffer(self):
        """Serialize object to catbuffer interchange format."""

    def toCatbuffer(self):
        return self.to_catbuffer()

    @classmethod
    def from_catbuffer(cls, data):
        """Deserialize object from catbuffer interchange format."""

    @classmethod
    def fromCatbuffer(cls, data):
        return cls.from_catbuffer(data)


class Model(Dto, Catbuffer):
    """Base class for NEM models."""

    __slots__ = ()

    def serialize(self, format: InterchangeFormat):
        """Serialize data to interchange format."""

        return format.serialize(self)

    @classmethod
    def deserialize(cls, data, format: InterchangeFormat):
        """Deserialize data from interchange format."""

        return format.deserialize(data, cls)
