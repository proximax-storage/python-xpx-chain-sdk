"""
    account_properties_metadata
    ===========================

    Account properties metadata.

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
from ... import util

__all__ = ['AccountPropertiesMetadata']


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountPropertiesMetadata(util.Object):
    """
    Metadata describing account properties.

    DTO Format:
        .. code-block:: yaml

            AccountPropertiesMetaDTO:
                # Hex(Id) (24-bytes)
                id: string
    """

    id: str

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            # TODO(ahuszagh) Check when stabilized
            'id': self.id,
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        return cls(
            # TODO(ahuszagh) Check when stabilized
            id=data['id'],
        )
