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

from nem2 import util
from .multisig_account_info import MultisigAccountInfo

__all__ = ['MultisigAccountGraphInfo']

OptionalValue = typing.Optional[MultisigAccountInfo]
GraphType = typing.Dict[int, MultisigAccountInfo]


@util.inherit_doc
@util.dataclass(frozen=True, slots=False)
class MultisigAccountGraphInfo:
    """
    Graph info for multi-sig accounts.

    :param \\*args: (Optional) positional arguments to initialize mapping.
    :param \\**kwds: (Optional) keyword arguments to initialize mapping.
    """

    multisig_accounts: GraphType

    def __init__(self, *args, **kwds) -> None:
        self.multisig_accounts = dict(*args, **kwds)

    def __contains__(self, key: int) -> bool:
        return key in self.multisig_accounts

    def __getitem__(self, key: int) -> MultisigAccountInfo:
        return self.multisig_accounts[key]

    def __setitem__(self, key: int, account: MultisigAccountInfo) -> None:
        self.multisig_accounts[key] = account

    def __delitem__(self, key: int) -> None:
        del self.multisig_accounts[key]

    def __iter__(self) -> typing.Iterator[int]:
        return iter(self.multisig_accounts)

    def __len__(self) -> int:
        return len(self.multisig_accounts)

    def clear(self) -> None:
        self.multisig_accounts.clear()

    def copy(self) -> MultisigAccountGraphInfo:
        return MultisigAccountGraphInfo(self.multisig_accounts)

    def get(self, key: int, default: OptionalValue = None) -> OptionalValue:
        return self.multisig_accounts.get(key, default)

    def items(self) -> typing.ItemsView[int, MultisigAccountInfo]:
        return self.multisig_accounts.items()

    def keys(self) -> typing.KeysView[int]:
        return self.multisig_accounts.keys()

    def values(self) -> typing.ValuesView[MultisigAccountInfo]:
        return self.multisig_accounts.values()

    def pop(self, key: int, *args: MultisigAccountInfo):
        return self.multisig_accounts.pop(key, *args)

    def popitem(self) -> typing.Tuple[int, MultisigAccountInfo]:
        return self.multisig_accounts.popitem()

    def setdefault(self, key: int, default: OptionalValue = None) -> OptionalValue:
        return self.multisig_accounts.setdefault(key, default)

    def update(self, *args, **kwds):
        return self.multisig_accounts.update(*args, **kwds)
