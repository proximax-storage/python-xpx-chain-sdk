
from __future__ import annotations

import typing

from .metadata import Metadata
from ... import util

__all__ = ['NamespaceMetadataInfo']


@util.inherit_doc
@util.dataclass(frozen=True)
class NamespaceMetadataInfo(util.DTO):
    """

    :param metadata:  Metadata info.

    DTO Format:
        .. code-block:: yaml

            NamespaceMetadataInfoDTO:
                metedata: MetadataDTO
    """

    metadata: Metadata

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

        metadata = data['metadata']
        return cls(
            metadata=Metadata.create_from_dto(metadata)
        )
