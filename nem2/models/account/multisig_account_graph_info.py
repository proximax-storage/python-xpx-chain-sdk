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

from collections import abc
import typing

from nem2 import util

if typing.TYPE_CHECKING:
    from .multisig_account_info import MultisigAccountInfo

GraphType = typing.MutableMapping[int, 'MultisigAccountInfo']


@util.inherit_doc
@util.dataclass(frozen=True, slots=False)
class MultisigAccountGraphInfo(abc.MutableMapping):
    """
    Graph info for multi-sig accounts.

    :param \*args: (optional) Positional arguments to initialize mapping.
    :param \**kwds: (optional) Keyword arguments to initialize mapping.
    """

    multisig_accounts: GraphType

    def __init__(self, *args, **kwds) -> None:
        super().__init__(dict(*args, **kwds))

    def __getitem__(self, key: int) -> 'MultisigAccountInfo':
        return self.multisig_accounts[key]

    def __setitem__(self, key: int, account: 'MultisigAccountInfo') -> None:
        self.multisig_accounts[key] = account

    def __delitem__(self, key: int) -> None:
        del self.multisig_accounts[key]

    def __iter__(self) -> typing.Iterator:
        return iter(self.multisig_accounts)

    def __len__(self) -> int:
        return len(self.multisig_accounts)
