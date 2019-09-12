
from __future__ import annotations

import typing

from .field import Field
from ... import util

__all__ = ['Metadata']


@util.inherit_doc
@util.dataclass(frozen=True)
class Metadata(util.DTO):
    """

    :param metadataType:  Metadata type.
    :param fields:  Sequence of FieldDTOs.
    :param metadataId:  Metadata ID.

    DTO Format:
        .. code-block:: yaml

            MetadataDTO:
                metedataType: int
                fields: FieldDTO[]
                metedataId: string
    """

    metadata_type: int
    filds: typing.Sequence[Field] 
    metadata_id: str

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {
            'metadataType',
            'fields',
            'metadataId'
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
            'metadataType': self.metadata_type,
            'fields': [x.to_dto() for x in self.filds],
            'metadataId': self.metadata_id
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
            metadata_type=data["metadataType"],
            filds=[x.create_from_dto(field) for field in data["fields"]],
            metadata_id=data["metadataId"]
        )
