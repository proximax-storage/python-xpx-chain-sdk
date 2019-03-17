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

from nem2 import util
from .transaction_type import TransactionType
from ..blockchain.network_type import NetworkType


@util.inherit_doc
@util.dataclass
class SignedTransaction:
    """
    Signed transaction data and signature/hash.

    :param payload: Serialized transaction data.
    :param hash: Transaction hash.
    :param signer: Transaction signer (public key).
    :param type: Transaction type.
    :param network_type: Signer network type.
    """

    payload: bytes
    hash: str
    signer: str
    type: TransactionType
    network_type: NetworkType

    def __init__(
        self,
        payload: bytes,
        hash: str,
        signer: str,
        type: TransactionType,
        network_type: NetworkType,
    ):
        if len(hash) != 64:
            raise ValueError('Transaction hash must be 64 characters long.')
        self._set('payload', payload)
        self._set('hash', hash)
        self._set('signer', signer)
        self._set('type', type)
        self._set('network_type', network_type)
