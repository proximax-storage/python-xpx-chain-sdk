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

from __future__ import annotations
import typing

from nem2 import util
from .mosaic_id import MosaicId
from .mosaic_levy_type import MosaicLevyType
from ..account.address import Address
from ..blockchain.network_type import OptionalNetworkType

__all__ = ['MosaicLevy']


# TODO(ahuszagh) This is not yet implemented in Catapult. Subject to change
@util.inherit_doc
@util.dataclass(frozen=True)
class MosaicLevy(util.DTO):
    """
    Information describing a mosaic levy.

    :param type: Levy type.
    :param recipient: Recipient of levy.
    :param mosaic_id: Mosaic in which levy is paid.
    :param fee: Fee amount for levy.
    """

    type: MosaicLevyType
    recipient: Address
    mosaic_id: MosaicId
    fee: int

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'type': self.type.to_dto(),
            'recipient': self.recipient.to_dto(),
            'mosaicId': self.mosaic_id.to_dto(),
            'fee': self.fee
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        return cls(
            type=MosaicLevyType.from_dto(data['type']),
            recipient=Address.from_dto(data['recipient']),
            mosaic_id=MosaicId.from_dto(data['mosaicId']),
            fee=data['fee'],
        )


OptionalMosaicLevyType = typing.Optional[MosaicLevy]
