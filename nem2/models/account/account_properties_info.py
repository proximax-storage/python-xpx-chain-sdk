"""
    account_properties_info
    =======================

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
import typing

from .account_properties import AccountProperties
from .account_properties_metadata import OptionalAccountPropertiesMetadata
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['AccountPropertiesInfo']


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountPropertiesInfo(util.DTOSerializable):
    """
    Basic information describing account properties.

    :param meta: Account properties metadata.
    :param account_properties: List of account properties.

    DTO Format:
        .. code-block:: yaml

            AccountPropertiesInfoDTO:
                meta: AccountPropertiesMetaDTO
                accountProperties: AccountPropertiesDTO
    """

    meta: OptionalAccountPropertiesMetadata
    account_properties: typing.Sequence[AccountProperties]

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        to_dto = AccountProperties.sequence_to_dto
        return {
            # TODO(ahuszagh) Check when stabilized
            'meta': {},
            'accountProperties': to_dto(self.account_properties, network_type),
        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        assert data['meta'] == {}
        from_dto = AccountProperties.sequence_from_dto
        return cls(
            # TODO(ahuszagh) Check when stabilized
            meta=None,
            account_properties=from_dto(data.get('accountProperties', []), network_type),
        )
