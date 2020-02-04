"""
    mosaic_info
    ===========

    Detailed information describing an asset.

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

from .mosaic_id import MosaicId
from .mosaic_properties import MosaicProperties
from ..account.public_account import PublicAccount
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['MosaicInfo']


@util.inherit_doc
@util.dataclass(frozen=True)
class MosaicInfo(util.DTO):
    """
    Information describing a mosaic.

    :param active: Mosaic is active.
    :param index: Mosaic index.
    :param meta_id: Mosaic metadata ID.
    :param mosaic_id: Mosaic ID.
    :param nonce: Mosaic nonce.
    :param supply: Mosaic supply.
    :param height: Block height when mosaic was created.
    :param owner: Account that owns mosaic.
    :param properties: Mosaic properties.

    DTO Format:
        .. code-block:: yaml

            MosaicMetaDTO:
                # Hex(Id) (24-bytes)
                id: string

            MosaicDefinitionDTO:
                mosaicId: UInt64DTO
                supply: UInt64DTO
                height: UInt64DTO
                # Hex(PublicKey) (64-bytes)
                owner: string
                revision: integer
                properties: MosaicPropertiesDTO

            MosaicInfoDTO:
                meta: MosaicMetaDTO
                mosaic: MosaicDefinitionDTO
    """

    meta_id: str
    mosaic_id: MosaicId
    supply: int
    height: int
    owner: PublicAccount
    revision: int
    properties: MosaicProperties

    @property
    def divisibility(self) -> int:
        """Get the decimal place mosaic can be divided into."""
        return self.properties.divisibility

    @property
    def duration(self) -> int:
        """Get the number of blocks the mosaic will be available."""
        return self.properties.duration

    def is_supply_mutable(self) -> bool:
        """Mosaic allows a supply change later on. Default false."""
        return self.properties.supply_mutable

    def is_transferable(self) -> bool:
        """Allow transfer of funds from non-creator accounts. Default true."""
        return self.properties.transferable

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'meta', 'mosaic'}
        required_l21 = {'id'}
        required_l22 = {
            'mosaicId',
            'supply',
            'height',
            'owner',
            'revision',
            'properties',
        }
        return (
            # Level 1
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
            # Level 2_1
            and cls.validate_dto_required(data['meta'], required_l21)
            and cls.validate_dto_all(data['meta'], required_l21)
            # Level 2_2
            and cls.validate_dto_required(data['mosaic'], required_l22)
            # and cls.validate_dto_all(data['mosaic'], required_l22)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'meta': {
                'id': self.meta_id,
            },
            'mosaic': {
                'mosaicId': util.u64_to_dto(int(self.mosaic_id)),
                'supply': util.u64_to_dto(self.supply),
                'height': util.u64_to_dto(self.height),
                'owner': self.owner.public_key,
                'revision': util.u32_to_dto(self.revision),
                'properties': self.properties.to_dto(network_type),
            },
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        meta_dto = data['meta']
        mosaic_dto = data['mosaic']
        owner_dto = mosaic_dto['owner']
        return cls(
            meta_id=meta_dto['id'],
            mosaic_id=MosaicId(util.u64_from_dto(mosaic_dto['mosaicId'])),
            supply=util.u64_from_dto(mosaic_dto['supply']),
            height=util.u64_from_dto(mosaic_dto['height']),
            owner=PublicAccount.create_from_public_key(owner_dto, network_type),
            revision=util.u32_from_dto(mosaic_dto['revision']),
            properties=MosaicProperties.create_from_dto(mosaic_dto['properties']),
        )
