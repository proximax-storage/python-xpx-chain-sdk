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

from .namespace_id import NamespaceId
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['NamespaceName']


@util.inherit_doc
@util.dataclass(frozen=True)
class NamespaceName(util.Model):
    """
    Namespace name and identifier.

    :param namespace_id: Namespace ID.
    :param name: Namespace name.
    """

    namespace_id: NamespaceId
    name: str

    @classmethod
    def create_from_name(cls, name: str):
        """
        Create namespace name and identifier from name.

        :param name: Namespace name.
        """
        namespace_id = NamespaceId(name)
        return cls(namespace_id, name.split('.')[-1])

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
        return {
            'namespaceId': self.namespace_id.to_dto(network_type),
            'name': self.name
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        namespace_id = NamespaceId.from_dto(data['namespaceId'], network_type)
        name = data['name']
        return cls(namespace_id, name)

    def to_catbuffer(
        self,
        network_type: OptionalNetworkType = None,
    ) -> bytes:
        # uint64_t id
        # uint8_t name_size
        # uint8_t[name_size] name
        id = self.namespace_id.to_catbuffer(network_type)
        name_size = util.u8_to_catbuffer(len(self.name))
        name = self.name.encode('ascii')

        return id + name_size + name

    @classmethod
    def from_catbuffer_pair(
        cls,
        data: bytes,
        network_type: OptionalNetworkType = None,
    ):
        id, data = NamespaceId.from_catbuffer_pair(data, network_type)
        name_size = util.u8_from_catbuffer(data[:1])
        data = data[1:]
        name = data[:name_size].decode('ascii')
        inst = cls(id, name)

        return inst, data[name_size:]
