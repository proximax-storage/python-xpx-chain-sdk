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

def sync_callback(endpoint: str) -> 'Host':
    """Callback for synchronous HTTP client."""
    return host.Host(SYNC_SESSION, endpoint)

(
    Http,
    AccountHttp,
    BlockchainHttp,
    MosaicHttp,
    NamespaceHttp,
    NetworkHttp,
    TransactionHttp,
) = map(util.defactorize, http.factory(sync_callback))

# ASYNCHRONOUS

ASYNC_SESSION = aiohttp.ClientSession()

@atexit.register
def close_sessions() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ASYNC_SESSION.close())

def async_callback(endpoint: str, loop: util.OptionalLoopType = None) -> 'Host':
    """Callback for asynchronous HTTP client."""

    if loop is None:
        return host.AsyncHost(ASYNC_SESSION, endpoint)

    # Create a managed session with an internal loop
    session = aiohttp.ClientSession(loop=loop)
    return host.AsyncHost(session, endpoint, loop=loop)

(
    AsyncHttp,
    AsyncAccountHttp,
    AsyncBlockchainHttp,
    AsyncMosaicHttp,
    AsyncNamespaceHttp,
    AsyncNetworkHttp,
    AsyncTransactionHttp,
) = map(util.defactorize, async_http.factory(async_callback))
