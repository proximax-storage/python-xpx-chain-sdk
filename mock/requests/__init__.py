"""
    requests
    ========

    Mock version of the `requests` package for unittesting.
"""

import chardet
import contextlib
import copy
import datetime
import json

from .exceptions import *

__version__ = "2.21"


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


class Response:

    def __init__(self):
        self.status_code = None
        self.headers = None
        self.cookies = None
        self.url = None
        self._content = None
        self.encoding = None
        self.elapsed = None

    @classmethod
    def mock(cls, status_code, **kwds):
        inst = Response()
        inst.status_code = status_code
        inst.headers = kwds.get('headers', CaseInsensitiveDict())
        inst._content = kwds.get('content', b'')
        inst.encoding = kwds.get('encoding')
        inst.elapsed = kwds.get('elapsed', datetime.timedelta(0))

        return inst

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def __bool__(self):
        return self.ok

    def __iter__(self):
        return iter(self.content)

    def close(self):
        pass

    @property
    def ok(self):
        return self.status_code < 400

    @property
    def is_redirect(self):
        raise NotImplementedError

    @property
    def is_permanent_redirect(self):
        raise NotImplementedError

    @property
    def next(self):
        raise NotImplementedError

    @property
    def apparent_encoding(self):
        return chardet.detect(self.content)['encoding']

    @property
    def content(self):
        return self._content

    @property
    def text(self):
        if not self._content:
            return ''
        encoding = self.encoding or self.apparent_encoding
        return self.content.decode(encoding)

    def json(self):
        encoding = self.encoding or self.apparent_encoding
        return json.loads(self.content.decode(encoding))

    def raise_for_status(self):
        if not self.ok:
            raise HTTPError("Error: {}".format(self.status_code))


class Session:

    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def close(self):
        pass

    def request(self, method, url, **kwds):
        if EXCEPTION is not None:
            raise EXCEPTION
        elif RESPONSE is None:
            raise RuntimeError("Must use within `default_response` block.")
        response = copy.copy(RESPONSE)
        response.url = url
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


def request(method, url, **kwds):
    with Session() as session:
        return session.request(method, url, **kwds)


def get(url, params=None, **kwds):
    return request('GET', url, params=params, **kwds)


def head(url, **kwds):
    return request('HEAD', url, **kwds)


def options(url, **kwds):
    return request('OPTIONS', url, **kwds)


def patch(url, data=None, **kwds):
    return request('PATCH', url, data=data, **kwds)


def post(url, data=None, json=None, **kwds):
    return request('POST', url, data=data, json=json, **kwds)


def put(url, data=None, **kwds):
    return request('PUT', url, data=data, **kwds)


def delete(url, **kwds):
    return request('DELETE', url, **kwds)


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
def default_response(status_code=200, **kwds):
    """Set the global, default response."""

    global RESPONSE
    try:
        RESPONSE = Response.mock(status_code, **kwds)
        yield
    finally:
        RESPONSE = None
