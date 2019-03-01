"""
    format
    ======

    Enumerations for data interchange formats.
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
    InterchangeFormat.CATBUFFER: lambda d, t: t.from_catbuffer(d),
}
