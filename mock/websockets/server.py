import asyncio

from .exceptions import InvalidHandshake, InvalidOrigin
from .protocol import WebSocketCommonProtocol


class WebSocketServerProtocol(WebSocketCommonProtocol):
    """Protocol for websockets server."""

    is_client = False
    side = "server"

    def __init__(
        self,
        origin=None,
        extensions=None,
        subprotocols=None,
        extra_headers=None,
        process_request=None,
        select_subprotocol=None,
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

    def process_request(self, path, request_headers):
        return None

    @staticmethod
    def process_origin(headers, origins):
        raise InvalidOrigin

    @staticmethod
    def process_extensions(headers, available_extensions):
        raise InvalidHandshake

    @staticmethod
    def process_subprotocol(headers, available_subprotocols):
        raise InvalidHandshake

    def select_subprotocol(self, client_subprotocols, server_subprotocols):
        raise NotImplementedError


class WebsocketServer:
    """Core websockets server."""

    def __init__(self, loop):
        self.loop = loop or asyncio.get_event_loop()
        self.websockets = set()
        self.close_task = None
        self.closed_waiter = self.loop.create_future()
        self._closed = False

    def is_serving(self) -> bool:
        return not self._closed

    def register(self, protocol):
        self.websockets.add(protocol)

    def unregister(self, protocol):
        self.websockets.remove(protocol)

    def close(self):
        self.close_task = self.loop.create_task(self._close())

    async def _close(self):
        self._closed = True
        self.closed_waiter.set_result(None)

    async def wait_closed(self):
        await asyncio.shield(self.closed_waiter)

    @property
    def sockets(self):
        return None


class Serve:
    """Context manager that guards WebSocketServerProtocol within a block."""

    def __init__(self, ws_handler, host, port, *, loop=None, **kwds):
        self._ws_handler = ws_handler
        self._kwds = kwds
        self._kwds.setdefault("host", host)
        self._kwds.setdefault("port", port)
        self._loop = loop or asyncio.get_event_loop()
        self.ws_server = WebsocketServer(self._loop)
        raise NotImplementedError

    async def __aenter__(self):
        return await self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.ws_server.close()
        await self.ws_server.wait_closed()

    def __await__(self):
        return self.ws_server

    def __iter__(self):
        return self.ws_server


serve = Serve
