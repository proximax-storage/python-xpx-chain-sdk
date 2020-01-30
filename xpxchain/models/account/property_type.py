"""
    property_type
    =============

    Types of properties for an account.

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

__all__ = ['PropertyType']


@util.inherit_doc
class PropertyType(util.U8Mixin, util.EnumMixin, enum.IntEnum):
    """Identifier for an account property type."""

    ALLOW_ADDRESS       = 0x01  # noqa: E221
    ALLOW_MOSAIC        = 0x02  # noqa: E221
    ALLOW_TRANSACTION   = 0x04  # noqa: E221
    SENTINEL            = 0x05  # noqa: E221
    BLOCK_ADDRESS       = 0x81  # noqa: E221
    BLOCK_MOSAIC        = 0x82  # noqa: E221
    BLOCK_TRANSACTION   = 0x84  # noqa: E221

    def description(self) -> str:
        return DESCRIPTION[self]


DESCRIPTION = {
    PropertyType.ALLOW_ADDRESS: "The property type is an address.",
    PropertyType.ALLOW_MOSAIC: "The property type is a mosaic id.",
    PropertyType.ALLOW_TRANSACTION: "The property type is a transaction type.",
    PropertyType.SENTINEL: "Property type sentinel.",
    PropertyType.BLOCK_ADDRESS: "The property type is a blocking address operation.",
    PropertyType.BLOCK_MOSAIC: "The property type is a blocking mosaic id operation.",
    PropertyType.BLOCK_TRANSACTION: "The property type is a blocking transaction type operation.",  # noqa: E501
}
