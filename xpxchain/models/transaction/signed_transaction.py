"""
    signed_transaction
    ==================

    Signed transaction data.

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

from .transaction_type import TransactionType
from ..blockchain.network_type import NetworkType
from ... import util

__all__ = ['SignedTransaction']

AnyStr1 = typing.TypeVar('AnyStr1', bytes, str)
AnyStr2 = typing.TypeVar('AnyStr2', bytes, str)
AnyStr3 = typing.TypeVar('AnyStr3', bytes, str)


@util.inherit_doc
@util.dataclass(frozen=True)
class SignedTransaction(util.Object):
    """
    Signed transaction data and signature/hash.

    :param payload: Serialized transaction data.
    :param hash: Transaction hash.
    :param signer: Transaction signer (public key).
    :param type: Transaction type.
    :param network_type: Signer network type.
    """

    payload: str
    hash: str
    signer: str
    type: TransactionType
    network_type: NetworkType

    def __init__(
        self,
        payload: typing.AnyStr,
        hash: typing.AnyStr,
        signer: typing.AnyStr,
        type: TransactionType,
        network_type: NetworkType,
    ) -> None:
        payload = util.encode_hex(payload)
        hash = util.encode_hex(hash)
        signer = util.encode_hex(signer)
        if len(hash) != 64:
            raise ValueError('Transaction hash must be 64 characters long.')
        if len(signer) not in (0, 64):
            raise ValueError('Signer public key must be empty or 64 characters long.')
        self._set('payload', payload)
        self._set('hash', hash)
        self._set('signer', signer)
        self._set('type', type)
        self._set('network_type', network_type)

    @classmethod
    def create_from_announced(
        cls,
        hash: typing.AnyStr,
        type: TransactionType,
        network_type: NetworkType,
    ):
        """
        Create minimal signed transaction from announced transaction hash and type.

        :param hash: Transaction hash.
        :param type: Transaction type.
        :param network_type: Signer network type.
        """
        return cls('', hash, '', type, network_type)  # type: ignore

    def __eq__(self, other) -> bool:
        # Since we may use `create_from_announced` and we want it
        # to compare equal, we ignore payload and signer in equality checks.
        if not isinstance(other, SignedTransaction):
            return False
        lhs = (self.hash, self.type, self.network_type)
        rhs = (other.hash, other.type, other.network_type)
        return lhs == rhs
