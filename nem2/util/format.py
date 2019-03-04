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


class InterchangeFormat(enum.IntEnum):
    """Enumerations for the NEM interchange formats."""

    DTO        = 0
    CATBUFFER   = 1

    def description(self):
        """Describe enumerated values in detail."""

        return DESCRIPTION[self]

    def serialize(self, value):
        """Serialize model to data interchange format."""

        return SERIALIZE[self](value)

    def deserialize(self, data, value_type):
        """Deserialize model from data interchange format."""

        return DESERIALIZE[self](data, value_type)


DESCRIPTION = {
    InterchangeFormat.DTO: "DTO",
    InterchangeFormat.CATBUFFER: "catbuffer",
}

SERIALIZE = {
    InterchangeFormat.DTO: lambda x: x.to_dto(),
    InterchangeFormat.CATBUFFER: lambda x: x.to_catbuffer(),
}

DESERIALIZE = {
    InterchangeFormat.DTO: lambda d, t: t.from_dto(d),
    InterchangeFormat.CATBUFFER: lambda d, t: t.from_catbuffer(d)[0],
}
