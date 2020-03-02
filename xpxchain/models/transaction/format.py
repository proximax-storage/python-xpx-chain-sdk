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

from .aggregate_transaction_info import AggregateTransactionInfo
from .deadline import Deadline
from .transaction_info import TransactionInfo
from .transaction_type import TransactionType
from .transaction_version import TransactionVersion
from ..account.public_account import PublicAccount
from ..blockchain.network_type import NetworkType
from ... import util


class FormatBase(util.Object):
    """Utilities to simplify loading and saving to interchange formats."""

    def save(self, key, data, value, network_type) -> None:
        """Save value to interchange format by key."""
        raise util.AbstractMethodError

    def load(self, key, data, network_type):
        """Load value from interchange format by key."""
        raise util.AbstractMethodError

    def load_size(self, data):
        """Load transaction size."""
        return self.load('size', data, None)

    def load_type(self, data):
        """Load transaction type."""
        return self.load('type', data, None)

    def load_network_type(self, data):
        """Load network type."""
        return self.load('network_type', data, None)

    def find_transaction(self, type_map, data):
        """Find derived transaction class via the transaction type."""
        return type_map[self.load_type(data)]


@util.dataclass(frozen=True)
class CatbufferFormat(FormatBase):
    """Utilities to simplify loading and saving to catbuffer."""

    slices: typing.Dict[str, slice]
    size_shared: int

    def save(self, key, data, value, network_type) -> None:
        slc = self.slices[key]
        cb = SAVE_CATBUFFER[key]
        data[slc] = cb(value, network_type)

    def load(self, key, data, network_type):
        slc = self.slices[key]
        cb = LOAD_CATBUFFER[key]
        return cb(data[slc], network_type)


@util.dataclass(frozen=True)
class DTOFormat(FormatBase):
    """Utilities to simplify loading and saving to catbuffer."""

    names: typing.Dict[str, str]

    def save(self, key, data, value, network_type) -> None:
        name = self.names[key]
        cb = SAVE_DTO[key]
        if key != 'transaction_info':
            data = data.setdefault('transaction', {})
        if value is not None:
            data[name] = cb(value, network_type)

    def load(self, key, data, network_type):
        name = self.names[key]
        cb = LOAD_DTO[key]
        if key != 'transaction_info':
            data = data['transaction']
        value = data.get(name)
        if value is not None:
            return cb(value, network_type)


# CATBUFFER HELPERS


def save_signature_catbuffer(signature, network_type):
    if signature is None:
        return bytes(64)
    return util.unhexlify(signature)


def save_signer_catbuffer(signer, network_type):
    if signer is None:
        return bytes(32)
    return util.unhexlify(signer.public_key)


SAVE_CATBUFFER = {
    'size': lambda x, n: util.u32_to_catbuffer(x),
    'signature': save_signature_catbuffer,
    'signer': save_signer_catbuffer,
    'version': lambda x, n: x.to_catbuffer(n),
    'network_type': lambda x, n: x.to_catbuffer(n),
    'type': lambda x, n: x.to_catbuffer(n),
    'max_fee': lambda x, n: util.u64_to_catbuffer(x),
    'deadline': lambda x, n: util.u64_to_catbuffer(x.to_timestamp()),
}


def load_signature_catbuffer(data, network_type):
    if data == bytes(64):
        return None
    return util.hexlify(data)


def load_signer_catbuffer(data, network_type):
    if data == bytes(32):
        return None
    return PublicAccount.create_from_public_key(data, network_type)


LOAD_CATBUFFER = {
    'size': lambda x, n: util.u32_from_catbuffer(x),
    'signature': load_signature_catbuffer,
    'signer': load_signer_catbuffer,
    'version': TransactionVersion.create_from_catbuffer,
    'network_type': NetworkType.create_from_catbuffer,
    'type': TransactionType.create_from_catbuffer,
    'max_fee': lambda x, n: util.u64_from_catbuffer(x),
    'deadline': lambda x, n: Deadline.create_from_timestamp(util.u64_from_catbuffer(x)),
}


# DTO HELPERS


def save_signature_dto(signature, network_type):
    return signature


def save_signer_dto(signer, network_type):
    return signer.public_key


def save_version_dto(version, network_type):
    return version | (int(network_type) << 24)


def save_transaction_info_dto(transaction_info, network_type):
    return transaction_info.to_dto(network_type)


SAVE_DTO = {
    'signature': save_signature_dto,
    'signer': save_signer_dto,
    'version': save_version_dto,
    'type': lambda x, n: x.to_dto(n),
    'max_fee': lambda x, n: util.u64_to_dto(x),
    'deadline': lambda x, n: util.u64_to_dto(x.to_timestamp()),
    'transaction_info': save_transaction_info_dto,
}


def load_signature_dto(data, network_type):
    return data


def load_signer_dto(data, network_type):
    return PublicAccount.create_from_public_key(data, network_type)


def load_version_dto(data, network_type):
    # Version are 3B
    return data & 0xFFFFFF


def load_network_type_dto(data, network_type):
    return NetworkType((data >> 24) & 0x000000FF)


def load_transaction_info_dto(data, network_type):
    if 'hash' in data:
        return TransactionInfo.create_from_dto(data, network_type)
    return AggregateTransactionInfo.create_from_dto(data, network_type)


LOAD_DTO = {
    'signature': load_signature_dto,
    'signer': load_signer_dto,
    'version': load_version_dto,
    'network_type': load_network_type_dto,
    'type': TransactionType.create_from_dto,
    'max_fee': lambda x, n: util.u64_from_dto(x),
    'deadline': lambda x, n: Deadline.create_from_timestamp(util.u64_from_dto(x)),
    'transaction_info': load_transaction_info_dto,
}
