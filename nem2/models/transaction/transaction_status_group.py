"""
    transaction_status_group
    ========================

    Enumerated groups for a transaction status.

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

from ... import util

__all__ = ['TransactionStatusGroup']


@util.inherit_doc
class TransactionStatusGroup(util.EnumMixin, str, enum.Enum):
    """Enumerated groups  for a transaction status."""

    UNKNOWN = "unknown"
    FAILED = "failed"
    UNCONFIRMED = "unconfirmed"
    CONFIRMED = "confirmed"

    def description(self) -> str:
        return DESCRIPTION[self]


DESCRIPTION = {
    TransactionStatusGroup.UNKNOWN: "Unknown status.",
    TransactionStatusGroup.FAILED: "Transaction failed.",
    TransactionStatusGroup.UNCONFIRMED: "Transaction not yet confirmed.",
    TransactionStatusGroup.CONFIRMED: "Transaction confirmed.",
}
