"""
    account_properties
    ==================

    List of properties for an account.

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

from .account_property import AccountProperty
from .address import Address
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['AccountProperties']


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountProperties(util.DTO):
    """
    Describe properties for an account.

    :param address: Account address.
    :param properties: Account properties.

    DTO Format:
        .. code-block:: yaml

            AccountPropertiesDTO:
                # Base64(Base32(Address)) (56-bytes)
                address: string
                properties: AccountPropertyDTO[]
    """

    address: Address
    properties: typing.Sequence[AccountProperty]

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_l1 = {'accountProperties'}
        required_l2 = {'address', 'properties'}
        return (
            cls.validate_dto_required(data, required_l1)
            and cls.validate_dto_all(data, required_l1)
            and cls.validate_dto_required(data['accountProperties'], required_l2)
            and cls.validate_dto_all(data['accountProperties'], required_l2)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        account_properties = {
            'address': self.address.hex,
            'properties': AccountProperty.sequence_to_dto(self.properties, network_type),
        }

        return {
            'accountProperties': account_properties,
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        account_properties = data['accountProperties']

        from_dto = AccountProperty.sequence_from_dto
        return cls(
            address=Address.create_from_encoded(account_properties['address']),
            properties=from_dto(account_properties['properties'], network_type),
        )
