
from __future__ import annotations

from .mosaic_metadata import MosaicMetadata
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['MosaicMetadataInfo']


@util.inherit_doc
@util.dataclass(frozen=True)
class MosaicMetadataInfo(util.DTO):
    """

    :param metadata:  Mosaic metadata info.

    DTO Format:
        .. code-block:: yaml

            MosaicMetadataInfoDTO:
                metedata: MosaicMetadataDTO
    """

    metadata: MosaicMetadata

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'metadata'}

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
            'metadata': self.metadata.to_dto(),
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
            metadata=MosaicMetadata.create_from_dto(data['metadata'])
        )
