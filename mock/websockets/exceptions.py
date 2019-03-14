class InvalidHandshake(Exception):
    pass


class InvalidState(Exception):
    pass


class InvalidURI(Exception):
    pass


class PayloadTooBig(Exception):
    pass


class WebSocketProtocolError(Exception):
    pass


class AbortHandshake(InvalidHandshake):
    pass


class InvalidHeader(InvalidHandshake):
    pass


class InvalidMessage(InvalidHandshake):
    pass


class InvalidStatusCode(InvalidHandshake):
    pass


class NegotiationError(InvalidHandshake):
    pass


class RedirectHandshake(InvalidHandshake):
    pass


class InvalidHeaderFormat(InvalidHeader):
    pass


class InvalidHeaderValue(InvalidHeader):
    pass


class InvalidOrigin(InvalidHeader):
    pass


class InvalidUpgrade(InvalidHeader):
    pass


class ConnectionClosed(InvalidState):
    pass


class DuplicateParameter(NegotiationError):
    pass


class InvalidParameterName(NegotiationError):
    pass


class InvalidParameterValue(NegotiationError):
    pass
