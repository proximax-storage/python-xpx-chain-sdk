"""
    util
    ====

    Generic, internal utilities for the NEM2 SDK.

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

# Modules
from . import hashlib
from . import signature

# Asynchronous
from .asynchronous import *

# Decorators
from .documentation import doc, inherit_doc, undoc
from .factory import defactorize
from .observable import observable
from .reify import reify

# DTO
from .stdint import *

# Identifiers
from .identifier import generate_mosaic_id, generate_namespace_id

# Models
from .abc import *
from .dataclasses import Field, FrozenInstanceError, InitVar, MISSING, dataclass
from .mixin import *

# Text utilities
from .base64 import b32encode, b32decode, b64encode, b64decode
from .binascii import decode_hex, encode_hex, hexlify, unhexlify

__all__ = [
    # Modules
    'hashlib',
    'signature',

    # Asynchronous
    'LoopType',
    'OptionalLoopType',
    'get_event_loop',
    'get_running_loop',

    # Decorators
    'doc',
    'inherit_doc',
    'undoc',
    'defactorize',
    'observable',
    'reify',

    # DTO
    'U8_BYTES',
    'U16_BYTES',
    'U32_BYTES',
    'U64_BYTES',
    'U128_BYTES',
    'U8DTOType',
    'U16DTOType',
    'U32DTOType',
    'U64DTOType',
    'U128DTOType',
    'u8_high',
    'u8_low',
    'u8_from_catbuffer',
    'u8_from_dto',
    'u8_to_catbuffer',
    'u8_to_dto',
    'u16_high',
    'u16_low',
    'u16_from_catbuffer',
    'u16_from_dto',
    'u16_to_catbuffer',
    'u16_to_dto',
    'u32_high',
    'u32_low',
    'u32_from_catbuffer',
    'u32_from_dto',
    'u32_to_catbuffer',
    'u32_to_dto',
    'u64_high',
    'u64_low',
    'u64_from_catbuffer',
    'u64_from_dto',
    'u64_to_catbuffer',
    'u64_to_dto',
    'u128_high',
    'u128_low',
    'u128_from_catbuffer',
    'u128_from_dto',
    'u128_to_catbuffer',
    'u128_to_dto',

    # Identifiers
    'generate_mosaic_id',
    'generate_namespace_id',

    # Models
    'Field',
    'FrozenInstanceError',
    'InitVar',
    'MISSING',
    'dataclass',
    'EnumMixin',
    'IntMixin',
    'U8Mixin',
    'U16Mixin',
    'U32Mixin',
    'U64Mixin',
    'U128Mixin',
    'AbstractMethodError',
    'Catbuffer',
    'DTO',
    'Model',

    # Text utilities
    'b32encode',
    'b32decode',
    'b64encode',
    'b64decode',
    'decode_hex',
    'encode_hex',
    'hexlify',
    'unhexlify',
]
