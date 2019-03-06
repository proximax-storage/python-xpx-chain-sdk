"""
    namespace_id
    ============

    Identifier for a namespace.

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

IdType = typing.Union[str, int]


class NamespaceId(util.Tie):
    """Identifier for a namespace."""

    __slots__ = ('_id',)

    def __init__(self, id: IdType):
        """
        :param id: Identifier or name for namespace.
        """
        if isinstance(id, int):
            self._id = id
        elif isinstance(id, str):
            ids = util.generate_namespace_id(id) or [0]
            self._id = ids[-1]
        else:
            name = type(id).__name__
            raise TypeError(f"Expected str or int for NamespaceId, got {name}")

    @property
    def id(self):
        """Get raw identifier for namespace."""
        return self._id

    def __int__(self) -> int:
        return self.id

    def __index__(self) -> int:
        return self.__int__()

    @classmethod
    def from_hex(cls, data: str) -> 'NamespaceId':
        """
        Create instance of class from hex string.

        :param data: Hex-encoded ID data (with or without '0x' prefix).
        """

        return NamespaceId(int(data, 16))

    @util.doc(util.Tie.tie.__doc__)
    def tie(self) -> tuple:
        return super().tie()