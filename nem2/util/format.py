"""
    format
    ======

    Enumerations for data interchange formats.

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

import enum
import typing


class InterchangeFormat(enum.IntEnum):
    """Enumerations for the NEM interchange formats."""

    DTO = 0
    CATBUFFER = 1

    def description(self) -> str:
        """Describe enumerated values in detail."""

        return DESCRIPTION[self]

    def serialize(self, value: typing.Any) -> typing.Any:
        """Serialize model to data interchange format."""

        return SERIALIZE[self](value)

    def deserialize(self, data: typing.Any, value_type: type) -> typing.Any:
        """Deserialize model from data interchange format."""

        return DESERIALIZE[self](data, value_type)


def to_dto(value: typing.Any) -> typing.Any:
    """Export value to DTO."""

    return value.to_dto()


def to_catbuffer(value: typing.Any) -> bytes:
    """Export value to catbuffer."""

    return value.to_catbuffer()


def from_dto(data: typing.Any, value_type: type) -> typing.Any:
    """Load value from DTO."""

    return value_type.from_dto(data)


def from_catbuffer(data: bytes, value_type: type) -> typing.Any:
    """Load value from catbuffer."""

    return value_type.from_catbuffer(data)[0]


DESCRIPTION = {
    InterchangeFormat.DTO: "DTO",
    InterchangeFormat.CATBUFFER: "catbuffer",
}

SERIALIZE = {
    InterchangeFormat.DTO: to_dto,
    InterchangeFormat.CATBUFFER: to_catbuffer,
}

DESERIALIZE = {
    InterchangeFormat.DTO: from_dto,
    InterchangeFormat.CATBUFFER: from_catbuffer,
}
