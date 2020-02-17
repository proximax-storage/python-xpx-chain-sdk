"""
    account_names
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

from .address import Address
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['AccountNames']


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountNames(util.DTO):
    """
    Describe properties for an account.

    :param address: Account address.
    :param names: The mosaic linked namespace names..

    DTO Format:
        .. code-block:: yaml

            AccountPropertiesDTO:
                # Base64(Base32(Address)) (56-bytes)
                address: string
                names: string[]
    """

    address: Address
    names: typing.Sequence[str]

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'address', 'names'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'address': self.address.address,
            'names': self.names,
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
            address=Address.create_from_encoded(data['address']),
            names=data['names'],
        )
