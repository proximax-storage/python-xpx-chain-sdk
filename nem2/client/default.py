"""
    default
    =======

    Synchronous and asynchronous NIS client using the default backend.

    The core HTTP client shares a global session, to share a connection
    pool to speed up requests.

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

__all__ = [
    'Http',
    'AccountHttp',
    'AsyncHttp',
    'AsyncAccountHttp',
]

import asyncio
import atexit
import aiohttp
import inspect
import requests
from . import async_http, http
from .host import Host


def qualname(cls, func):
    """Get qualified name from function."""

    return '{}.{}'.format(cls.__name__, func.__name__)


def patch_classmethod(cls, meth):
    """Patch classmethod qualified name."""

    patch_function(cls, meth.__func__)


def patch_function(cls, func):
    """Patch function qualified name."""

    func.__module__ = __name__
    func.__qualname__ = qualname(cls, func)
    # Recursively patch wrapped functions.
    wrapped = getattr(func, '__wrapped__', None)
    if wrapped is not None:
        patch_function(cls, wrapped)


def patch_property(cls, prop):
    """Patch property qualified name."""

    if prop.fget is not None:
        patch_function(cls, prop.fget)
    if prop.fset is not None:
        patch_function(cls, prop.fset)
    if prop.fdel is not None:
        patch_function(cls, prop.fdel)


def patch(cls):
    """
    Patch a class to modify the qualified name and module.

    This is mostly for Sphinx compatibility, to avoid
    treating the class like a local variable in class factories.

    This only does a 1-depth pass, and ignores all special and private
    members.
    """

    cls.__module__ = __name__
    cls.__qualname__ = cls.__name__
    members = inspect.getmembers(cls)
    for key, inner in members:
        if not key.startswith('_'):
            # Ignore private and special members
            if inspect.ismethod(inner):
                # Classmethods only
                patch_classmethod(cls, inner)
            elif inspect.isfunction(inner):
                patch_function(cls, inner)
            elif isinstance(inner, property):
                # Properties only
                patch_property(cls, inner)
            else:
                # Error so we can handle other class types.
                raise NotImplementedError

    return cls

# SYNCHRONOUS

SYNC_SESSION = requests.Session()
atexit.register(SYNC_SESSION.close)

Sync = http.factory(lambda endpoint: Host(SYNC_SESSION, endpoint))
Http = patch(Sync[0])
AccountHttp = patch(Sync[1])

# ASYNCHRONOUS

ASYNC_SESSION = aiohttp.ClientSession()

@atexit.register
def close_session():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ASYNC_SESSION.close())

Async = async_http.factory(lambda endpoint: Host(ASYNC_SESSION, endpoint))
AsyncHttp = patch(Async[0])
AsyncAccountHttp = patch(Async[1])
