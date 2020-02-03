
from __future__ import annotations

from .address_metadata import AddressMetadata
from .mosaic_metadata import MosaicMetadata
from .namespace_metadata import NamespaceMetadata
from .metadata_type import MetadataType
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['MetadataInfo']


@util.inherit_doc
@util.dataclass(frozen=True)
class MetadataInfo(util.DTO):
    """

    :param metadata:  Generic metadata info.

    DTO Format:
        .. code-block:: yaml

            AddressMetadataInfoDTO:
                metedata: MetadataDTO
    """

    metadata: AddressMetadata

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'metadata'}
        required_l2 = {'metadataType', 'fields', 'metadataId'}

        return (
            # Level 1
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
            and cls.validate_dto_required(data['metadata'], required_l2)
            and cls.validate_dto_all(data['metadata'], required_l2)
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

        metadata = data['metadata']

        if (metadata['metadataType'] == MetadataType.ADDRESS):
            return cls(
                metadata=AddressMetadata.create_from_dto(metadata)
            )
        elif (metadata['metadataType'] == MetadataType.MOSAIC):
            return cls(
                metadata=MosaicMetadata.create_from_dto(metadata)
            )
        elif (metadata['metadataType'] == MetadataType.NAMESPACE):
            return cls(
                metadata=NamespaceMetadata.create_from_dto(metadata)
            )
        else:
            raise ValueError('Invalid data-transfer object.')
