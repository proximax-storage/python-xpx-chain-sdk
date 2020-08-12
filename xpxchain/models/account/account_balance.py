"""
    account_balance
    ==================

    Account balance.

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

from .address import Address
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['AccountBalance']


@util.inherit_doc
@util.dataclass(frozen=True)
class AccountBalance(util.DTO):
    """
    Describe properties for an account.

    :param account: Public account.
    :param amount: Amount of the given mosaic

    DTO Format:
        .. code-block:: yaml

            AccountPropertiesDTO:
                # Base64(Base32(Address)) (56-bytes)
                address: string
                publicKey: string
                amount: UInt64DTO
    """

    address: Address
    public_key: str
    amount: int

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'address', 'publicKey', 'amount'}
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
            'publicKey': self.public_key,
            'amount': util.u64_to_dto(self.amount),
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
            public_key=data['publicKey'],
            amount=util.u64_from_dto(data['amount']),
        )
