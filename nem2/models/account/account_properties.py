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
class AccountProperties(util.DTOSerializable):
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

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        raise NotImplementedError
        # We're getting str from address.address, should be getting bytes.
#        return {
#            # TODO(ahuszagh) Check when stabilized
#            'address': util.b64encode(self.address.address),
#            'properties': AccountProperty.sequence_to_dto(self.properties, network_type),
#        }

    @classmethod
    def from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        raise NotImplementedError
#        properties = data.get('properties', [])
#        return cls(
#            # TODO(ahuszagh) Check when stabilized
#            address=Address.create_from_encoded(util.b64decode(data['address'])),
#            properties=AccountProperty.sequence_from_dto(properties, network_type),
#        )
