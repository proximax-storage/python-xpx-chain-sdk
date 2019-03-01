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
import requests
from . import async_http, http
from .host import Host

# SYNCHRONOUS

_SYNC_SESSION = requests.Session()
atexit.register(_SYNC_SESSION.close)

_Sync = http.factory(lambda endpoint: Host(_SYNC_SESSION, endpoint))
Http = _Sync[0]
AccountHttp = _Sync[1]

# ASYNCHRONOUS

_ASYNC_SESSION = aiohttp.ClientSession()

@atexit.register
def close_session():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_ASYNC_SESSION.close())

_Async = async_http.factory(lambda endpoint: Host(_ASYNC_SESSION, endpoint))
AsyncHttp = _Async[0]
AsyncAccountHttp = _Async[1]
