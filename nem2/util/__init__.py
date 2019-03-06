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

from . import hashlib
from . import signature

from .abc import *
from .format import InterchangeFormat

from .stdint import *

from .documentation import doc, undoc
from .factory import defactorize
from .reactive import observable
from .reify import reify

from .identifier import generate_mosaic_id, generate_namespace_id

from .base64 import b32encode, b32decode, b64encode, b64decode
from .binascii import hexlify, unhexlify

__all__ = [
    # Modules
    'hashlib',
    'signature',

    # Models
    'ABCEnumMeta',
    'Dto',
    'Catbuffer',
    'Model',
    'Tie',
    'InterchangeFormat',
    'enum_catbuffer',
    'enum_dto',
    'enum_model',

    # DTO
    'Uint32DtoType',
    'Uint64DtoType',
    'Uint128DtoType',
    'uint64_high',
    'uint64_low',
    'uint64_to_dto',
    'dto_to_uint64',
    'uint128_high',
    'uint128_low',
    'uint128_to_dto',
    'dto_to_uint128',

    # Decorators
    'doc',
    'undoc',
    'defactorize',
    'observable',
    'reify',

    # Identifiers
    'generate_mosaic_id',
    'generate_namespace_id',

    # Text utilities
    'b32encode',
    'b32decode',
    'b64encode',
    'b64decode',
    'hexlify',
    'unhexlify',
]
