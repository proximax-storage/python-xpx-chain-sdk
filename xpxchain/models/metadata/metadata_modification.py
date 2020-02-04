"""
    account_property_modification
    =============================

    Account property modification type and value.

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

from .field import Field
from .metadata_modification_type import MetadataModificationType
from ..blockchain.network_type import NetworkType, OptionalNetworkType
from ... import util

__all__ = ['MetadataModification']


@util.inherit_doc
@util.dataclass(frozen=True)
class MetadataModification(util.DTO):
    """
    Metadata modification type and value.

    :param modification_type: Metadata modification type.
    :param field: Modification field.
    """

    modification_type: MetadataModificationType
    field: Field

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'modificationType', 'key', 'value'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def catbuffer_size_specific(self) -> int:
        modification_size = util.U32_BYTES
        modification_type_size = MetadataModificationType.CATBUFFER_SIZE
        key_size = util.U8_BYTES
        value_size = util.U16_BYTES
        field_size = self.field.catbuffer_size_specific()

        return modification_size + modification_type_size + key_size + value_size + field_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:

        modification_size = util.u32_to_catbuffer(self.catbuffer_size_specific())
        modification_type = util.u8_to_catbuffer(self.modification_type)
        key_size = util.u8_to_catbuffer(len(self.field.key))
        value_size = util.u16_to_catbuffer(len(self.field.value))
        field = self.field.to_catbuffer_specific(network_type)

        return modification_size + modification_type + key_size + value_size + field

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'modificationType': self.modification_type.to_dto(network_type),
            'key': self.field.key,
            'value': self.field.value,
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
            modification_type=MetadataModificationType.create_from_dto(
                data['modificationType']
            ),
            field=Field(data['key'], data['value']),
        )
