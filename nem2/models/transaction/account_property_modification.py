"""
    account_property_modification
    =============================

    Account property modification type and value.

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

from ..account.account_property import PropertyValue
from ..account.address import Address
from ..account.property_modification_type import PropertyModificationType
from ..blockchain.network_type import OptionalNetworkType
from ..mosaic.mosaic_id import MosaicId
from ..transaction.transaction_type import TransactionType
from ... import util

__all__ = ['AccountPropertyModification']

def to_dto(value: PropertyValue) -> typing.Union[str, list, int]:
    """Serialize property modification value to DTO."""

    if isinstance(value, Address):
        return value.address
    elif isinstance(value, MosaicId):
        return util.u64_to_dto(int(value.id))
    elif isinstance(value, Transaction):
        return value.to_dto()
    else:
        raise NotImplementedError


def from_dto(data: typing.Union[str, list, int]) -> PropertyValue:
    """Load property modification value from DTO."""

    if isinstance(data, str):
        return Address(data)
    elif isinstance(data, list):
        return MosaicId(util.u64_from_dto(data))
    elif isinstance(data, int):
        return TransactionType.create_from_dto(data)
    else:
        raise NotImplementedError


# TODO(ahuszagh) Add unittests...
@util.inherit_doc
@util.dataclass(frozen=True)
class AccountPropertyModification(util.DTO):
    """
    Account property modification type and value.

    :param modification_type: Property modification type.
    :param value: Modification value.
    """

    modification_type: PropertyModificationType
    value: PropertyValue

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            # TODO(ahuszagh) Check when stabilized
            'modificationType': self.modification_type.to_dto(network_type),
            'value': to_dto(self.value),
        }

    @classmethod
    def create_from_dto(
        cls,
        data: dict,
        network_type: OptionalNetworkType = None,
    ):
        type = data['modificationType']
        return cls(
            # TODO(ahuszagh) Check when stabilized
            modification_type=PropertyModificationType.create_from_dto(type),
            value=from_dto(data['value']),
        )

#    def to_catbuffer(
#        self,
#        network_type: OptionalNetworkType = None,
#    ) -> bytes:
#        # uint8_t[32] signer
#        # uint8_t[64] signature
#        signer = util.unhexlify(self.signer.public_key)
#        signature = util.unhexlify(self.signature)
#        return signer + signature
#
#    @classmethod
#    def create_from_catbuffer(
#        cls,
#        data: bytes,
#        network_type: OptionalNetworkType = None,
#    ):
#        # uint8_t[32] signer
#        # uint8_t[64] signature
#        signer = PublicAccount.create_from_public_key(data[:32], network_type)
#        signature = data[32:96]
#        return cls(signature, signer)
