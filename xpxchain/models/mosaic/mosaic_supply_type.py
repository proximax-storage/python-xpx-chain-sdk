"""
    mosaic_supply_type
    ==================

    Constants for the mosaic supply type.

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

__all__ = ['MosaicSupplyType']


@util.inherit_doc
class MosaicSupplyType(util.U8Mixin, util.EnumMixin, enum.IntEnum):
    """Mosaic supply type."""

    DECREASE = 0
    INCREASE = 1

    def description(self) -> str:
        return DESCRIPTION[self]


DESCRIPTION = {
    MosaicSupplyType.DECREASE: "Decrease mosaic supply.",
    MosaicSupplyType.INCREASE: "Increase mosaic supply.",
}
