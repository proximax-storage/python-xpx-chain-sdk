"""
    mosaic_info
    ===========

    Detailed information describing a NEM asset.

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

from nem2 import util


class MosaicInfo(util.Tie):
    """
    NEM mosaic information.

    Information describing a custom NEM asset.
    """

    __slots__ = (
        '_active',
        '_index',
        '_meta_id',
        '_id',
        '_nonce',
        '_supply',
        '_height',
        '_owner',
        '_properties',
        '_levy',
    )

    def __init__(self,
        active: bool,
        index: int,
        meta_id: str,
        id: 'MosaicId',
        nonce: 'MosaicNonce',
        supply: int,
        height: int,
        owner: 'PublicAccount',
        properties: 'MosaicProperties',
        # TODO(ahuszagh) Need to check the actual form of the levy.
        levy = None,
    ) -> None:
        """
        :param active: Mosaic is active.
        :param index: Mosaic index.
        :param meta_id: Mosaic metadata ID.
        :param id: Mosaic ID.
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
        self._id = id
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
    def id(self) -> 'MosaicId':
        """Get the mosaic ID."""
        return self._id

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
    def levy(self):
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

    @util.doc(util.Tie.tie)
    def tie(self) -> tuple:
        return super().tie()
