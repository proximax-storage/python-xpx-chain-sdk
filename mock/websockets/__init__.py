"""
    websockets
    ==========

    Mock version of the `websockets` package for unittesting.
"""

__version__ = "7.0"

__all__ = [
    # Package
    'connect',
    'parse_uri',
    'serve',
    'AbortHandshake',
    'ConnectionClosed',
    'DuplicateParameter',
    'InvalidHandshake',
    'InvalidHeader',
    'InvalidHeaderFormat',
    'InvalidHeaderValue',
    'InvalidMessage',
    'InvalidOrigin',
    'InvalidParameterName',
    'InvalidParameterValue',
    'InvalidState',
    'InvalidStatusCode',
    'InvalidUpgrade',
    'InvalidURI',
    'NegotiationError',
    'PayloadTooBig',
    'RedirectHandshake',
    'WebSocketClientProtocol',
    'WebSocketCommonProtocol',
    'WebSocketProtocolError',
    'WebSocketServerProtocol',
    'WebSocketURI',

    # Mock
    'default_exception',
    'default_response',
]


from .client import connect, WebSocketClientProtocol
from .exceptions import *
from .protocol import default_exception, default_response, WebSocketCommonProtocol
from .server import serve, WebSocketServerProtocol
from .uri import *
