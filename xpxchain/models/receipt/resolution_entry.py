"""
    resolution_entry
    ================

    Resolution entry

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

from ..blockchain.network_type import OptionalNetworkType
from .source import Source
from ... import util

__all__ = ['ResolutionEntry']


@util.inherit_doc
@util.dataclass(frozen=True)
class ResolutionEntry(util.DTO):
    """
    Resolution entry.

    :param source: The receipt source.
    :param resolved: A resolved address or resolved mosaicId.

    DTO Format:
        .. code-block:: yaml

            ResolutionEntryDTO:
                source: SourceDTO
                resolved: Uint64DTO
    """

    source: Source
    resolved: int

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'source', 'resolved'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'source': self.source.to_dto(),
            'resolved': util.u64_to_dto(self.resolved),
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
            source=Source.create_from_dto(data['source']),
            resolved=util.u64_from_dto(data['resolved']),
        )
