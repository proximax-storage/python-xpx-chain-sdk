"""
    mosaic
    ======

    Description of an asset.

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

from .mosaic_id import MosaicId
from ..blockchain.network_type import OptionalNetworkType
from ..namespace.namespace_id import NamespaceId
from ... import util

__all__ = ['Mosaic']

IdType = typing.Union[MosaicId, NamespaceId]


@util.inherit_doc
@util.dataclass(frozen=True, amount=0)
class Mosaic(util.Model):
    """
    Basic information describing a mosaic.

    :param id: Identifier for mosaic.
    :param amount: Mosaic quantity in the smallest unit possible.

    DTO Format:
        .. code-block:: yaml

            MosaicDTO:
                id: UInt64DTO
                amount: UInt64DTO
    """

    id: IdType
    amount: int
    CATBUFFER_SIZE: typing.ClassVar[int] = 2 * util.U64_BYTES

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'id', 'amount'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'amount': util.u64_to_dto(self.amount),
            'id': util.u64_to_dto(int(self.id)),
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        mosaic_id = MosaicId(util.u64_from_dto(data['id']))
        amount = util.u64_from_dto(data['amount'])
        return cls(mosaic_id, amount)

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None,
        fee_strategy: typing.Optional[util.FeeCalculationStrategy] = util.FeeCalculationStrategy.MEDIUM,
    ) -> bytes:
        mosaic_id = util.u64_to_catbuffer(int(self.id))
        amount = util.u64_to_catbuffer(self.amount)
        return mosaic_id + amount

    @classmethod
    def create_from_catbuffer(
        cls,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ):
        mosaic_id = MosaicId(util.u64_from_catbuffer(data[:8]))
        amount = util.u64_from_catbuffer(data[8:16])
        return cls(mosaic_id, amount)


MosaicList = typing.Sequence[Mosaic]
