"""
    coroutine
    =========

    Wrapper for asynchronous coroutine.

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


class Coroutine:
    """Coroutine wrapper type."""

    def __init__(self, value, loop=None):
        self._value = value
        self._loop = loop
        self._observable = None

    def close(self) -> None:
        """Raise GeneratorExit inside coroutine."""
        self._value.close()

    def send(self, arg):
        """Send `arg` into coroutine."""
        return self._value.send(arg)

    def throw(self, exception_type, *args):
        """Raise exception in coroutine."""
        return self._value.throw(exception_type, *args)

    def to_observable(self):
        """Export awaitable object to Observable."""
        if self._observable is None:
            self._observable = rx.Observable.from_coroutine(
                self._value,
                loop=self._loop
            )
        return self._observable

    @property
    def cr_await(self):
        return self._value.cr_await

    @property
    def cr_code(self):
        return self._value.cr_code

    @property
    def cr_frame(self):
        return self._value.cr_frame

    @property
    def cr_running(self):
        return self._value.cr_running

    def __await__(self):
        if self._observable is None:
            return self._value.__await__()
        return self._observable.__await__()


class CoroutineMixin(typing.Awaitable):
    """Mixin for awaitable classes to support `to_observable`."""

    def to_observable(self):
        """Export awaitable object to Observable."""
        loop = getattr(self, 'loop', None)
        return rx.Observable.from_coroutine(
            self.__aiter__(),
            loop=loop
        )
