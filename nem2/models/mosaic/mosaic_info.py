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
from .mosaic_levy import MosaicLevy, OptionalMosaicLevyType
from .mosaic_properties import MosaicProperties
from ..account.public_account import PublicAccount
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['MosaicInfo']


@util.inherit_doc
@util.dataclass(frozen=True, levy=None)
class MosaicInfo(util.DTOSerializable):
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
    :param levy: (Optional) Levy for mosaic.

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
                levy: MosaicLevyDTO

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
    levy: OptionalMosaicLevyType

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

    def is_levy_mutable(self) -> bool:
        """Get if levy is mutable. Default false."""
        return self.properties.levy_mutable

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'meta': {
                'id': self.meta_id,
            },
            'mosaic': {
                'mosaicId': self.mosaic_id.to_dto(),
                'supply': util.u64_to_dto(self.supply),
                'height': util.u64_to_dto(self.height),
                'owner': self.owner.to_dto(network_type),
                'revision': util.u32_to_dto(self.revision),
                'properties': self.properties.to_dto(),
                'levy': {},
            },
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        meta_dto = data['meta']
        mosaic_dto = data['mosaic']
        levy_dto = mosaic_dto['levy']
        levy = MosaicLevy.from_dto(levy_dto) if levy_dto else None
        return cls(
            meta_id=meta_dto['id'],
            mosaic_id=MosaicId.from_dto(mosaic_dto['mosaicId']),
            supply=util.u64_from_dto(mosaic_dto['supply']),
            height=util.u64_from_dto(mosaic_dto['height']),
            owner=PublicAccount.from_dto(mosaic_dto['owner'], network_type),
            revision=util.u32_from_dto(mosaic_dto['revision']),
            properties=MosaicProperties.from_dto(mosaic_dto['properties']),
            levy=levy,
        )
