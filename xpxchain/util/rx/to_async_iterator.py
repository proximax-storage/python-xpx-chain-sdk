"""
    to_async_generator
    ==================

    RxPy extension to convert an observable to an async iterator.

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
import collections
import rx
from rx.internal import extensionmethod


class AsyncIterable:
    """Adapter class to convert an observable to an asynchronous iterator."""

    def __init__(self, observable: rx.Observable):
        self.observable = observable
        self.notifications: collections.deque = collections.deque()
        self.future: asyncio.Future = asyncio.Future()
        self.observable.materialize().subscribe(self.on_next)

    def __aiter__(self):
        return self

    async def __anext__(self):
        self.process()
        value = await self.future
        self.future = asyncio.Future()
        return value

    def process(self):
        if not self.notifications or self.future.done():
            return

        notification = self.notifications.popleft()
        if notification.kind == 'N':
            self.future.set_result(notification.value)
        elif notification.kind == 'E':
            self.future.set_exception(notification.exception)
        else:
            self.future.set_exception(StopAsyncIteration)

    def on_next(self, notification):
        self.notifications.append(notification)
        self.process()


def __aiter__(self):
    return self


async def __anext__(self):
    # Use a name that's unlikely to be ever touched.
    if not hasattr(self, '_xpxchain_async_iter'):
        self._xpxchain_async_iter = AsyncIterable(self)
    try:
        return await self._xpxchain_async_iter.__anext__()
    except StopAsyncIteration:
        self._xpxchain_async_iter = None
        raise


extensionmethod(rx.AnonymousObservable)(__aiter__)
extensionmethod(rx.Observable)(__aiter__)
extensionmethod(rx.AnonymousObservable)(__anext__)
extensionmethod(rx.Observable)(__anext__)
