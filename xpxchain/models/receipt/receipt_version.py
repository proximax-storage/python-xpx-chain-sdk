"""
    receipt_version
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

from ... import util

__all__ = ['ReceiptVersion']


@util.inherit_doc
class ReceiptVersion(util.U8Mixin, enum.IntEnum):
    """Receipt version."""

    HARVEST_FEE = 1
    INFALTION = 1
    ADDRESS_ALIAS_RESOLUTION = 1
    MOSAIC_ALIAS_RESOLUTION = 1
    TRANSACTION_GROUP = 1
    MOSAIC_EXPIRED = 1
    MOSAIC_LEVY = 1
    MOSAIC_RENTAL_FEE = 1
    NAMESPACE_EXPIRED = 1
    NAMESPACE_RENTAL_FEE = 1
    LOCKHASH_COMPLETED = 1
    LOCKHASH_EXPIRED = 1
    LOCKSECRET_COMPLETED = 1
    LOCKSECRET_EXPIRED = 1
    LOCKHASH_CREATED = 1
    LOCKSECRET_CREATED = 1

    def description(self) -> str:
        return DESCRIPTION[self]


DESCRIPTION = {
    ReceiptVersion(1): "Receipt version 1.",
}
