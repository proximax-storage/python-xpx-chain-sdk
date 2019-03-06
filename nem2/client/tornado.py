"""
    tornado
    =======

    Synchronous and asynchronous NIS client using the tornado backend.

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

from tornado.httpclient import AsyncHTTPClient, HTTPClient, HTTPRequest
from tornado.httputil import url_concat, urlencode


def format_request(url, method, **kwds) -> 'HTTPRequest':
    """Format a request to form a valid HTTPRequest."""

    # TODO(ahuszagh) Only add to the URL for a get request...
    # TODO(ahuszagh) This is so annoying, so deal with it later.
    params = kwds.pop('params', None)
    if method == "GET":
        url = url_concat(url, params)
    elif method == "POST":
        # TODO(only if it's a mapping object...)
        body = urlencode(params)
    timeout = kwds.pop('timeout', None)
    # TODO(ahuszagh) Add more for other methods...

    return HTTPRequest(url, method=method, request_timeout=timeout)


class SyncClient:
    """Wrapper for tornado.httpclient.HTTPClient()."""

    def __init__(self) -> None:
        self._client = HTTPClient()

    def get(self, url, **kwds):
        raise NotImplementedError

    def post(self, url, **kwds):
        raise NotImplementedError


class AsyncClient:
    """Wrapper for tornado.httpclient.AsyncHTTPClient()."""

    def __init__(self) -> None:
        self._client = AsyncHTTPClient()

    def get(self, url, **kwds):
        raise NotImplementedError

    def post(self, url, **kwds):
        raise NotImplementedError


class SyncResponse:
    pass


class AsyncResponse:
    pass

# TODO(ahuszagh) Implement...
#import atexit
#from tornado.httpclient import AsyncHTTPClient, HTTPClient
#
#_HTTP_SESSION = HTTPClient()
#atexit.register(_HTTP_SESSION.close)
#
#_ASYNC_HTTP_SESSION = AsyncHTTPClient()
#atexit.register(_ASYNC_HTTP_SESSION.close)

# TODO(ahuszagh) Need to think about restructuring this, since we may just
# Want async and sync shared code, for tornado or non-tornado backends.
