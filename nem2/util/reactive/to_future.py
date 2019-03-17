"""
    to_future
    =========

    RxPy extension to convert an observable to a future-like object.

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
import asyncio
import rx
from rx.internal import extensionmethod


def to_future(self) -> asyncio.Future:
    """Convert observable to an awaitable object."""

    future: asyncio.Future = asyncio.Future()
    values = []

    def on_next(v):
        values.append(v)

    def on_error(ex):
        future.set_exception(ex)

    def on_completed():
        # Fixes a critical bug where if no value is assigned, the
        # observable will hang forever.
        v = values.pop() if values else None
        future.set_result(v)

    self.subscribe(on_next, on_error, on_completed)

    return future


def __await__(self):
    return to_future(self).__await__()


extensionmethod(rx.AnonymousObservable)(__await__)
extensionmethod(rx.Observable)(__await__)
