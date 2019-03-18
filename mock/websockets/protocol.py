import asyncio
import contextlib
import itertools

from .exceptions import ConnectionClosed

EXCEPTION = None
MESSAGE = None


class WebSocketCommonProtocol:
    """Shared protocol for client and server."""

    def __init__(
        self,
        host=None,
        port=None,
        secure=None,
        ping_interval=20,
        ping_timeout=20,
        close_timeout=None,
        max_size=2 ** 20,
        max_queue=2 ** 5,
        read_limit=2 ** 16,
        write_limit=2 ** 16,
        loop=None,
    ):
        self.host = host
        self.port = port
        self.secure = secure
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.close_timeout = close_timeout
        self.max_size = max_size
        self.max_queue = max_queue
        self.read_limit = read_limit
        self.write_limit = write_limit
        self.loop = loop or asyncio.get_event_loop()
        self._closed = False
        self._iter = {}

    @property
    def local_address(self):
        return (self.host, self.port)

    @property
    def remote_address(self):
        return (self.host, self.port)

    @property
    def open(self):
        return not self.closed

    @property
    def closed(self):
        return self._closed

    async def wait_closed(self):
        await self.close()

    async def __aiter__(self):
        try:
            while True:
                yield await self.recv()
        except ConnectionClosed as exc:
            if exc.code == 1000 or exc.code == 1001:
                return
            else:
                raise

    async def recv(self):
        if EXCEPTION is not None:
            raise EXCEPTION
        elif MESSAGE is None:
            raise RuntimeError("Must use within `default_response` block.")

        self._iter.setdefault(id(MESSAGE), itertools.cycle(MESSAGE))
        return next(self._iter[id(MESSAGE)])

    async def send(self, message):
        pass

    async def close(self, code=1000, reason=""):
        self._closed = True

    async def ping(self, data=None):
        async def inner():
            return None
        if EXCEPTION is not None:
            raise EXCEPTION
        return inner()

    async def pong(self, data):
        if EXCEPTION is not None:
            raise EXCEPTION


# MOCKING


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
def default_response(data):
    """Set the global, default response."""

    global MESSAGE
    try:
        MESSAGE = data
        yield
    finally:
        MESSAGE = None
