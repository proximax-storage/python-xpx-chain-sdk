"""
    fallback
    ========

    Fallback ed25519 implementation if a C implementation is not installed.

    Optimized version of the reference implementation of Ed25519

    Written in 2011? by Daniel J. Bernstein <djb@cr.yp.to>
               2013 by Donald Stufft <donald@stufft.io>
               2013 by Alex Gaynor <alex.gaynor@gmail.com>
               2013 by Greg Price <price@mit.edu>

    Modified in 2019 by Alex Huszagh <ahuszagh@gmail.com>

    .. warning::
        This code is not safe for use with secret keys or secret data.
        This code is susceptible to timing and side-channel attacks,
        since it uses Python's arbitrary-precision integer arithmetic,
        which may lead to the disclosure of the secrets.

    License
    -------

    Copyright 2019 NEM

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from __future__ import annotations
import os
import typing
import warnings

from xpxchain.util import bit

# EXCEPTIONS

HashFuncType = typing.Callable[[bytes], bytes]
SECRET_LEAK_MSG = (
    'Security warning: {} using insecure ed25519'  # nosec
    ' implementation, secrets may be leaked.'
)


class SecretsWarning(UserWarning):
    pass


# API


def generate_api(hash512: HashFuncType):        # noqa: C901
    """Generate the ed25519 API from a hash function."""

    class BadSignatureError(Exception):
        pass

    class SigningKey:
        """Signing (secret) key."""

        def __init__(self, signing_key: bytes):
            if len(signing_key) == 64:
                self._signing_key = signing_key
            elif len(signing_key) == 32:
                self._signing_key = publickey(signing_key, hash512)[0]
            else:
                raise ValueError("Invalid signing key or seed length.")

        def __eq__(self, other):
            if not isinstance(other, SigningKey):
                return False
            return self._signing_key == other._signing_key

        def to_bytes(self) -> bytes:
            """Export signing key to bytes."""

            return self._signing_key

        def to_seed(self) -> bytes:
            """Export seed from signing key."""

            return self._signing_key[:32]

        def get_verifying_key(self) -> 'VerifyingKey':
            """Get verifying key from signing key."""

            return VerifyingKey(self._signing_key[32:])

        def sign(self, message: bytes) -> bytes:
            """Sign message and return signature."""

            return sign(message, self._signing_key, hash512)

        __hash__ = None

    class VerifyingKey:
        """Verifying (public) key."""

        def __init__(self, verifying_key: bytes):
            if len(verifying_key) != 32:
                raise ValueError("Invalid verifying key length.")
            self._verifying_key = verifying_key

        def __eq__(self, other):
            if not isinstance(other, VerifyingKey):
                return False
            return self._verifying_key == other._verifying_key

        def to_bytes(self) -> bytes:
            """Export verifying key to bytes."""

            return self._verifying_key

        def verify(self, signature: bytes, message: bytes) -> None:
            """Verify signature from message."""

            if not verify(self._verifying_key, signature, message, hash512):
                raise BadSignatureError("Bad signature")

        __hash__ = None

    def create_keypair(entropy=os.urandom):
        """Generate signing/verifying keypair from entropy."""

        signing_key = SigningKey(entropy(32))
        verifying_key = signing_key.get_verifying_key()
        return signing_key, verifying_key

    return BadSignatureError, SigningKey, VerifyingKey, create_keypair


# UTILITY

Point = typing.Tuple[int, int, int, int]

BITS: int = 256
Q: int = 2 ** 255 - 19
L: int = 2 ** 252 + 27742317777372353535851937790883648493


def pow2(x: int, p: int) -> int:
    """== pow(x, 2**p, q)"""

    while p > 0:
        x = x * x % Q
        p -= 1
    return x


def zero_msb(s: bytes) -> bytes:
    """Zero the most-significant bit in an array."""

    s = bytearray(s)
    s[31] = bit.clear(s[31], 7)
    return bytes(s)


def hint(m: bytes, hash512: HashFuncType) -> int:
    return int.from_bytes(hash512(m), 'little')


def inv(z: int) -> int:
    """$= z^{-1} \\mod q$, for z != 0"""

    # Adapted from curve25519_athlon.c in djb's Curve25519.
    z2 = z * z % Q                                  # 2
    z9 = pow2(z2, 2) * z % Q                        # 9
    z11 = z9 * z2 % Q                               # 11
    z2_5_0 = (z11 * z11) % Q * z9 % Q               # 31 == 2^5 - 2^0
    z2_10_0 = pow2(z2_5_0, 5) * z2_5_0 % Q          # 2^10 - 2^0
    z2_20_0 = pow2(z2_10_0, 10) * z2_10_0 % Q       # ...
    z2_40_0 = pow2(z2_20_0, 20) * z2_20_0 % Q
    z2_50_0 = pow2(z2_40_0, 10) * z2_10_0 % Q
    z2_100_0 = pow2(z2_50_0, 50) * z2_50_0 % Q
    z2_200_0 = pow2(z2_100_0, 100) * z2_100_0 % Q
    z2_250_0 = pow2(z2_200_0, 50) * z2_50_0 % Q     # 2^250 - 2^0
    return pow2(z2_250_0, 5) * z11 % Q              # 2^255 - 2^5 + 11 = q - 2


D: int = -121665 * inv(121666) % Q
I: int = pow(2, (Q - 1) // 4, Q)


def xrecover(y: int) -> int:
    xx: int = (y * y - 1) * inv(D * y * y + 1)
    x: int = pow(xx, (Q + 3) // 8, Q)

    if (x * x - xx) % Q != 0:
        x = (x * I) % Q

    if x % 2 != 0:
        x = Q - x

    return x


BY: int = 4 * inv(5)
BX: int = xrecover(BY)
B: Point = (BX % Q, BY % Q, 1, (BX * BY) % Q)
IDENT: Point = (0, 1, 1, 0)


def edwards_add(p: Point, q: Point) -> Point:
    # This is formula sequence 'addition-add-2008-hwcd-3' from
    # http://www.hyperelliptic.org/EFD/g1p/auto-twisted-extended-1.html
    (x1, y1, z1, t1) = p
    (x2, y2, z2, t2) = q

    a: int = (y1 - x1) * (y2 - x2) % Q
    b: int = (y1 + x1) * (y2 + x2) % Q
    c: int = t1 * 2 * D * t2 % Q
    d: int = z1 * 2 * z2 % Q
    e: int = b - a
    f: int = d - c
    g: int = d + c
    h: int = b + a
    x3: int = e * f
    y3: int = g * h
    t3: int = e * h
    z3: int = f * g

    return (x3 % Q, y3 % Q, z3 % Q, t3 % Q)


def edwards_double(p: Point) -> Point:
    # This is formula sequence 'dbl-2008-hwcd' from
    # http://www.hyperelliptic.org/EFD/g1p/auto-twisted-extended-1.html
    (x1, y1, z1, t1) = p

    a: int = x1 * x1 % Q
    b: int = y1 * y1 % Q
    c: int = 2 * z1 * z1 % Q
    # d: int = -a
    e: int = ((x1 + y1) * (x1 + y1) - a - b) % Q
    g: int = -a + b  # d + b
    f: int = g - c
    h: int = -a - b  # d - b
    x3: int = e * f
    y3: int = g * h
    t3: int = e * h
    z3: int = f * g

    return (x3 % Q, y3 % Q, z3 % Q, t3 % Q)


def scalarmult(p: Point, e: int) -> Point:
    if e == 0:
        return IDENT
    q: Point = scalarmult(p, e // 2)
    q = edwards_double(q)
    if e & 1:
        q = edwards_add(q, p)
    return q


def make_bpow() -> typing.List[Point]:
    """BPOW[i] == scalarmult(B, 2**i)"""

    bpow = []
    p: Point = B
    for i in range(253):
        bpow.append(p)
        p = edwards_double(p)

    return bpow


BPOW = make_bpow()


def scalarmult_b(e: int) -> Point:
    """Implements scalarmult(B, e) more efficiently."""
    # scalarmult(B, L) is the identity
    e = e % L
    p = IDENT
    for i in range(253):
        if e & 1:
            p = edwards_add(p, BPOW[i])
        e = e // 2

    assert e == 0
    return p


def encode_uint256(y: int) -> bytes:
    """Encode 256-bit integer to little-endian buffer."""

    return y.to_bytes(32, 'little')


def encode_point(p: Point) -> bytes:
    """Encode point along the elliptical curve."""

    (x, y, z, t) = p
    zi = inv(z)
    x = (x * zi) % Q
    y = (y * zi) % Q

    s = bytearray(encode_uint256(y))
    s[31] = bit.assign(s[31], 7, x & 1 == 1)

    return bytes(s)


def is_on_curve(p: Point) -> bool:
    (x, y, z, t) = p
    return (
        z % Q != 0
        and x * y % Q == z * t % Q
        and (y * y - x * x - z * z - D * t * t) % Q == 0
    )


def decode_uint256(s: bytes) -> int:
    """Decode 256-bit integer from little-endian buffer."""

    assert len(s) == 32
    return int.from_bytes(s, 'little')


def decode_point(s: bytes) -> Point:
    """Decode point along the elliptical curve."""

    assert len(s) == 32
    y = decode_uint256(zero_msb(s))
    x = xrecover(y)
    if x & 1 != bit.get(s[31], 7):
        x = Q - x
    p = (x, y, 1, (x * y) % Q)
    if not is_on_curve(p):
        raise ValueError("decoding point that is not on curve")
    return p


def decode_hash512(h: bytes) -> int:
    """Decode 512-bit hash to 256-bit integer"""

    assert len(h) == 64

    # Modify the hash buffer to clear bits prior to encoding.
    h = bytearray(h[:32])
    h[0] &= 248
    h[31] &= 127
    h[31] |= 64

    return decode_uint256(h)


def publickey(
    seed: bytes,
    hash512: HashFuncType
) -> typing.Tuple[bytes, bytes]:
    """Generate public and private key from seed."""

    warning_msg = SECRET_LEAK_MSG.format('generating verifying key')
    warnings.warn(warning_msg, SecretsWarning)

    assert len(seed) == 32

    h = hash512(seed)
    a = decode_hash512(h)
    public_key: bytes = encode_point(scalarmult_b(a))
    return seed + public_key, public_key


def sign(
    message: bytes,
    signing_key: bytes,
    hash512: HashFuncType
) -> bytes:
    """Sign message using public and private key."""

    warning_msg = SECRET_LEAK_MSG.format('signing message')
    warnings.warn(warning_msg, SecretsWarning)

    if len(signing_key) != 64:
        raise ValueError("Invalid signing key length.")

    seed = signing_key[:32]
    verifying_key = signing_key[32:64]
    h = hash512(seed)
    a = decode_hash512(h)
    r = hint(h[32:64] + message, hash512)
    p = scalarmult_b(r)
    s = (r + hint(encode_point(p) + verifying_key + message, hash512) * a) % L
    return encode_point(p) + encode_uint256(s)


def verify(
    verifying_key: bytes,
    signature: bytes,
    message: bytes,
    hash512: HashFuncType
) -> bool:
    """
    Verify signature from public key and message.

    :param verifying_key: Key to verify signature.
    :param signature: Signature generated from message.
    :param message: Original message.
    """

    warning_msg = SECRET_LEAK_MSG.format('verifying signature')
    warnings.warn(warning_msg, SecretsWarning)

    if len(verifying_key) != 32:
        raise ValueError("Invalid verifying key length.")
    if len(signature) != 64:
        raise ValueError("Invalid signature length.")

    r = decode_point(signature[:32])
    a = decode_point(verifying_key)
    s = decode_uint256(signature[32: 64])
    h = hint(encode_point(r) + verifying_key + message, hash512)

    (x1, y1, z1, t1) = p = scalarmult_b(s)
    (x2, y2, z2, t2) = q = edwards_add(r, scalarmult(a, h))

    return (
        is_on_curve(p)
        and is_on_curve(q)
        and (x1 * z2 - x2 * z1) % Q == 0
        and (y1 * z2 - y2 * z1) % Q == 0
    )
