"""
    account_link_transaction
    ========================

    Transaction to delegate account importance to a proxy account.

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

from .deadline import Deadline
from .inner_transaction import InnerTransaction
from .link_action import LinkAction
from .registry import register_transaction
from .transaction import Transaction
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ... import util

__all__ = [
    'AccountLinkTransaction',
    'AccountLinkInnerTransaction',
]


@util.inherit_doc
@util.dataclass(frozen=True)
@register_transaction('LINK_ACCOUNT')
class AccountLinkTransaction(Transaction):
    """
    Account link transaction.

    Delegates account importance to a proxy account for harvesting.

    :param network_type: Network type.
    :param version: Transaction version.
    :param deadline: Deadline to include transaction.
    :param max_fee: Max fee for the transaction. Higher fees increase priority.
    :param remote_account_key: Public key of the remote account.
    :param link_action: Account link action.
    :param signature: (Optional) Transaction signature (missing if embedded transaction).
    :param signer: (Optional) Account of transaction creator.
    :param transaction_info: (Optional) Transaction metadata.
    """

    remote_account_key: str
    link_action: LinkAction

    def __init__(
        self,
        network_type: NetworkType,
        version: TransactionVersion,
        deadline: Deadline,
        remote_account_key: str,
        link_action: LinkAction,
        max_fee: int = 0,
        signature: typing.Optional[str] = None,
        signer: typing.Optional[PublicAccount] = None,
        transaction_info: typing.Optional[TransactionInfo] = None,
    ) -> None:
        remote_account_key = util.encode_hex(remote_account_key)
        if len(remote_account_key) != 64:
            raise ValueError("Invalid remote account public key length.")
        super().__init__(
            TransactionType.LINK_ACCOUNT,
            network_type,
            version,
            deadline,
            max_fee,
            signature,
            signer,
            transaction_info,
        )
        self._set('remote_account_key', remote_account_key)
        self._set('link_action', link_action)

    @classmethod
    def create(
        cls,
        deadline: Deadline,
        remote_account_key: str,
        link_action: LinkAction,
        network_type: NetworkType,
        max_fee: int = 0,
    ):
        """
        Create new account link transaction.

        :param deadline: Deadline to include transaction.
        :param remote_account_key: Public key of the remote account.
        :param link_action: Account link action.
        :param network_type: Network type.
        :param max_fee: (Optional) Max fee defined by sender.
        """
        return cls(
            network_type,
            TransactionVersion.LINK_ACCOUNT,
            deadline,
            remote_account_key,
            link_action,
            max_fee,
        )

    # CATBUFFER

    def catbuffer_size_specific(self) -> int:
        key_size = util.U8_BYTES * 32
        action_size = util.U8_BYTES
        return key_size + action_size

    def to_catbuffer_specific(
        self,
        network_type: NetworkType,
    ) -> bytes:
        """Export account link-specific data to catbuffer."""

        # uint8_t[32] remote_account_key
        # uint8_t link_action
        remote_account_key = util.unhexlify(self.remote_account_key)
        link_action = self.link_action.to_catbuffer(network_type)
        return remote_account_key + link_action

    def load_catbuffer_specific(
        self,
        data: bytes,
        network_type: NetworkType,
    ) -> bytes:
        """Load account link-specific data data from catbuffer."""

        # uint8_t[32] remote_account_key
        # uint8_t link_action
        remote_account_key = util.hexlify(data[:32])
        link_action = LinkAction.create_from_catbuffer(data[32:33], network_type)
        data = data[33:]

        self._set('remote_account_key', remote_account_key)
        self._set('link_action', link_action)

        return data

    # DTO

    @classmethod
    def validate_dto_specific(cls, data: dict) -> bool:
        required_keys = {'remoteAccountKey', 'action'}
        return cls.validate_dto_required(data, required_keys)

    def to_dto_specific(
        self,
        network_type: NetworkType,
    ) -> dict:
        return {
            'remoteAccountKey': self.remote_account_key,
            'action': self.link_action.to_dto(network_type),
        }

    def load_dto_specific(
        self,
        data: dict,
        network_type: NetworkType,
    ) -> None:
        remote_account_key = data['remoteAccountKey']
        link_action = LinkAction.create_from_dto(data['action'])
        self._set('remote_account_key', remote_account_key)
        self._set('link_action', link_action)


@register_transaction('LINK_ACCOUNT')
class AccountLinkInnerTransaction(InnerTransaction, AccountLinkTransaction):
    """Embedded account link transaction."""

    __slots__ = ()
