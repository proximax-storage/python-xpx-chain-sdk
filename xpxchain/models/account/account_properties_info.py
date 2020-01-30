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

from .account_properties import AccountProperties
from .account_properties_metadata import AccountPropertiesMetadata
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['AccountPropertiesInfo']


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountPropertiesInfo(util.DTO):
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

    meta: AccountPropertiesMetadata
    account_properties: AccountProperties

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'meta', 'accountProperties'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'meta': self.meta.to_dto(network_type),
            'accountProperties': self.account_properties.to_dto(network_type),
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        from_dto = AccountProperties.create_from_dto
        return cls(
            meta=AccountPropertiesMetadata.create_from_dto(data['meta'], network_type),
            account_properties=from_dto(data['accountProperties'], network_type),
        )
