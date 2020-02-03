
from __future__ import annotations

from ..blockchain.network_type import NetworkType, OptionalNetworkType
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
        )

    def catbuffer_size_specific(self) -> int:
        key_size = util.U8_BYTES * len(self.key)
        value_size = util.U8_BYTES * len(self.value)

        return key_size + value_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        key = self.key.encode('utf8')
        value = self.value.encode('utf8')

        return key + value

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        return cls(
            key=data['key'],
            value=data['value'],
        )
