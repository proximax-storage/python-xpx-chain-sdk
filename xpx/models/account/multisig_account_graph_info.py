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
from collections import abc
import copy
import typing

from .multisig_account_info import MultisigAccountInfo
from ..blockchain.network_type import OptionalNetworkType
from ... import util

__all__ = ['MultisigAccountGraphInfo']

Key = int
Value = typing.Sequence[MultisigAccountInfo]
OptionalValue = typing.Optional[Value]
DictType = typing.Dict[int, Value]
TupleType = typing.Sequence[Value]
DictFactory = typing.Callable[..., DictType]
TupleFactory = typing.Callable[..., TupleType]


@util.inherit_doc
class MultisigAccountGraphInfo(util.DTO, abc.Mapping):
    """
    Graph info for multi-sig accounts.

    :param \\*args: (Optional) positional arguments to initialize mapping.


    DTO Format:
        .. code-block:: yaml

            MultisigAccountGraphInfoLevelDTO:
                level: integer
                multisigEntries: MultisigAccountInfoDTO[]

            MultisigAccountGraphInfoDTO: MultisigAccountGraphInfoLevelDTO[]
    """

    _multisig_accounts: DictType
    __slots__ = ('_multisig_accounts',)

    # DATACLASS-LIKE

    def __init__(self, *args) -> None:
        self._multisig_accounts = dict(*args)

    def __repr__(self) -> str:
        return f'MultisigAccountGraphInfo({self._multisig_accounts})'

    def __eq__(self, other) -> bool:
        if not isinstance(other, MultisigAccountGraphInfo):
            return False
        return self._multisig_accounts == other._multisig_accounts

    def __hash__(self) -> int:
        return hash(tuple(self.items()))

    def __copy__(self) -> MultisigAccountGraphInfo:
        return self.copy()

    def __deepcopy__(self, memo=None) -> MultisigAccountGraphInfo:
        data = copy.deepcopy(self._multisig_accounts, memo)
        return MultisigAccountGraphInfo(data)

    def asdict(
        self,
        recurse: bool = True,
        dict_factory: DictFactory = dict,
    ) -> DictType:
        if not recurse:
            return dict_factory(self.items())

        asdict = lambda x: x.asdict(recurse=True, dict_factory=dict_factory)
        return dict_factory([(k, [asdict(i) for i in v]) for k, v in self.items()])

    def astuple(
        self,
        recurse: bool = True,
        tuple_factory: TupleFactory = tuple,
    ) -> TupleType:
        if not recurse:
            return tuple_factory(self.values())

        astuple = lambda x: x.astuple(recurse=True, tuple_factory=tuple_factory)
        return tuple_factory([[astuple(j) for j in i] for i in self.values()])

    # MAPPING

    def __contains__(self, key: Key) -> bool:       # type: ignore
        return key in self._multisig_accounts

    def __getitem__(self, key: Key) -> Value:       # type: ignore
        return self._multisig_accounts[key]

    def __iter__(self) -> typing.Iterator[Key]:     # type: ignore
        return iter(self._multisig_accounts)

    def __len__(self) -> int:                       # type: ignore
        return len(self._multisig_accounts)

    def copy(self) -> MultisigAccountGraphInfo:
        return MultisigAccountGraphInfo(self._multisig_accounts)

    def get(                                        # type: ignore
        self,
        key: Key,
        default: OptionalValue = None
    ) -> OptionalValue:
        return self._multisig_accounts.get(key, default)

    def items(self) -> typing.ItemsView[Key, Value]:
        return self._multisig_accounts.items()

    def keys(self) -> typing.KeysView[Key]:
        return self._multisig_accounts.keys()

    def values(self) -> typing.ValuesView[Value]:
        return self._multisig_accounts.values()

    @classmethod
    def validate_dto(cls, data: list) -> bool:
        """Validate the data-transfer object."""

        required_keys = {'level', 'multisigEntries'}
        return all((
            cls.validate_dto_required(entry, required_keys)
            and cls.validate_dto_all(entry, required_keys)
        ) for entry in data)

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
    def create_from_dto(
        cls,
        data: list,
        network_type: OptionalNetworkType = None,
    ):
        if not cls.validate_dto(data):
            raise ValueError('Invalid data-transfer object.')

        graph = {}
        for item in data:
            key = item['level']
            entries = item['multisigEntries']
            value = MultisigAccountInfo.sequence_from_dto(entries, network_type)
            graph[key] = value
        return cls(graph)
