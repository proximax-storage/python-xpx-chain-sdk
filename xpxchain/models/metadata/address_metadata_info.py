
from __future__ import annotations

from .address_metadata import AddressMetadata
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['AddressMetadataInfo']


@util.inherit_doc
@util.dataclass(frozen=True)
class AddressMetadataInfo(util.DTO):
    """

    :param metadata:  Address metadata info.

    DTO Format:
        .. code-block:: yaml

            AddressMetadataInfoDTO:
                metedata: AddressMetadataDTO
    """

    metadata: AddressMetadata

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
            metadata=AddressMetadata.create_from_dto(data['metadata'])
        )
