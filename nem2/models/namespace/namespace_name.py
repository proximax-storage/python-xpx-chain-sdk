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
import typing

from nem2 import util
from .namespace_id import NamespaceId
from ..blockchain.network_type import NetworkType

__all__ = ['NamespaceName']

OptionalNetworkType = typing.Optional[NetworkType]


@util.inherit_doc
@util.dataclass(frozen=True)
class NamespaceName(util.DTO):
    """
    Namespace name and identifier.

    :param namespace_id: Namespace ID.
    :param name: Namespace name.
    """

    namespace_id: NamespaceId
    name: str

    @classmethod
    def create_from_name(cls, name: str) -> NamespaceName:
        """
        Create namespace name and identifier from name.

        :param name: Namespace name.
        """
        namespace_id = NamespaceId(name)
        return cls(namespace_id, name)

    def to_dto(
        self,
        network_type: OptionalNetworkType = None
    ) -> dict:
        return {
            'namespaceId': self.namespace_id.to_dto(network_type),
            'name': self.name
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None
    ) -> NamespaceName:
        namespace_id = NamespaceId.from_dto(data['namespaceId'], network_type)
        name = data['name']
        return cls(namespace_id, name)
