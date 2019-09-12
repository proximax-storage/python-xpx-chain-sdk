
from __future__ import annotations

import typing

from ... import util

__all__ = ['Field']


@util.inherit_doc
@util.dataclass(frozen=True)
class Field(util.DTO):
    """

    :param key:  Key of a field.
    :param value:  Value of a field.

    DTO Format:
        .. code-block:: yaml

            FieldDTO:
                key: string
                value: string
    """

    key: str
    value: str

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {
            'key',
            'value'
        }
        
        return (
            # Level 1
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'key': key,
            'value': self.value
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        return cls(
            key=data["key"],
            value=data["value"]
        )
