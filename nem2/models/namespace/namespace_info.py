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

import typing

from nem2 import util
from .alias_type import AliasType
from .namespace_id import NamespaceId
from .namespace_type import NamespaceType

NamespaceIdListType = typing.Sequence['NamespaceId']


class NamespaceInfo(util.Tie):
    """Information describing a namespace."""

    __slots__ = (
        '_active',
        '_index',
        '_meta_id',
        '_type',
        '_depth',
        '_levels',
        '_parent_id',
        '_owner',
        '_start_height',
        '_end_height',
        '_alias',
    )

    def __init__(self,
        active: bool,
        index: int,
        meta_id: str,
        type: 'NamespaceType',
        depth: int,
        levels: NamespaceIdListType,
        parent_id: 'NamespaceId',
        owner: 'PublicAccount',
        start_height: int,
        end_height: int,
        alias: 'Alias',
    ):
        """
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
        self._active = active
        self._index = index
        self._meta_id = meta_id
        self._type = type
        self._depth = depth
        self._levels = levels
        self._parent_id = parent_id
        self._owner = owner
        self._start_height = start_height
        self._end_height = end_height
        self._alias = alias

    @property
    def active(self) -> bool:
        """Get if namespace is active."""
        return self._active

    @property
    def index(self) -> int:
        """Get the namespace index."""
        return self._index

    @property
    def meta_id(self) -> str:
        """Get the metadata ID."""
        return self._meta_id

    metaID = util.undoc(meta_id)

    @property
    def type(self) -> NamespaceType:
        """Get the namespace type."""
        return self._type

    @property
    def depth(self) -> int:
        """Get the level of namespace."""
        return self._depth

    @property
    def levels(self) -> NamespaceIdListType:
        """Get the namespace ID levels."""
        return self._levels

    @property
    def parent_id(self) -> NamespaceId:
        """Get the namespace parent ID."""
        return self._parent_id

    parentID = util.undoc(parent_id)

    @property
    def owner(self) -> 'PublicAccount':
        """Get the account that owns the namespace."""
        return self._owner

    @property
    def start_height(self) -> int:
        """Get the block height at which ownership begins."""
        return self._start_height

    startHeight = util.undoc(start_height)

    @property
    def end_height(self) -> int:
        """Get the block height at which ownership ends."""
        return self._end_height

    endHeight = util.undoc(end_height)

    @property
    def alias(self) -> 'Alias':
        """Get the alias linked to namespace."""
        return self._alias

    @property
    def id(self) -> 'NamespaceId':
        """Get the namespace ID."""
        return self.levels[-1]

    def is_root(self) -> bool:
        """Get if namespace is root namespace."""

        return self.type == NamespaceType.ROOT_NAMESPACE

    isRoot = util.undoc(is_root)

    def is_subnamespace(self) -> bool:
        """Get if namespace is subnamespace."""

        return self.type == NamespaceType.SUB_NAMESPACE

    isSubnamespace = util.undoc(is_subnamespace)

    def has_alias(self) -> bool:
        """Get if namespace has alias."""

        return self.alias.type != AliasType.NONE

    hasAlias = util.undoc(has_alias)

    def parent_namespace_id(self) -> 'NamespaceId':
        """Get parent namespace ID."""

        if self.is_root():
            raise ValueError("Unable to get parent namespace ID of root namespace.")
        return self.parent_id

    @util.doc(util.Tie.tie.__doc__)
    def tie(self) -> tuple:
        return super().tie()