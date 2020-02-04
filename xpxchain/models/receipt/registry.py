"""
    registry
    ========

    Class decorators to simplify defining and registering transactions.
    These allow us to register classes via `TYPE_MAP` with a class
    decorator, simplifying the generation of new transactions.

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

from .receipt_type import ReceiptType


def register_receipt(name: str):
    """Register receipt by its type."""

    type = getattr(ReceiptType, name)

    def decorator(cls):
        cls.TYPE_MAP[type] = cls
        return cls

    return decorator
