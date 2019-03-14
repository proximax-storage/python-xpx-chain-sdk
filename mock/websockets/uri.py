import urllib.parse
import typing

from .exceptions import InvalidURI


class WebSocketURI(typing.NamedTuple):
    secure: bool
    host: str
    port: int
    resource_name: str
    user_info: typing.Optional[typing.Tuple[str, str]]


def parse_uri(uri: str) -> WebSocketURI:
    parsed = urllib.parse.urlparse(uri)
    if parsed.scheme not in ["ws", "wss"]:
        raise InvalidURI(uri)

    secure = parsed.scheme == "wss"
    host = parsed.hostname
    port = parsed.port or (443 if secure else 80)
    resource_name = parsed.path or "/"
    if parsed.query:
        resource_name += "?" + parsed.query
    user_info = None
    if parsed.username or parsed.password:
        user_info = (parsed.username, parsed.password)
    return WebSocketURI(secure, host, port, resource_name, user_info)
