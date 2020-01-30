"""
    async_generator
    ===============

    Wrapper for asynchronous generators.

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
import rx


class AsyncGenerator:
    """Asynchronous generator wrapper type."""

    def __init__(self, value, loop=None):
        self._value = value
        self._loop = loop
        self._observable = None
        # In case we get an asynchronous iterable, which does not
        # support __anext__. If we get an asynchronous iterator,
        # or an asychronous generator iterator, use.
        if not hasattr(self._value, '__anext__'):
            self._value = self._value.__aiter__()

    async def aclose(self) -> None:
        """Raise GeneratorExit inside generator."""
        await self._value.aclose()

    async def asend(self, arg):
        """Send `arg` into generator."""
        return await self._value.asend(arg)

    async def throw(self, exception_type, *args):
        """Raise exception in generator."""
        return await self._value.athrow(exception_type, *args)

    def to_observable(self):
        """Export awaitable object to Observable."""
        if self._observable is None:
            self._observable = rx.Observable.from_async_iterable(
                self._value,
                loop=self._loop
            )
        return self._observable

    @property
    def ag_await(self):
        return self._value.ag_await

    @property
    def ag_code(self):
        return self._value.ag_code

    @property
    def ag_frame(self):
        return self._value.ag_frame

    @property
    def ag_running(self):
        return self._value.ag_running

    def __aiter__(self):
        return self

    def __anext__(self):
        if self._observable is None:
            return self._value.__anext__()
        return self._observable.__anext__()


class AsyncGeneratorMixin(typing.AsyncIterable):
    """Mixin for async iterable classes to support `to_observable`."""

    def to_observable(self):
        """Export async iterable object to Observable."""
        loop = getattr(self, 'loop', None)
        return rx.Observable.from_async_iterable(
            self.__aiter__(),
            loop=loop
        )
