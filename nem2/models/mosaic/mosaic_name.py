"""
    mosaic_name
    ===========

    Describes a mosaic by name and identifier.

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
from ..blockchain.network_type import OptionalNetworkType
from ..namespace.namespace_id import NamespaceId
from ... import util

__all__ = ['MosaicName']


@util.inherit_doc
@util.dataclass(frozen=True)
class MosaicName(util.DTO):
    """
    Mosaic name and identifiers.

    :param mosaic_id: Mosaic ID.
    :param name: Mosaic name.
    :param parent_id: Parent namespace ID.

    DTO Format:
        .. code-block:: yaml

            MosaicNameDTO:
                parentId: UInt64DTO
                mosaicId: UInt64DTO
                name: string
    """

    mosaic_id: MosaicId
    name: str
    parent_id: NamespaceId

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'mosaicId': util.u64_to_dto(int(self.mosaic_id)),
            'name': self.name,
            'parentId': util.u64_to_dto(int(self.parent_id)),
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        return cls(
            mosaic_id=MosaicId(util.u64_from_dto(data['mosaicId'])),
            name=data['name'],
            parent_id=NamespaceId(util.u64_from_dto(data['parentId'])),
        )
