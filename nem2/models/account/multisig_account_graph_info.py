"""
    multisig_account_graph_info
    ===========================

    Mapping of account numbers and multisig accounts.

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

from .multisig_account_info import MultisigAccountInfo
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['MultisigAccountGraphInfo']

Key = int
Value = typing.Sequence[MultisigAccountInfo]
OptionalValue = typing.Optional[Value]
GraphType = typing.Dict[int, Value]


@util.inherit_doc
class MultisigAccountGraphInfo(util.DTO):
    """
    Graph info for multi-sig accounts.

    :param \\*args: (Optional) positional arguments to initialize mapping.
    :param \\**kwds: (Optional) keyword arguments to initialize mapping.
    """

    _multisig_accounts: GraphType

    def __init__(self, *args) -> None:
        self._multisig_accounts = dict(*args)

    @property
    def multisig_accounts(self) -> GraphType:
        return self._multisig_accounts

    def __contains__(self, key: Key) -> bool:
        return key in self.multisig_accounts

    def __getitem__(self, key: Key) -> Value:
        return self.multisig_accounts[key]

    def __setitem__(self, key: Key, accounts: Value) -> None:
        self.multisig_accounts[key] = accounts

    def __delitem__(self, key: Key) -> None:
        del self.multisig_accounts[key]

    def __iter__(self) -> typing.Iterator[Key]:
        return iter(self.multisig_accounts)

    def __len__(self) -> Key:
        return len(self.multisig_accounts)

    def clear(self) -> None:
        self.multisig_accounts.clear()

    def copy(self) -> MultisigAccountGraphInfo:
        return MultisigAccountGraphInfo(self.multisig_accounts)

    def get(self, key: Key, default: OptionalValue = None) -> OptionalValue:
        return self.multisig_accounts.get(key, default)

    def items(self) -> typing.ItemsView[Key, Value]:
        return self.multisig_accounts.items()

    def keys(self) -> typing.KeysView[Key]:
        return self.multisig_accounts.keys()

    def values(self) -> typing.ValuesView[Value]:
        return self.multisig_accounts.values()

    def pop(self, key: Key, *args: Value):
        return self.multisig_accounts.pop(key, *args)

    def popitem(self) -> typing.Tuple[Key, Value]:
        return self.multisig_accounts.popitem()

    def setdefault(self, key: Key, default: OptionalValue = None) -> OptionalValue:
        return self.multisig_accounts.setdefault(key, default)

    def update(self, *args, **kwds):
        return self.multisig_accounts.update(*args, **kwds)

    def to_dto(
        self,
        network_type: OptionalNetworkType = None,
    ) -> list:
        data = []
        for key, value in self.items():
            entries = MultisigAccountInfo.sequence_to_dto(value, network_type)
            data.append({'level': key, 'multisigEntries': entries})
        return data

    @classmethod
    def from_dto(
        cls,
        data: list,
        network_type: OptionalNetworkType = None,
    ):
        inst = cls()
        for item in data:
            key = item['level']
            entries = item['multisigEntries']
            value = MultisigAccountInfo.sequence_from_dto(entries, network_type)
            inst[key] = value
        return inst
