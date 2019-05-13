"""
    namespace_name
    ==============

    Describes a namespace by name and identifier.

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
import re
import typing

from .namespace_id import NamespaceId
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['NamespaceName']


@util.inherit_doc
@util.dataclass(frozen=True, parent_id=None)
class NamespaceName(util.DTO):
    """
    Namespace name and identifier.

    :param namespace_id: Namespace ID.
    :param name: Namespace name.

    DTO Format:
        .. code-block:: yaml

            NamespaceNameDTO:
                namespaceId: UInt64DTO
                name: string
                parentId?: UInt64DTO
    """

    namespace_id: NamespaceId
    name: str
    parent_id: typing.Optional[NamespaceId]

    @classmethod
    def create_from_name(cls, name: str):
        """
        Create namespace name and identifier from name.

        :param name: Namespace name.
        """

        ids = util.generate_namespace_id(name)
        if len(ids) == 0:
            namespace_id = NamespaceId(0)
            parent_id = None
        elif len(ids) == 1:
            namespace_id = NamespaceId(ids[0])
            parent_id = None
        else:
            namespace_id = NamespaceId(ids[-1])
            parent_id = NamespaceId(ids[-2])

        return cls(
            namespace_id=namespace_id,
            name=name.split('.')[-1],
            parent_id=parent_id,
        )

    def is_valid(self) -> bool:
        """Determine if the namespace name is valid."""
        return (
            len(self.name) <= 64
            and re.match(r'\A[a-z0-9_-]+\Z', self.name) is not None
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        data = {
            'namespaceId': util.u64_to_dto(int(self.namespace_id)),
            'name': self.name
        }
        if self.parent_id is not None:
            data['parentId'] = util.u64_to_dto(int(self.parent_id))

        return data

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        parent_id = None
        if 'parentId' in data:
            parent_id = NamespaceId(util.u64_from_dto(data['parentId']))
        return cls(
            namespace_id=NamespaceId(util.u64_from_dto(data['namespaceId'])),
            name=data['name'],
            parent_id=parent_id,
        )
