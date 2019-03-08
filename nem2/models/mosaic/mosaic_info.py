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

import typing

from nem2 import util
from .mosaic_id import MosaicId
from ..account.public_account import PublicAccount

if typing.TYPE_CHECKING:
    from .mosaic_levy import MosaicLevy
    from .mosaic_nonce import MosaicNonce
    from .mosaic_properties import MosaicProperties

OptionalMosaicLevyType = typing.Optional['MosaicLevy']


# TODO(ahuszagh) Needs to/from dto.
#   Issues:
#       nonce cannot be generated from the data provided.
#           Mosaic ID is a hash of nonce + public key, cannot reverse.
#       namespace ID is missing in info, not in DTO.
class MosaicInfo(util.Dto, util.Tie):
    """Information describing a mosaic."""

    _active: bool
    _index: int
    _meta_id: str
    _mosaic_id: 'MosaicId'
    _nonce: 'MosaicNonce'
    _supply: int
    _height: int
    _owner: 'PublicAccount'
    _properties: 'MosaicProperties'
    _levy: OptionalMosaicLevyType

    def __init__(self,
        active: bool,
        index: int,
        meta_id: str,
        mosaic_id: 'MosaicId',
        nonce: 'MosaicNonce',
        supply: int,
        height: int,
        owner: 'PublicAccount',
        properties: 'MosaicProperties',
        levy: OptionalMosaicLevyType = None,
    ) -> None:
        """
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
        self._active = active
        self._index = index
        self._meta_id = meta_id
        self._mosaic_id = mosaic_id
        self._nonce = nonce
        self._supply = supply
        self._height = height
        self._owner = owner
        self._properties = properties
        self._levy = levy

    # TODO(ahuszagh) Document and finish implementing...

    @property
    def active(self) -> bool:
        """Get if mosaic is active."""
        return self._active

    @property
    def index(self) -> int:
        """Get the mosaic index."""
        return self._index

    @property
    def meta_id(self) -> str:
        """Get the mosaic metadata ID."""
        return self._meta_id

    @property
    def mosaic_id(self) -> 'MosaicId':
        """Get the mosaic ID."""
        return self._mosaic_id

    @property
    def nonce(self) -> 'MosaicNonce':
        """Get the mosaic nonce."""
        return self._nonce

    @property
    def supply(self) -> int:
        """Get the mosaic supply."""
        return self._supply

    @property
    def height(self) -> int:
        """Get the block height when mosaic was created."""
        return self._height

    @property
    def owner(self) -> 'PublicAccount':
        """Get the account that owns mosaic."""
        return self._owner

    @property
    def properties(self) -> 'MosaicProperties':
        """Get the mosaic properties."""
        return self._properties

    # TODO(ahuszagh) Add type annotations
    @property
    def levy(self) -> OptionalMosaicLevyType:
        """Get the mosaic levy."""
        return self._levy

    @property
    def divisibility(self) -> int:
        """Get the decimal place mosaic can be divided into."""
        return self.properties.divisibility

    @property
    def duration(self) -> int:
        """Get the number of blocks the mosaic will be available."""
        return self.properties.duration

    def is_supply_mutable(self) -> bool:
        """Mosaic allows a supply change later on. Defaults to false."""
        return self.properties.supply_mutable

    isSupplyMutable = util.undoc(is_supply_mutable)

    def is_transferable(self) -> bool:
        """Allow transfer of funds from accounts other than the creator. Defaults to true."""
        return self.properties.transferable

    isTransferable = util.undoc(is_transferable)

    def is_levy_mutable(self) -> bool:
        """Get if levy is mutable. Defaults to false."""
        return self.properties.levy_mutable

    isLevyMutable = util.undoc(is_levy_mutable)

    @util.doc(util.Dto.to_dto)
    def to_dto(self) -> dict:
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
        #         'owner': self.owner.public_key,
        #         'properties': self.properties.to_dto(),
        #         'levy': levy,
        #     },
        # }
        raise NotImplementedError

    @util.doc(util.Dto.from_dto)
    @classmethod
    def from_dto(cls, data: dict) -> 'MosaicLevy':
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
        #     owner=PublicAccount.create_from_public_key(mosaic['owner'], network_type),
        #     properties=MosaicProperties.from_dto(mosaic['properties']),
        #     levy=levy,
        # )
        raise NotImplementedError
