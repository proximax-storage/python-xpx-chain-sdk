"""
    host
    ====

    HTTP client wrapper to inject the proper host (schema, domain and port)
    into requests providing solely a relative path.
"""

import typing
import urllib.error
import urllib3

# UTILITY


DEFAULT_PORT = {
    'http': 80,
    'https': 443,
    'ws': 80,
    'wss': 443
}


def parse_http_url(uri: str, scheme: str = 'http') -> 'urllib3.util.Url':
    """Add a default scheme if not present."""

    url = urllib3.util.parse_url(uri)
    if url.scheme is None:
        url = url._replace(scheme=scheme)
    if url.scheme not in ('http', 'https'):
        raise urllib.error.URLError("HTTP scheme not recognized.")
    if url.port is None:
        url._replace(port=DEFAULT_PORT[url.scheme])

    return url


def parse_ws_url(uri: str, scheme: str = 'ws') -> 'urllib3.util.Url':
    """Process a websockets URI and return the kwds for the initializer."""

    url = urllib3.util.parse_url(uri)
    if url.scheme is None:
        url = url._replace(scheme=scheme)
    if url.scheme not in ('ws', 'wss'):
        raise urllib.error.URLError("websockets scheme not recognized.")
    if url.port is None:
        url._replace(port=DEFAULT_PORT[url.scheme])

    return url


# HTTP


class Client:
    """
    Client wrapper for an abstract HTTP session.

    :param session: Requests or aiohttp-like HTTP client session.
    :param endpoint: Domain name and port for the endpoint.
    """

    def __init__(self, session, endpoint) -> None:
        self._session = session
        self._endpoint = parse_http_url(endpoint).url
        self._closed = False

    def __enter__(self) -> 'Client':
        return self

    def __exit__(self) -> None:
        self.close()

    def close(self):
        """Close the client session."""
        self._closed = True
        self._session.close()

    @property
    def closed(self) -> bool:
        """Get if client session has been closed."""
        return self._closed

    def get(self, relative_path, *args, **kwds):
        """
        Make GET request from relative path.

        :param relative_path: Relative path from endpoint prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self._endpoint + relative_path
        return self._session.get(path, *args, **kwds)

    def head(self, relative_path, *args, **kwds):
        """
        Make HEAD request from relative path.

        :param relative_path: Relative path from endpoint prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self._endpoint + relative_path
        return self._session.head(path, *args, **kwds)

    def options(self, relative_path, *args, **kwds):
        """
        Make OPTIONS request from relative path.

        :param relative_path: Relative path from endpoint prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self._endpoint + relative_path
        return self._session.options(path, *args, **kwds)

    def patch(self, relative_path, *args, **kwds):
        """
        Make PATCH request from relative path.

        :param relative_path: Relative path from endpoint prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self._endpoint + relative_path
        return self._session.patch(path, *args, **kwds)

    def post(self, relative_path, *args, **kwds):
        """
        Make POST request from relative path.

        :param relative_path: Relative path from endpoint prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self._endpoint + relative_path
        return self._session.post(path, *args, **kwds)

    def put(self, relative_path, *args, **kwds):
        """
        Make PUT request from relative path.

        :param relative_path: Relative path from endpoint prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self._endpoint + relative_path
        return self._session.put(path, *args, **kwds)

    def delete(self, relative_path, *args, **kwds):
        """
        Make DELETE request from relative path.

        :param relative_path: Relative path from endpoint prefixed with "/".
        :param \*args: Optional positional arguments for request.
        :param \**kwds: Optional keyword arguments for request.
        """

        path = self._endpoint + relative_path
        return self._session.delete(path, *args, **kwds)


class AsyncClient(Client):
    """
    Asynchronous client with a managed loop.

    :param session: Requests or aiohttp-like HTTP client session.
    :param endpoint: Domain name and port for the endpoint.
    :param loop: Event loop.
    """

    def __init__(self, session, endpoint, loop=None) -> None:
        self._session = session
        self._endpoint = parse_http_url(endpoint).url
        self._loop = loop

    def __enter__(self) -> 'AsyncClient':
        raise TypeError("Only use async with.")

    def __exit__(self) -> None:
        pass

    async def __aenter__(self) -> 'AsyncClient':
        return self

    async def __aexit__(self) -> None:
        await self.close()

    def __del__(self):
        if self._loop is not None and not self.closed:
            self._loop.run_until_complete(self.close())

    async def close(self):
        """Close the client session."""
        await self._session.close()

    @property
    def closed(self) -> bool:
        """Get if client session has been closed."""
        return typing.cast(bool, self._session.closed)


# WEBSOCKETS


class WebsocketClient:
    """Asynchronous host using websockets."""

    def __init__(self, session, loop=None) -> None:
        self._session = session
        self._loop = loop

    def __enter__(self) -> 'WebsocketClient':
        raise TypeError("Only use async with.")

    def __exit__(self) -> None:
        pass

    async def __aenter__(self) -> 'WebsocketClient':
        return self

    async def __aexit__(self) -> None:
        return await self.close()

    async def __aiter__(self) -> typing.AsyncIterator[typing.AnyStr]:
        async for message in self._session:
            yield typing.cast(typing.AnyStr, message)

    def __del__(self) -> None:
        if self._loop is not None:
            self._loop.run_until_complete(self.close())

    async def close(self) -> None:
        """Close the client session."""
        await self._session.wait_closed()

    @property
    def closed(self) -> bool:
        """Get if client session has been closed."""
        result = self._session.closed
        return typing.cast(bool, result)

    async def recv(self) -> typing.AnyStr:
        """Receive next message."""
        result = await self._session.recv()
        return typing.cast(typing.AnyStr, result)

    async def send(self, data: typing.AnyStr) -> None:
        """Send message."""
        await self._session.send(data)

    async def ping(self, data: typing.Optional[bytes] = None) -> typing.Awaitable[None]:
        """Send websocket a ping."""
        result = await self._session.ping(data)
        return typing.cast(typing.Awaitable[None], result)

    async def pong(self, data: bytes = b'') -> None:
        """Send websocket a pong."""
        await self._session.pong(data)
