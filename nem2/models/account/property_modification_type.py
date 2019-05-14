"""
    property_modification_type
    ==========================

    Types of property modifications for an account.

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

__all__ = ['PropertyModificationType']


@util.inherit_doc
class PropertyModificationType(util.U8Mixin, util.EnumMixin, enum.IntEnum):
    """Identifier for an account property modification type."""

    ADD     = 0x00  # noqa: E221
    REMOVE  = 0x01  # noqa: E221

    def description(self) -> str:
        return DESCRIPTION[self]


DESCRIPTION = {
    PropertyModificationType.ADD: "Add property to account.",
    PropertyModificationType.REMOVE: "Remove property from account.",
}
