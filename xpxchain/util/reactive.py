"""
    reactive
    ========

    Helpers to simplify interfacing with RxPy.

    If `RxPy` is installed, `@observable` makes `async def` functions
    return an `rx.Observable`. Otherwise, `@observable` does nothing.

    Example:
        .. code-block:: python

           >>> from xpxchain.util import observable
           >>> import asyncio
           >>> loop = asyncio.get_event_loop()
           >>> @observable
           ... async def f():
           ...     print("Called f()")
           ...     return 3
           >>> source = f().to_observable()
           >>> source.subscribe(lambda value: print("Received {0}".format(value)))
           >>> loop.run_until_complete(source)
           Called f()
           Received 3
           3

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
import functools
import inspect

__all__ = ['observable']

try:            # noqa: C901
    # Have RxPy installed.
    from . import rx

    def observable_class(cls):
        """Decorate class so it supports a `to_observable` method."""

        has_aiter = hasattr(cls, '__aiter__') or hasattr(cls, '__anext__')
        has_await = hasattr(cls, '__await__')
        # Only our Observables should provide both, since they're
        # a blanket class. Disable this in release builds.
        assert not (has_aiter and has_await)

        # determine the proper mixin
        if has_aiter:
            mixin = rx.AsyncGeneratorMixin
        else:
            mixin = rx.CoroutineMixin

        class ToObservable(cls, mixin):
            pass

        ToObservable.__doc__ = cls.__doc__
        ToObservable.__module__ = cls.__module__
        ToObservable.__name__ = cls.__name__
        ToObservable.__qualname__ = cls.__qualname__

        return ToObservable

    def observable_routine(f):
        """Decorate async function so the result supports `to_observable`."""

        # Need to get the proper adapter.
        if inspect.isasyncgenfunction(f):
            adapter = rx.AsyncGenerator
        else:
            adapter = rx.Coroutine

        # Wrap methods and free-functions separately. If the first
        # argument is self, we want to get an event loop, if bound,
        # from the class.
        args = inspect.getfullargspec(f).args
        if args and args[0] == 'self':
            # Method
            @functools.wraps(f)
            def wrapper(self, *args, **kwds):
                loop = getattr(self, "loop", None)
                return adapter(f(self, *args, **kwds), loop=loop)
        else:
            # Function
            @functools.wraps(f)
            def wrapper(*args, **kwds):
                return adapter(f(*args, **kwds))

        return wrapper

    def observable(value):
        """Decorates a function or class to allow `to_observable`."""

        if inspect.isclass(value):
            return observable_class(value)
        elif inspect.isroutine(value):
            return observable_routine(value)
        raise TypeError("Observable must be created from class or routine.")

except ImportError:
    # RxPy is not installed.

    def observable(value):
        """Dummy decorator that returns whatever was passed to it."""
        return value
