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

from collections.abc import MutableMapping
from typing import Iterable, Mapping

from nem2 import util
from .multisig_account_info import MultisigAccountInfo

GraphType = Mapping[int, MultisigAccountInfo]
GraphIterType = Iterable[GraphType]


class MultisigAccountGraphInfo(MutableMapping):
    """Graph info for multi-sig accounts."""

    def __init__(self, *args, **kwds):
        self._multisig_accounts = dict(*args, **kwds)

    @property
    def multisig_accounts(self) -> GraphType:
        return self._multisig_accounts

    multisigAccounts = util.undoc(multisig_accounts)

    def __getitem__(self, key: int) -> MultisigAccountInfo:
        return self._multisig_accounts[key]

    def __setitem__(self, key: int, account: MultisigAccountInfo):
        self._multisig_accounts[key] = account

    def __delitem__(self, key: int):
        del self._multisig_accounts[key]

    def __iter__(self) -> GraphIterType:
        return iter(self._multisig_accounts)

    def __len__(self) -> int:
        return len(self._multisig_accounts)
