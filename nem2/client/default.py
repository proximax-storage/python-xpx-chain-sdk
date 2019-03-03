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

import asyncio
import atexit
import aiohttp
import inspect
import requests

from nem2 import util
from . import async_http
from . import host
from . import http

# SYNCHRONOUS

SYNC_SESSION = requests.Session()
atexit.register(SYNC_SESSION.close)

Sync = http.factory(lambda endpoint: host.Host(SYNC_SESSION, endpoint))
Http = util.defactorize(Sync[0])
AccountHttp = util.defactorize(Sync[1])
BlockchainHttp = util.defactorize(Sync[2])

# ASYNCHRONOUS

ASYNC_SESSION = aiohttp.ClientSession()

@atexit.register
def close_session():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ASYNC_SESSION.close())

Async = async_http.factory(lambda endpoint: host.Host(ASYNC_SESSION, endpoint))
AsyncHttp = util.defactorize(Async[0])
AsyncAccountHttp = util.defactorize(Async[1])
AsyncBlockchainHttp = util.defactorize(Async[2])
