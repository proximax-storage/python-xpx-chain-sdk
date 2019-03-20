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

from nem2 import util
from .mosaic_id import MosaicId
from .mosaic_levy import OptionalMosaicLevyType
from .mosaic_nonce import MosaicNonce
from .mosaic_properties import MosaicProperties
from ..account.public_account import PublicAccount
from ..blockchain.network_type import OptionalNetworkType

__all__ = ['MosaicInfo']


# TODO(ahuszagh) Needs to/from dto.
#   Issues:
#       nonce cannot be generated from the data provided.
#           Mosaic ID is a hash of nonce + public key, cannot reverse.
#       namespace ID is missing in info, not in DTO.
@util.inherit_doc
@util.dataclass(frozen=True, levy=None)
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
    :param levy: (Optional) Levy for mosaic.
    """

    active: bool
    index: int
    meta_id: str
    mosaic_id: MosaicId
    nonce: MosaicNonce
    supply: int
    height: int
    owner: PublicAccount
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
        # TODO(ahuszagh) This differs, since it seems the old
        # way was a mosaic name.
        #
        # levy = self.levy.to_dto() if self.levy else {}
        # mosaic_id = MosaicId.create_from_nonce(self.nonce, self.owner)
        # return {
        #     'meta': {
        #         'active': self.active,
        #         'index': self.index,
        #         'id': self.meta_id,
        #     },
        #     'mosaic': {
        #         # TODO(ahuszagh)
        #         #'namespaceId'
        #         'mosaicId': self.mosaic_id.to_dto(),
        #         'supply': util.uint64_to_dto(self.supply),
        #         'height': util.uint64_to_dto(self.height),
        #         'owner': self.owner.to_dto(network_type),
        #         'properties': self.properties.to_dto(),
        #         'levy': levy,
        #     },
        # }
        raise NotImplementedError

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        # Namespace ID is clearly the parent ID.
        # Nonce is clearly found somewhere???
        # TODO(ahuszagh) We obviously cannot get the nonce...
        # So remove it?
        # TODO(ahuszagh) need network type...
        # TODO(ahuszagh) This differs, since it seems the old
        # way was a mosaic name.
        #
        # meta = data['meta']
        # mosaic = data['mosaic']
        # levy = mosaic['levy']
        # levy = MosaicLevy.from_dto(levy) if levy else None
        # mosaic_id = MosaicId.from_dto(mosaic['mosaicId'])
        # return cls(
        #     active=meta['active'],
        #     index=meta['index'],
        #     meta_id=meta['id'],
        #     # TODO(ahuszagh) Likely remove.
        #     #'nonce'
        #     mosaic_id=mosaic_id,
        #     supply=util.dto_to_uint64(mosaic['supply']),
        #     height=util.dto_to_uint64(mosaic['height']),
        #     owner=PublicAccount.from_dto(mosaic['owner'], network_type),
        #     properties=MosaicProperties.from_dto(mosaic['properties']),
        #     levy=levy,
        # )
        raise NotImplementedError
