"""
    reactive
    ========

    Helpers to simplify interfacing with RxPy.

    If `RxPy` is installed, `@observable` makes `async def` functions
    return an `rx.Observable`. Otherwise, `@observable` does nothing.

    Example:
        .. code-block:: python

           >>> from nem2.util import observable
           >>> import asyncio
           >>> loop = asyncio.get_event_loop()
           >>> @observable
           ... async def f():
           ...     print("Called f()")
           ...     return 3
           >>> source = f()
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

try:
    import rx
    HAS_REACTIVE = True
except ImportError:
    HAS_REACTIVE = False

import functools
import inspect

from .asynchronous import *


if HAS_REACTIVE:
    # RxPy available.

    def wrap(coro, loop=None):
        """Wrap coroutine to generate rx.Observable."""

        loop = get_event_loop(loop)
        task = loop.create_task(coro)
        return rx.Observable.from_future(task)

else:
    # RxPy not available, use asyncio for everything.

    def wrap(coro, loop=None):
        """Wrap coroutine to generate awaitable object."""

        if loop is None:
            return coro
        return loop.create_task(coro)


def wrap_loop(loop=None):
    """Wrap event loop to generate awaitable object."""

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwds):
            return wrap(f(*args, **kwds), loop)
        return wrapper
    return decorator


def wrap_method(f):
    """Wrap a method to generate awaitable object."""

    @functools.wraps(f)
    def wrapper(self, *args, **kwds):
        loop = getattr(self, "loop", None)
        return wrap(f(self, *args, **kwds), loop)
    return wrapper


def wrap_function(f):
    """Wrap a function to generate awaitable object."""

    @functools.wraps(f)
    def wrapper(*args, **kwds):
        return wrap(f(*args, **kwds), None)
    return wrapper


def observable(value):
    """Wrap an `async def` function into an `Observable`."""

    if value is None or isinstance(value, LoopType):
        return wrap_loop(value)
    elif callable(value):
        # Have a callable function, we need to determine if this
        # might have a custom event loop bound to the class.
        args = inspect.getfullargspec(value).args
        if args and args[0] == 'self':
            return wrap_method(value)
        else:
            return wrap_function(value)
    else:
        raise TypeError("Observable must be created from event loop or asynchronous function.")
