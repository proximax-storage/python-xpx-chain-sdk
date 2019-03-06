"""
    reactive
    ========

    Helpers to simplify interfacing with RxPy.

    If `RxPy` is installed, `@observable` makes `async def` functions
    return an `rx.Observable`. Otherwise, `@observable` does nothing.

    Example
    -------

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
    import asyncio
    import rx
    HAS_REACTIVE = True
except ImportError:
    HAS_REACTIVE = False

import functools
import typing


def observable(f: typing.Callable) -> typing.Callable:
    """Wrap an `async def` function into an `Observable`."""

    if not HAS_REACTIVE:
        # Return the `async def` function if RxPy is not available.
        return f

    loop = asyncio.get_event_loop()

    @functools.wraps(f)
    def wrapper(*args, **kwds) -> rx.Observable:
        return rx.Observable.from_future(loop.create_task(f(*args, **kwds)))

    return wrapper
