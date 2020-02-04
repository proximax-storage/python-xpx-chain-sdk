"""
    format
    ======

    Class-bound helpers to simplify conversion between interchange formats.

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

from ... import util


class FormatBase(util.Object):
    """Utilities to simplify loading and saving to interchange formats."""

    def save(self, key, data, value) -> None:
        """Save value to interchange format by key."""
        raise util.AbstractMethodError

    def load(self, key, data):
        """Load value from interchange format by key."""
        raise util.AbstractMethodError

    def load_type(self, data):
        """Load transaction type."""
        return self.load('type', data)

    def find_receipt(self, type_map, data):
        """Find derived receipt class via the receipt type."""
        return type_map[self.load_type(data)]


# DTO HELPERS
@util.dataclass(frozen=True)
class DTOFormat(FormatBase):
    """Utilities to simplify loading and saving to catbuffer."""

    names: typing.Dict[str, str]

    def save(self, key, data, value) -> None:
        name = self.names[key]
        cb = SAVE_DTO[key]
        if value is not None:
            data[name] = cb(value)

    def load(self, key, data):
        name = self.names[key]
        cb = LOAD_DTO[key]
        value = data.get(name)
        if value is not None:
            return cb(value)


def save_version_dto(version):
    return version


def save_type_dto(data):
    return data


def load_version_dto(version):
    return version


def load_type_dto(data):
    return data


SAVE_DTO = {
    'version': save_version_dto,
    'type': save_type_dto,
}

LOAD_DTO = {
    'version': load_version_dto,
    'type': load_type_dto,
}
