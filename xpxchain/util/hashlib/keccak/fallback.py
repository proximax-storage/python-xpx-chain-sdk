"""
    keccak
    ======

    Fallback implementation of v52 of the keccak hash functions.

    The Keccak sponge function was designed by Guido Bertoni, Joan Daemen,
    Michaël Peeters and Gilles Van Assche. For more information, feedback or
    questions, please refer to their website: http://keccak.noekeon.org/

    Based on the implementation by Renaud Bauvin,
    from http://keccak.noekeon.org/KeccakInPython-3.0.zip

    Modified by Moshe Kaplan to be hashlib-compliant.
    Modified by Alex Huszagh for Python3-compliance and best coding practices.

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
import binascii
import math
import typing

# API


def keccak_224(data: typing.Optional[bytes] = None) -> Keccak:
    """Returns a 224-bit keccak hash object"""

    return Keccak(c=448, r=1152, n=224, name='keccak_224', data=data)


def keccak_256(data: typing.Optional[bytes] = None) -> Keccak:
    """Returns a 256-bit keccak hash object"""

    return Keccak(c=512, r=1088, n=256, name='keccak_256', data=data)


def keccak_384(data: typing.Optional[bytes] = None) -> Keccak:
    """Returns a 384-bit keccak hash object"""

    return Keccak(c=768, r=832, n=384, name='keccak_384', data=data)


def keccak_512(data: typing.Optional[bytes] = None) -> Keccak:
    """Returns a 512-bit keccak hash object"""

    return Keccak(c=1024, r=576, n=512, name='keccak_512', data=data)

# HASHER


class KeccakError(Exception):
    """Custom error Class used in the Keccak implementation"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Keccak:
    """Hashlib-compatible object for the v52 of the Keccak hash function."""

    def __init__(
        self,
        r: int,
        c: int,
        n: int,
        name: str,
        data: typing.Optional[bytes] = None
    ) -> None:
        # Initialize the constants used throughout Keccak bitrate
        self.r = r
        # capacity
        self.c = c
        # output size
        self.n = n

        self.b = r + c
        # b = 25*w
        self.w = self.b // 25
        # 2**l = w
        self.l = int(math.log(self.w, 2))

        self.n_r = 12 + 2 * self.l

        self.block_size = r / 8
        self.digest_size = n / 8
        self.name = name

        # Initialize the state of the sponge
        # The state is made up of 25 words, each word being w bits.
        self.state = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

        # A string of hexchars, where each char represents 4 bits.
        self.buffered_data = b""

        # Store the calculated digest.
        # We'll only apply padding and recalculate the hash if it's modified.
        self.last_digest: typing.Optional[bytes] = None

        if data:
            self.update(data)

    def update(self, data: bytes) -> None:
        """Update this hash object's state with the provided bytes-like object."""

        # Convert the data into a workable format, and add it to the buffer
        self.last_digest = None
        self.buffered_data += binascii.hexlify(data)

        # Absorb any blocks we can:
        if len(self.buffered_data) * 4 >= self.r:
            extra_bits = len(self.buffered_data) * 4 % self.r

            # An exact fit!
            if extra_bits == 0:
                p = self.buffered_data
                self.buffered_data = b""
            else:
                # Slice it up into the first r*a bits, for some constant
                # a>=1, and the remaining total-r*a bits.
                p = self.buffered_data[:-extra_bits // 4]
                self.buffered_data = self.buffered_data[-extra_bits // 4:]

            # Absorbing phase
            for i in range((len(p) * 8 // 2) // self.r):
                start_i = i * (2 * self.r // 8)
                stop_i = (i + 1) * (2 * self.r // 8)
                to_convert = p[start_i:stop_i] + b'00' * (self.c // 8)
                p_i = _convert_str_to_table(to_convert, self.w, self.b)

                # First apply the XOR to the state + block
                for y in range(5):
                    for x in range(5):
                        self.state[x][y] = self.state[x][y] ^ p_i[x][y]
                # Then apply the block permutation, Keccak-F
                self.state = _keccakf(self.state, self.n_r, self.w)

    def digest(self) -> bytes:
        """Return the digest value as a bytes object."""

        if self.last_digest:
            return self.last_digest

        # First finish the padding and force the final update:
        self.buffered_data = _pad10star1(self.buffered_data, self.r)
        self.update(b'')
        assert len(self.buffered_data) == 0

        # Squeezing time!
        z = b''
        output_length = self.n
        while output_length > 0:
            string = _convert_table_to_str(self.state, self.w)
            # Read the first 'r' bits of the state
            z = z + string[:self.r * 2 // 8]
            output_length -= self.r
            if output_length > 0:
                self.state = _keccakf(self.state, self.n_r, self.w)

        self.last_digest = binascii.unhexlify(z[:2 * self.n // 8])
        return self.last_digest

    def hexdigest(self) -> str:
        """Return the digest value as a string of hexadecimal digits."""

        return binascii.hexlify(self.digest()).decode('ascii')

    def copy(self) -> Keccak:
        """Return a copy of the hash object."""

        # First initialize whatever can be done normally
        duplicate = Keccak(c=self.c, r=self.r, n=self.n, name=self.name)
        # Copy over the state.
        for i in range(5):
            for j in range(5):
                duplicate.state[i][j] = self.state[i][j]
        # Copy over other stored data.
        duplicate.buffered_data = self.buffered_data
        duplicate.last_digest = self.last_digest
        return duplicate

# UTILITY


_ROUND_CONSTANTS = [
    0x0000000000000001,
    0x0000000000008082,
    0x800000000000808A,
    0x8000000080008000,
    0x000000000000808B,
    0x0000000080000001,
    0x8000000080008081,
    0x8000000000008009,
    0x000000000000008A,
    0x0000000000000088,
    0x0000000080008009,
    0x000000008000000A,
    0x000000008000808B,
    0x800000000000008B,
    0x8000000000008089,
    0x8000000000008003,
    0x8000000000008002,
    0x8000000000000080,
    0x000000000000800A,
    0x800000008000000A,
    0x8000000080008081,
    0x8000000000008080,
    0x0000000080000001,
    0x8000000080008008
]

_ROTATION_OFFSETS = [
    [0,  36,   3,  41,  18],    # noqa: E241
    [1,  44,  10,  45,   2],    # noqa: E241
    [62,  6,  43,  15,  61],    # noqa: E241
    [28, 55,  25,  21,  56],    # noqa: E241
    [27, 20,  39,   8,  14],    # noqa: E241
]


def _rot(x, shift_amount, length):
    """
    Rotate x shift_amount bits to the left, considering the string of
    bits is length bits long.
    """

    shift_amount = shift_amount % length
    return ((x >> (length - shift_amount)) + (x << shift_amount)) % (1 << length)


def _round(a, rc_fixed, w):
    """
    Perform one round of computation as defined in the Keccak-f permutation.

    :param a: 5x5 matrix containing the state.
    :param rc_fixed: Value of round-constant to use.
    :param w: Word size.
    """

    # Initialization of temporary variables
    b = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    c = [0, 0, 0, 0, 0]
    d = [0, 0, 0, 0, 0]

    # Theta step
    for x in range(5):
        c[x] = a[x][0] ^ a[x][1] ^ a[x][2] ^ a[x][3] ^ a[x][4]

    for x in range(5):
        d[x] = c[(x - 1) % 5] ^ _rot(c[(x + 1) % 5], 1, w)

    for x in range(5):
        for y in range(5):
            a[x][y] = a[x][y] ^ d[x]

    # Rho and Pi steps
    for x in range(5):
        for y in range(5):
            b[y][(2 * x + 3 * y) % 5] = _rot(a[x][y], _ROTATION_OFFSETS[x][y], w)

    # Chi step
    for x in range(5):
        for y in range(5):
            a[x][y] = b[x][y] ^ ((~b[(x + 1) % 5][y]) & b[(x + 2) % 5][y])

    # Iota step
    a[0][0] = a[0][0] ^ rc_fixed

    return a


def _keccakf(a, n_r, w):
    """
    Perform Keccak-f function on the state a.

    :param a: 5x5 matrix containing the state.
    :param n_r: Number of rounds.
    :param w: Word size.
    """

    for i in range(n_r):
        a = _round(a, _ROUND_CONSTANTS[i] % (1 << w), w)
    return a


def _get_byte(hex_string: bytes, bytes_filled: int, bits_filled: int):
    if bits_filled == 0:
        byte = 0
    else:
        byte = int(hex_string[bytes_filled * 2:bytes_filled * 2 + 2], 16)
    return byte >> (8 - bits_filled)


def _get_char(hex_string: bytes, bytes_filled: int, bits_filled: int, shift: int):
    byte = _get_byte(hex_string, bytes_filled, bits_filled)
    byte = byte + 2 ** bits_filled + shift
    return b"%02X" % byte


def _get_string(hex_string: bytes, bytes_filled: int, bits_filled: int, shift: int):
    hex_char = _get_char(hex_string, bytes_filled, bits_filled, shift)
    return hex_string[0:bytes_filled * 2] + hex_char


def _pad10star1(hex_string: bytes, n):
    """
    Pad M with the pad10*1 padding rule to reach a length multiple of r bits

    :param hex_string: hex string to pad.
    :param n: hex length in bits (multiple of 8).

    .. code-block:: python

       >>>  _pad10star1(b'BA594E0FB9EBBD30', 8)
       b'BA594E0FB9EBBD93'
    """

    bit_length = 4 * len(hex_string)

    # Check the parameter n
    if n % 8 != 0:
        raise KeccakError("n must be a multiple of 8")

    # Check the length of the provided string
    if len(hex_string) % 2 != 0:
        # Pad with one '0' to reach correct length (don't know test vectors coding)
        hex_string += b'0'
    if bit_length > (len(hex_string) // 2 * 8):
        raise KeccakError("string is too short to contain announced bits")

    bytes_filled = bit_length // 8
    bits_filled = bit_length % 8
    l = bit_length % n
    if (n - 8) <= l <= (n - 2):
        hex_string = _get_string(hex_string, bytes_filled, bits_filled, 2**7)
    else:
        hex_string = _get_string(hex_string, bytes_filled, bits_filled, 0)
        while((8 * len(hex_string) // 2) % n < (n - 8)):
            hex_string = hex_string + b'00'
        hex_string = hex_string + b'80'

    return hex_string


def from_hex_string_to_lane(string):
    """Convert a string of bytes written in hexadecimal to a lane value"""

    # Check that the string has an even number of characters i.e. whole number of bytes
    if len(string) % 2 != 0:
        raise KeccakError("The provided string does not end with a full byte")

    # Perform the conversion
    temp = b''
    length = len(string) // 2
    for i in range(length):
        offset = (length - i - 1) * 2
        temp += string[offset:offset + 2]
    return int(temp, 16)


def from_lane_to_hex_string(lane, w):
    """Convert a lane value to a string of bytes written in hexadecimal"""

    lane_hex_b_e = ((b"%%0%dX" % (w // 4)) % lane)
    # Perform the conversion
    temp = b''
    length = len(lane_hex_b_e) // 2
    for i in range(length):
        offset = (length - i - 1) * 2
        temp += lane_hex_b_e[offset:offset + 2]
    return temp.upper()


def _convert_str_to_table(string, w, b):
    """
    Convert a string of hex-chars to its 5x5 matrix representation

    string: string of bytes of hex-coded bytes (e.g. '9A2C...')
    """

    # Check that the input paramaters are expected
    if w % 8 != 0:
        raise KeccakError("w is not a multiple of 8")

    # Each character in the string represents 4 bits.
    # The string should have exactly 'b' bits.
    if len(string) * 4 != b:
        raise KeccakError(
            "string can't be divided in 25 blocks of w "
            "bits i.e. string must have exactly b bits"
        )

    # Convert
    output = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    bits_per_char = 2 * w // 8
    for x in range(5):
        for y in range(5):
            # Each entry will have b/25=w bits.
            offset = (5 * y + x) * bits_per_char
            # Store the data into the associated word.
            hexstring = string[offset:offset + bits_per_char]
            output[x][y] = from_hex_string_to_lane(hexstring)
    return output


def _convert_table_to_str(table, w):
    """Convert a 5x5 matrix representation to its string representation"""

    # Check input format
    if w % 8 != 0:
        raise KeccakError("w is not a multiple of 8")
    if len(table) != 5 or any(len(row) != 5 for row in table):
        raise KeccakError("table must be 5x5")

    # Convert
    output = [b''] * 25
    for x in range(5):
        for y in range(5):
            output[5 * y + x] = from_lane_to_hex_string(table[x][y], w)
    output = b''.join(output).upper()
    return output
