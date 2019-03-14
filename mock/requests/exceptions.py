from urllib3.exceptions import HTTPError as BaseHTTPError


class RequestException(IOError):
    pass


class ChunkedEncodingError(RequestException):
    pass


class ConnectionError(RequestException):
    pass


class HTTPError(RequestException):
    pass


class ProxyError(RequestException):
    pass


class RetryError(RequestException):
    pass


class SSLError(RequestException):
    pass


class Timeout(RequestException):
    pass


class TooManyRedirects(RequestException):
    pass


class URLRequired(RequestException):
    pass


class UnrewindableBodyError(RequestException):
    pass


class InvalidHeader(RequestException, ValueError):
    pass


class InvalidSchema(RequestException, ValueError):
    pass


class InvalidURL(RequestException, ValueError):
    pass


class MissingSchema(RequestException, ValueError):
    pass


class ReadTimeout(Timeout):
    pass


class ContentDecodingError(RequestException, BaseHTTPError):
    pass


class StreamConsumedError(RequestException, TypeError):
    pass


class ConnectTimeout(ConnectionError, Timeout):
    pass


class InvalidProxyURL(InvalidURL):
    pass
