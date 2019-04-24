"""
    namespace_info
    ==============

    Data and metadata describing a namespace.

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

from .alias import Alias
from .alias_type import AliasType
from .namespace_id import NamespaceId, NamespaceIdList
from .namespace_type import NamespaceType
from ..account.address import Address
from ..account.public_account import PublicAccount
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['NamespaceInfo']


@util.inherit_doc
@util.dataclass(frozen=True, alias=Alias(AliasType.NONE, None))
class NamespaceInfo(util.DTO):
    """
    Information describing a namespace.

    :param active: Namespace is active.
    :param index: Namespace index.
    :param meta_id: Metadata ID.
    :param type: Namespace type.
    :param depth: Level of namespace.
    :param levels: Namespace ID levels.
    :param parent_id: Namespace parent ID.
    :param owner: Account that owns namespace.
    :param start_height: Block height at which ownership begins.
    :param end_height: Block height at which ownership ends.
    :param alias: Alias linked to a namespace.
    """

    active: bool
    index: int
    meta_id: str
    type: NamespaceType
    depth: int
    levels: NamespaceIdList
    parent_id: NamespaceId
    owner: PublicAccount
    start_height: int
    end_height: int
    alias: Alias

    @property
    def id(self) -> NamespaceId:
        """Get the namespace ID."""
        return self.levels[-1]

    def is_root(self) -> bool:
        """Get if namespace is root namespace."""

        return self.type == NamespaceType.ROOT_NAMESPACE

    def is_subnamespace(self) -> bool:
        """Get if namespace is subnamespace."""

        return self.type == NamespaceType.SUB_NAMESPACE

    def has_alias(self) -> bool:
        """Get if namespace has alias."""

        return self.alias.type != AliasType.NONE

    def parent_namespace_id(self) -> NamespaceId:
        """Get parent namespace ID."""

        if self.is_root():
            raise ValueError("Unable to get parent namespace ID of root namespace.")
        return self.parent_id

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        meta = {
            'active': self.active,
            'index': self.index,
            'id': self.meta_id,
        }
        namespace = {
            'type': self.type.to_dto(network_type),
            'depth': self.depth,
            'parentId': self.parent_id.to_dto(network_type),
            'owner': self.owner.to_dto(network_type),
            'ownerAddress': self.owner.address.to_dto(network_type),
            'startHeight': util.u64_to_dto(self.start_height),
            'endHeight': util.u64_to_dto(self.end_height),
        }

        # levels => ('level0', 'level1', ...)
        for i in range(self.depth):
            key = f"level{i}"
            namespace[key] = self.levels[i].to_dto(network_type)

        # Optional alias.
        if self.alias.type != AliasType.NONE:
            namespace['alias'] = self.alias.to_dto(network_type)

        return {
            'meta': meta,
            'namespace': namespace,
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        meta = data['meta']
        namespace = data['namespace']
        address = Address.from_dto(namespace['ownerAddress'], network_type)
        network_type = address.network_type
        depth = namespace['depth']

        # Load the levels.
        levels = []
        for i in range(depth):
            levels.append(NamespaceId.from_dto(namespace[f'level{i}'], network_type))

        # Load the alias.
        try:
            alias = Alias.from_dto(namespace['alias'], network_type)
        except KeyError:
            alias = Alias(AliasType.NONE, None)

        return cls(
            active=meta['active'],
            index=meta['index'],
            meta_id=meta['id'],
            type=NamespaceType.from_dto(namespace['type'], network_type),
            depth=depth,
            levels=levels,
            parent_id=NamespaceId.from_dto(namespace['parentId'], network_type),
            owner=PublicAccount.from_dto(namespace['owner'], network_type),
            start_height=util.u64_from_dto(namespace['startHeight']),
            end_height=util.u64_from_dto(namespace['endHeight']),
            alias=alias,
        )
