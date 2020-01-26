"""
    metadata_type
    =================

    Enumerations for alias action types.

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

import enum
from ... import util

__all__ = ['MetadataType']


@util.inherit_doc
class MetadataType(util.U8Mixin, util.EnumMixin, enum.IntEnum):
    """Metadata type."""

    NONE = 0
    ADDRESS = 1
    MOSAIC = 2
    NAMESPACE = 3

    def description(self) -> str:
        return DESCRIPTION[self]


DESCRIPTION = {
    MetadataType.NONE: "None metadata type",
    MetadataType.ADDRESS: "Address metadata type",
    MetadataType.MOSAIC: "Mosaic metadata type",
    MetadataType.NAMESPACE: "Namespace metadata type",
}
