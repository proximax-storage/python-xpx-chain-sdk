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

from nem2 import util
from .mosaic_id import MosaicId
from ..namespace.namespace_id import NamespaceId


@util.inherit_doc
@util.dataclass(frozen=True)
class MosaicName(util.Dto):
    """
    Mosaic name and identifiers.

    :param mosaic_id: Mosaic ID.
    :param name: Mosaic name.
    :param parent_id: Parent namespace ID.
    """

    mosaic_id: 'MosaicId'
    name: str
    parent_id: 'NamespaceId'

    def to_dto(self) -> dict:
        return {
            'mosaicId': self.mosaic_id.to_dto(),
            'name': self.name,
            'parentId': self.parent_id.to_dto(),
        }

    @classmethod
    def from_dto(cls, data: dict) -> 'MosaicName':
        mosaic_id = MosaicId.from_dto(data['mosaicId'])
        name = data['name']
        parent_id = NamespaceId.from_dto(data['parentId'])
        return cls(mosaic_id, name, parent_id)
