"""
    sync_announce
    =============

    Signed transaction to announce and sync to network.

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

from .signed_transaction import SignedTransaction
from ..account.address import Address
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['SyncAnnounce']


@util.dataclass(frozen=True)
class SyncAnnounce(util.DTO):
    """
    Signed transaction to announce and sync.

    :param payload: Signed transaction data.
    :param hash: Transaction hash.
    :param address: Transaction address.
    """

    payload: str
    hash: str
    address: str

    def __init__(
        self,
        payload: typing.AnyStr,
        hash: typing.AnyStr,
        address: str,
    ) -> None:
        payload = util.encode_hex(payload)
        hash = util.encode_hex(hash)
        if len(hash) != 64:
            raise ValueError('Transaction hash must be 64 characters long.')
        self._set('payload', payload)
        self._set('hash', hash)
        self._set('address', address)

    @classmethod
    def create(cls, transaction: SignedTransaction):
        """
        Create sync announce object from signed transaction data.

        :param transaction: Signed transaction data.
        """
        public_key = transaction.signer
        network_type = transaction.network_type
        address = Address.create_from_public_key(public_key, network_type)

        return cls(
            payload=transaction.payload,  # type: ignore
            hash=transaction.hash,  # type: ignore
            address=address.address,
        )

    @classmethod
    def validate_dto(cls, data: dict) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'payload', 'hash', 'address'}
        return (
            cls.validate_dto_required(data, required_keys)
            and cls.validate_dto_all(data, required_keys)
        )

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> dict:
        return {
            'payload': self.payload,
            'hash': self.hash,
            'address': self.address,
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
            payload=data['payload'],
            hash=data['hash'],
            address=data['address'],
        )
