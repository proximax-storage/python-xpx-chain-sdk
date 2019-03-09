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


@util.inherit_doc
@util.dataclass(frozen=True)
class NamespaceId(util.IntMixin, util.Dto):
    """
    Identifier for a namespace.

    :param id: Identifier or name for namespace.
    """

    id: int

    def __init__(self, id: IdType) -> None:
        if isinstance(id, int):
            object.__setattr__(self, 'id', id)
        elif isinstance(id, str):
            ids = util.generate_namespace_id(id) or [0]
            object.__setattr__(self, 'id', ids[-1])
        else:
            name = type(id).__name__
            raise TypeError(f"Expected str or int for NamespaceId, got {name}")

    def __int__(self) -> int:
        return self.id

    def to_dto(self) -> util.U64DTOType:
        return util.uint64_to_dto(self.id)

    @classmethod
    def from_dto(cls, data: util.U64DTOType) -> 'NamespaceId':
        return cls(util.dto_to_uint64(data))
