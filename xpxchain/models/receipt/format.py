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

from .receipt_type import ReceiptType
from .receipt_version import ReceiptVersion
from ..blockchain.network_type import NetworkType
from ... import util

import logging
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class FormatBase(util.Object):
    """Utilities to simplify loading and saving to interchange formats."""

    def save(self, key, data, value) -> None:
    #def save(self, key, data, value, network_type) -> None:
        """Save value to interchange format by key."""
        raise util.AbstractMethodError

    def load(self, key, data):
    #def load(self, key, data, network_type):
        """Load value from interchange format by key."""
        raise util.AbstractMethodError

    def load_size(self, data):
        """Load transaction size."""
        return self.load('size', data)
        #return self.load('size', data, None)

    def load_type(self, data):
        """Load transaction type."""
        #return self.load('version', data, None)
        return self.load('version', data)

    #def load_network_type(self, data):
    #    """Load network type."""
    #    return self.load('network_type', data, None)

    def find_receipt(self, type_map, data):
        """Find derived receipt class via the receipt type."""
        return type_map[self.load_type(data)]



# DTO HELPERS
@util.dataclass(frozen=True)
class DTOFormat(FormatBase):
    """Utilities to simplify loading and saving to catbuffer."""

    names: typing.Dict[str, str]

    def save(self, key, data, value) -> None:
    #def save(self, key, data, value, network_type) -> None:
        name = self.names[key]
        cb = SAVE_DTO[key]
        if value is not None:
            data[name] = cb(value)
            #data[name] = cb(value, network_type)

    def load(self, key, data):
    #def load(self, key, data, network_type):
        name = self.names[key]
        cb = LOAD_DTO[key]
        value = data.get(name)
        if value is not None:
            return cb(value)
            #return cb(value, network_type)


#def save_version_dto(version, network_type):
#    return version | (int(network_type) << 8)
def save_version_dto(version):
    return version


SAVE_DTO = {
    'version': save_version_dto,
    'type': lambda x, n: x.to_dto(n),
}


#def load_version_dto(data, network_type):
#    return data & 0xFF
def load_version_dto(data):
    return data


#def load_network_type_dto(data, network_type):
#    return NetworkType((data >> 24) & 0x000000ff)


LOAD_DTO = {
    'version': load_version_dto,
    #'network_type': load_network_type_dto,
    'type': ReceiptType.create_from_dto,
}
