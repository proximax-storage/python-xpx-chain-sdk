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


class MosaicName(util.Dto, util.Tie):
    """Mosaic name and identifiers."""

    _mosaic_id: 'MosaicId'
    _name: str
    _parent_id: 'NamespaceId'

    def __init__(self,
        mosaic_id: 'MosaicId',
        name: str,
        parent_id: 'NamespaceId'
    ) -> None:
        """
        :param mosaic_id: Mosaic ID.
        :param name: Mosaic name.
        :param parent_id: Parent namespace ID.
        """
        self._mosaic_id = mosaic_id
        self._name = name
        self._parent_id = parent_id

    @property
    def mosaic_id(self) -> 'MosaicId':
        """Get the mosaic ID."""
        return self._mosaic_id

    mosaicId = util.undoc(mosaic_id)

    @property
    def name(self) -> str:
        """Get the mosaic name."""
        return self._name

    @property
    def parent_id(self) -> 'NamespaceId':
        """Get the parent namespace ID."""
        return self._parent_id

    parentId = util.undoc(parent_id)

    @util.doc(util.Dto.to_dto)
    def to_dto(self) -> dict:
        return {
            'mosaicId': self.mosaic_id.to_dto(),
            'name': self.name,
            'parentId': self.parent_id.to_dto(),
        }

    @util.doc(util.Dto.from_dto)
    @classmethod
    def from_dto(cls, data: dict) -> 'MosaicName':
        mosaic_id = NamespaceId.from_dto(data['mosaicId'])
        name = data['name']
        parent_id = NamespaceId.from_dto(data['parentId'])
        return cls(mosaic_id, name, parent_id)
