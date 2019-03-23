"""
    transaction_version
    ===================

    Enumerations for transaction versions.

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
import enum

from nem2 import util

__all__ = ['TransactionVersion']


@util.inherit_doc
class TransactionVersion(util.U8Mixin, enum.IntEnum):
    """Transaction version."""

    TRANSFER = 3
    REGISTER_NAMESPACE = 2
    MOSAIC_DEFINITION = 3
    MOSAIC_SUPPLY_CHANGE = 2
    MODIFY_MULTISIG_ACCOUNT = 3
    AGGREGATE_COMPLETE = 2
    AGGREGATE_BONDED = 2
    LOCK = 1
    SECRET_LOCK = 1
    SECRET_PROOF = 1
    ADDRESS_ALIAS = 1
    MOSAIC_ALIAS = 1

    def description(self) -> str:
        return DESCRIPTION[self]


DESCRIPTION = {
    TransactionVersion.LOCK: "Transaction version 1.",
    TransactionVersion.AGGREGATE_BONDED: "Transaction version 2.",
    TransactionVersion.TRANSFER: "Transaction version 3.",
}
