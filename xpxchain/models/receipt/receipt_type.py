"""
    receipt_type
    ================

    Enumerations for transaction types.

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

__all__ = ['ReceiptType']


@util.inherit_doc
class ReceiptType(util.U16Mixin, util.EnumMixin, enum.IntEnum):
    """Receipt type."""

    MOSAIC_RENTAL_FEE = 0x134D
    NAMESPACE_RENTAL_FEE = 0x124E
    VALIDATE_FEE = 0x2143
    MOSAIC_LEVY = 0x124D
    LOCKHASH_COMPLETED = 0x2248
    LOCKHASH_EXPIRED = 0x2348
    LOCKSECRET_COMPLETED = 0x2252
    LOCKSECRET_EXPIRED = 0x2352
    LOCKHASH_CREATED = 0x3148
    LOCKSECRET_CREATED = 0x3152
    MOSAIC_EXPIRED = 0x414D
    NAMESPACE_EXPIRED = 0x414E
    INFLATION = 0x5143
    TRANSACTION_GROUP = 0xE134
    ADDRESS_ALIAS_RESOLUTION = 0xF143
    MOSAIC_ALIAS_RESOLUTION = 0xF243

    def description(self) -> str:
        return DESCRIPTION[self]


DESCRIPTION = {

    ReceiptType.MOSAIC_RENTAL_FEE: "Mosaic rental fee receipt type.",
    ReceiptType.NAMESPACE_RENTAL_FEE: "Namespace rental fee receipt type.",
    ReceiptType.VALIDATE_FEE: "Harvest fee receipt type.",
    ReceiptType.LOCKHASH_COMPLETED: "Lock hash completed receipt type.",
    ReceiptType.LOCKHASH_EXPIRED: "Lock hash expired receipt type.",
    ReceiptType.LOCKSECRET_COMPLETED: "Lock secret completed receipt type.",
    ReceiptType.LOCKSECRET_EXPIRED: "Lock secret expired receipt type.",
    ReceiptType.LOCKHASH_CREATED: "Lock hash created receipt type.",
    ReceiptType.LOCKSECRET_CREATED: "Lock secret created receipt type.",
    ReceiptType.MOSAIC_EXPIRED: "Mosaic expired receipt type.",
    ReceiptType.NAMESPACE_EXPIRED: "Namespace expired receipt type.",
    ReceiptType.INFLATION: "Inflation receipt type.",
    ReceiptType.TRANSACTION_GROUP: "Transaction group receipt type.",
    ReceiptType.ADDRESS_ALIAS_RESOLUTION: "Address alias resolution receipt type.",
    ReceiptType.MOSAIC_ALIAS_RESOLUTION: "Mosaic alias resolution receipt type.",

}
