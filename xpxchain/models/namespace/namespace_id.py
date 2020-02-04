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
from ... import util

__all__ = ['NamespaceId']

IdType = typing.Union[str, int]


def id_to_int(id: IdType) -> int:
    """Convert identifier to int."""

    if isinstance(id, int):
        return id
    elif isinstance(id, str):
        ids = util.generate_namespace_id(id) or [0]
        return ids[-1]
    else:
        raise TypeError(f"Invalid type for ID, got {type(id).__name__}")


@util.inherit_doc
@util.dataclass(frozen=True)
class NamespaceId(util.IntMixin, util.Object):
    """
    Identifier for a namespace.

    :param id: Identifier or name for namespace.
    """

    id: int

    def __init__(self, id: IdType) -> None:
        self._set('id', id_to_int(id))

    def __int__(self) -> int:
        return self.id

    def get_id(self) -> str:
        return util.hexlify(self.id.to_bytes(8, 'big'))

    @property
    def encoded(self) -> str:
        """Get the namespace ID as a hex-encoded string."""
        decoded = util.u64_to_catbuffer(self.id)
        return util.hexlify(decoded)

    @classmethod
    def create_from_encoded(cls, encoded: typing.AnyStr):
        """
        Create namespace ID from hex-encoded string.

        :param encoded: ID bytes or hex-encoded bytes.
        """
        decoded = util.decode_hex(encoded, with_prefix=True)
        return cls(util.u64_from_catbuffer(decoded))


NamespaceIdList = typing.Sequence[NamespaceId]
