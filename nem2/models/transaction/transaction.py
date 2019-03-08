"""
    transaction
    ===========

    Abstract base class for transactions.

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

import typing

from nem2 import util

if typing.TYPE_CHECKING:
    from .aggregate_transaction_info import AggregateTransactionInfo
    from .deadling import Deadline
    from .transaction_info import TransactionInfo
    from ..account.publicaccount import PublicAccount
    from ..blockchain.network_type import NetworkType


# TODO(ahuszagh) Model??
class Transaction(util.Dto):
    """Abstract transaction base class."""

    _type: int
    _network_type: 'NetworkType'
    _version: int
    _deadline: 'Deadline'
    _fee: int
    _signature: typing.Optional[str]
    _signer: typing.Optional['PublicAccount']
    _transaction_info: typing.Union['TransactionInfo', 'AggregateTransactionInfo']

    # TODO(ahuszagh) Finish the implementation...
    # __init__
    # signWith
    # buildTransaction
    # aggregateTransaction
    # toAggregate
    # isUnconfirmed
    # isConfirmed
    # hasMissingSignatures
    # isUnannounced
    # reapplyGiven

    # TODO(ahuszagh) Implement
    # from_dto
    # to_dto
