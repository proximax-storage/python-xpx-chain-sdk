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

from nem2 import util
from .mosaic_id import MosaicId
from ..blockchain.network_type import OptionalNetworkType
from ..namespace.namespace_id import NamespaceId

__all__ = ['Mosaic']

IdType = typing.Union[MosaicId, NamespaceId]
SIZE = MosaicId.CATBUFFER_SIZE + util.U64_BYTES


@util.inherit_doc
@util.dataclass(frozen=True, amount=0)
class Mosaic(util.Model):
    """
    Basic information describing a mosaic.

    :param id: Identifier for mosaic.
    :param amount: Mosaic quantity in the smallest unit possible.
    """

    id: IdType
    amount: int
    CATBUFFER_SIZE: typing.ClassVar[int] = SIZE

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'amount': util.u64_to_dto(self.amount),
            'id': self.id.to_dto(network_type),
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        mosaic_id = MosaicId.from_dto(data['id'], network_type)
        amount = util.u64_from_dto(data['amount'])
        return cls(mosaic_id, amount)

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None,
    ) -> bytes:
        mosaic_id = self.id.to_catbuffer(network_type)
        amount = util.u64_to_catbuffer(self.amount)
        return mosaic_id + amount

    @classmethod
    def from_catbuffer(
        cls,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ):
        mosaic_id, data = MosaicId.from_catbuffer_pair(data, network_type)
        amount = util.u64_from_catbuffer(data)
        return cls(mosaic_id, amount)


MosaicList = typing.Sequence[Mosaic]
