from .exceptions import InvalidHandshake
from .protocol import WebSocketCommonProtocol
from .uri import parse_uri


class WebSocketClientProtocol(WebSocketCommonProtocol):
    """Protocol for websockets client."""

    is_client = True
    side = "client"

    def __init__(
        self,
        origin=None,
        extensions=None,
        subprotocols=None,
        extra_headers=None,
        **kwds,
    ):
        self.origin = origin
        self.extensions = extensions
        self.subprotocols = subprotocols
        self.extra_headers = extra_headers
        super().__init__(**kwds)

    def write_http_request(self, path, headers):
        raise NotImplementedError

    def read_http_response(self):
        raise NotImplementedError

    @staticmethod
    def process_extensions(headers, available_extensions):
        raise InvalidHandshake

    @staticmethod
    def process_subprotocol(headers, available_subprotocols):
        raise InvalidHandshake

    async def handshake(
        self,
        wsuri,
        origin,
        available_extensions,
        available_subprotocols,
        extra_headers
    ):
        pass


class Connect:
    """Context manager that guards WebSocketClientProtocol within a block."""

    def __init__(self, uri, *args, **kwds):
        self._wsuri = parse_uri(uri)
        self._kwds = kwds
        self._kwds.setdefault("host", self._wsuri.host)
        self._kwds.setdefault("port", self._wsuri.port)
        self._kwds.setdefault("secure", self._wsuri.secure)
        self.ws_client = WebSocketClientProtocol(**self._kwds)

    async def __aenter__(self):
        return await self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.ws_client.close()

    def __await__(self):
        return self.await_impl().__await__()

    async def await_impl(self):
        return self.ws_client

    __iter__ = __await__


connect = Connect
