"""
    receipt
    ===========

    Abstract base class for transactions.

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
import bidict
import typing

from ..blockchain.network_type import OptionalNetworkType
from .format import DTOFormat
from .receipt_base import TypeMap, ReceiptBase
from ... import util

__all__ = ['Receipt']


@util.inherit_doc
class Receipt(ReceiptBase):
    """Abstract, non-embedded Receipt base class."""

    __slots__ = ()
    # Overridable classvars.
    TYPE_MAP: typing.ClassVar[TypeMap] = bidict.bidict()

    DTO: typing.ClassVar[DTOFormat] = DTOFormat(
        names={
            'type': 'type',
            'version': 'version',
        },
    )

    # DTO

    @classmethod
    def validate_dto_shared(cls, data: dict) -> bool:
        required_keys = {
            'version',
            'type',
        }
        return cls.validate_dto_required(data, required_keys)

    def to_dto_shared(
        self,
        network_type: OptionalNetworkType
    ) -> dict:
        # Shared data and callbacks.
        data: dict = {}
        cb = lambda k, v: self.DTO.save(k, data, v)
        cb_get = lambda k: cb(k, getattr(self, k))

        # Save shared data.
        # Do not export `network_type`, already exported
        # with version.
        cb_get('version')
        cb_get('type')

        return data

    def load_dto_shared(
        self,
        data: dict,
        network_type: OptionalNetworkType,
    ) -> None:
        # Shared data and callbacks.
        cb = lambda k: self.DTO.load(k, data)
        cb_set = lambda k: self._set(k, cb(k))

        # Load shared data.
        cb_set('version')
        cb_set('type')
