"""
    mosaic_levy
    ===========

    Detailed information describing a levy, or tax on asset transfers.

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
from .mosaic_levy_type import MosaicLevyType
from ..account.address import Address


# TODO(ahuszagh) This is not yet implemented in Catapult.
# Subject to change
class MosaicLevy(util.Dto, util.Tie):
    """Information describing a mosaic levy."""

    __slots__ = (
        '_type',
        '_recipient',
        '_mosaic_id',
        '_fee',
    )

    def __init__(self,
        type: 'MosaicLevyType',
        recipient: 'Address',
        mosaic_id: 'MosaicId',
        fee: int,
    ):
        """
        :param type: Levy type.
        :param recipient: Recipient of levy.
        :param mosaic_id: Mosaic in which levy is paid.
        :param fee: Fee amount for levy.
        """
        self._type = type
        self._recipient = recipient
        self._mosaic_id = mosaic_id
        self._fee = fee

    @property
    def type(self):
        """Get the levy type."""
        return self._type

    @property
    def recipient(self):
        """Get the recipient of levy."""
        return self._recipient

    @property
    def mosaic_id(self):
        """Get the mosaic in which the levy is paid."""
        return self._mosaic_id

    mosaicId = util.undoc(mosaic_id)

    @property
    def fee(self):
        """Get the fee amount for levy."""
        return self._fee

    @util.doc(util.Tie.tie)
    def tie(self) -> tuple:
        return super().tie()

    @util.doc(util.Dto.to_dto)
    def to_dto(self) -> dict:
        # TODO(ahuszagh) This differs, since it seems the old
        # way was a mosaic name.
        return {
            'type': self.type.to_dto(),
            'recipient': self.address.to_dto(),
            'mosaicId': self.mosaic_id.to_dto(),
            'fee': self.fee
        }

    @util.doc(util.Dto.from_dto)
    @classmethod
    def from_dto(cls, data: dict) -> 'MosaicLevy':
        # TODO(ahuszagh) This differs, since it seems the old
        # way was a mosaic name.
        return cls(
            type=MosaicLevyType.from_dto(data['type']),
            recipient=Address.from_dto(data['recipient']),
            mosaic_id=MosaicId.from_dto(data['mosaicId']),
            fee=data['fee'],
        )
