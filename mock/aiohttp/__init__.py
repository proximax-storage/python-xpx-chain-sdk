"""
    requests
    ========

    Mock version of the `aiohttp` package for unittesting.
"""

import chardet
import contextlib
import copy
import json
import asyncio

__version__ = "3.5.4"


class ClientError(Exception):
    pass


class ClientResponseError(ClientError):
    pass


class ContentTypeError(ClientResponseError):
    pass


class WSServerHandshakeError(ClientResponseError):
    pass


class ClientHttpProxyError(ClientResponseError):
    pass


class TooManyRedirects(ClientResponseError):
    pass


class ClientConnectionError(ClientError):
    pass


class ClientOSError(ClientConnectionError, OSError):
    pass


class ClientConnectorError(ClientOSError):
    pass


class ClientProxyConnectionError(ClientConnectorError):
    pass


class ServerConnectionError(ClientConnectionError):
    pass


class ServerDisconnectedError(ServerConnectionError):
    pass


class ServerTimeoutError(ServerConnectionError, asyncio.TimeoutError):
    pass


class ServerFingerprintMismatch(ServerConnectionError):
    pass


class ClientPayloadError(ClientError):
    pass


class InvalidURL(ClientError, ValueError):
    pass


class ClientSSLError(ClientConnectorError):
    pass


class ClientConnectorSSLError(ClientSSLError):
    pass


class ClientConnectorCertificateError(ClientSSLError, ValueError):
    pass


class CaseInsensitiveDict(dict):
    """Dict which performs case-insensitive lookups"""

    def __init__(self, *args, **kwds):
        d = dict(*args, **kwds)
        self.d = {k.lower(): v for k, v in d.items()}

    def __contains__(self, key):
        return key.lower() in self.d

    def __delitem__(self, key):
        del self.d[key.lower()]

    def __eq__(self, other):
        if not isinstance(other, CaseInsensitiveDict):
            return False
        return self.d == other.d

    def __getitem__(self, key):
        return self.d[key.lower()]

    def __iter__(self):
        return iter(self.d)

    def __len__(self):
        return len(self.d)

    def __setitem__(self, key, value):
        self.d[key.lower()] = value

    def clear(self):
        self.d.clear()

    def copy(self):
        cpy = CaseInsensitiveDict.__new__(CaseInsensitiveDict)
        cpy.d = self.d.copy()
        return cpy

    @classmethod
    def fromkeys(cls, iterable, *value):
        d = dict.fromkeys(iterable, *value)
        return cls(d)

    def get(self, key):
        return self.d.get(key.lower())

    def items(self):
        return self.d.items()

    def keys(self):
        return self.d.keys()

    def pop(self, key, *default):
        return self.d.pop(key.lower(), *default)

    def popitem(self):
        return self.d.popitem()

    def setdefault(self, key, *default):
        return self.d.setdefault(key.lower(), *default)

    def update(self, *args, **kwds):
        d = dict(*args, **kwds)
        self.update({k.lower(): v for k, v in d.items()})

    def values(self):
        return self.d.values()

    __hash__ = None


class ClientResponse:

    def __init__(self):
        self.status = None
        self._headers = None
        self.cookies = None
        self._url = None
        self._content = None
        self._encoding = None
        self._closed = None

    @classmethod
    def mock(cls, status, **kwds):
        inst = ClientResponse()
        inst.status = status
        inst._headers = kwds.get('headers', CaseInsensitiveDict())
        inst._content = kwds.get('content', b'')
        inst._encoding = kwds.get('encoding')
        inst._closed = False

        return inst

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        self.close()

    def close(self):
        self._closed = True

    def release(self):
        self.close()

    @property
    def url(self):
        return self._url

    @property
    def headers(self):
        return self._headers

    @property
    def closed(self):
        return self._closed

    async def read(self):
        return self._content

    def get_encoding(self):
        return self._encoding or chardet.detect(self._content)['encoding']

    async def text(self, encoding=None):
        if not self._content:
            return ''
        encoding = encoding or self.get_encoding()
        return self._content.decode(encoding)

    async def json(self, encoding=None):
        encoding = encoding or self.get_encoding()
        return json.loads(self._content.decode(encoding))

    def raise_for_status(self):
        if self.status >= 400:
            raise ClientResponseError("Error: {}".format(self.status))


class AsyncContextManager:

    def __init__(self, coro):
        self._coro = coro

    def send(self, arg):
        return self._coro.send(arg)

    def throw(self, arg):
        self._coro.throw(arg)

    def close(self):
        return self._coro.close()

    def __await__(self):
        ret = self._coro.__await__()
        return ret

    def __iter__(self):
        return self.__await__()

    async def __aenter__(self):
        self._resp = await self._coro
        return self._resp

    async def __aexit__(self, *args) -> None:
        self._resp.release()


class ClientSession:

    def __init__(self, **kwds):
        self._closed = False

    def __enter__(self):
        raise TypeError("Use `async with` instead.")

    def __exit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    @property
    def closed(self):
        return self._closed

    async def close(self):
        self._closed = True

    def request(self, method, url, **kwds):
        return AsyncContextManager(self._request(method, url, **kwds))

    async def _request(self, method, url, **kwds):
        if EXCEPTION is not None:
            raise EXCEPTION
        elif RESPONSE is None:
            raise RuntimeError("Must use within `default_response` block.")
        response = copy.copy(RESPONSE)
        response._url = url
        return response

    def get(self, url, params=None, **kwds):
        return self.request('GET', url, params=params, **kwds)

    def head(self, url, **kwds):
        return self.request('HEAD', url, **kwds)

    def options(self, url, **kwds):
        return self.request('OPTIONS', url, **kwds)

    def patch(self, url, data=None, **kwds):
        return self.request('PATCH', url, data=data, **kwds)

    def post(self, url, data=None, json=None, **kwds):
        return self.request('POST', url, data=data, json=json, **kwds)

    def put(self, url, data=None, **kwds):
        return self.request('PUT', url, data=data, **kwds)

    def delete(self, url, **kwds):
        return self.request('DELETE', url, **kwds)


# MOCKING

EXCEPTION = None
RESPONSE = None


@contextlib.contextmanager
def default_exception(exception_type, *args, **kwds):
    """Set the global, default exception."""

    global EXCEPTION
    try:
        EXCEPTION = exception_type(*args, **kwds)
        yield
    finally:
        EXCEPTION = None


@contextlib.contextmanager
def default_response(status=200, **kwds):
    """Set the global, default response."""

    global RESPONSE
    try:
        RESPONSE = ClientResponse.mock(status, **kwds)
        yield
    finally:
        RESPONSE = None
