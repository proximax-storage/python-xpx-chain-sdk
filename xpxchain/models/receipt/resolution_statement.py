"""
    resolution_statement
    ====================

    Resolution statement.

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

from .resolution_entry import ResolutionEntry
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = [
    'ResolutionStatement',
]


@util.inherit_doc
@util.dataclass(frozen=True)
class ResolutionStatement(util.DTO):
    """
    A resolution statement keeps the relation between a namespace alias used in a transaction
    and the real address or mosaicId.

    :param height:
    :param unresolved:
    :param resolutionEntries: The array of resolution entries linked to the unresolved namespaceId.
    """

    height: int
    unresolved: int
    resolution_entries: typing.Sequence[ResolutionEntry]

    # DTO

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        required_keys = {'height', 'unresolved', 'resolutionEntries'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'height': util.u64_to_dto(self.height),
            'unresolved': util.u64_to_dto(self.unresolved),
            'resolutionEntries': [ResolutionEntry.to_dto(i) for i in self.resolution_entries]
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        return cls(
            height=util.u64_from_dto(data['mosaicId']),
            unresolved=util.u64_from_dto(data['unresolved']),
            resolution_entries=[ResolutionEntry.create_from_dto(i) for i in data['resolutionEntries']]
        )
