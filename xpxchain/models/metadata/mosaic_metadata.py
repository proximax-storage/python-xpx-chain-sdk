
from __future__ import annotations

import typing

from .metadata_type import MetadataType
from ..mosaic.mosaic_id import MosaicId
from ..blockchain.network_type import OptionalNetworkType
from .field import Field
from ... import util

__all__ = ['MosaicMetadata']


@util.inherit_doc
@util.dataclass(frozen=True)
class MosaicMetadata(util.DTO):
    """

    :param metadataType:  Metadata type.
    :param fields:  Sequence of FieldDTOs.
    :param metadataId:  Metadata ID.

    DTO Format:
        .. code-block:: yaml

            MetadataDTO:
                metedataType: int
                fields: FieldDTO[]
                metedataId: int
    """

    metadata_type: MetadataType
    flds: typing.Sequence[Field]
    metadata_id: MosaicId

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
            'metadataType': util.u8_to_dto(self.metadata_type),
            'fields': [x.to_dto() for x in self.flds],
            'metadataId': util.u64_to_dto(int(self.metadata_id))
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
            metadata_type=MetadataType.create_from_dto(data["metadataType"]),
            flds=[Field.create_from_dto(f) for f in data["fields"]],
            metadata_id=MosaicId(util.u64_from_dto(data['metadataId']))
        )
