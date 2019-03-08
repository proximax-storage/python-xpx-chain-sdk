"""
    namespace_type
    ==============

    Enumerations for namespace types.

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


class NamespaceType(util.IntEnumDto):
    """Namespace type."""

    ROOT_NAMESPACE = 0
    SUB_NAMESPACE = 1

    def description(self) -> str:
        """Describe enumerated values in detail."""

        return DESCRIPTION[self]

    @util.doc(util.Dto.to_dto)
    def to_dto(self) -> int:
        return int(self)

    @util.doc(util.Dto.from_dto)
    @classmethod
    def from_dto(cls, data: int) -> 'NamespaceType':
        return cls(data)


DESCRIPTION = {
    NamespaceType.ROOT_NAMESPACE: "Root namespace.",
    NamespaceType.SUB_NAMESPACE: "Sub namespace.",
}
