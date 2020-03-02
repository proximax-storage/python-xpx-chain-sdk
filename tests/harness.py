"""
    harness
    =======

    Simple test harness to simplify testing asynchronous code.

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

import aiohttp
import asyncio
import collections
from collections import abc
import contextlib
import copy
import dataclasses
import datetime
import enum
import functools
import inspect
import json
import math
import requests
import string
import struct
import typing
import unittest
import warnings
import websockets

from xpxchain import client
from xpxchain import models
from xpxchain import util
from . import aitertools
from . import responses

# HELPERS


def get_argnames(func):
    """Get the argument names from a function."""

    # Get all positional arguments in __init__, including named
    # and named optional arguments. `co_varnames` stores all argument
    # names (including local variable names) in order, starting with
    # function arguments, so only grab `co_argcount` varnames.
    code = getattr(func, '__func__', func).__code__
    argcount = code.co_argcount
    return code.co_varnames[:argcount]


def setattr_default(obj, name, value):
    """Setdefault except for object attributes."""

    if name not in obj.__dict__:
        setattr(obj, name, value)


def add_tests(cls, tests, attrs, prefix):
    """Add tests to a class from a list of names and attrs passed to the class."""

    for test in tests:
        if attrs.get(test, True):
            name = f'test_{test}'
            func = globals()[f'{prefix}_test_{test}']
            setattr_default(cls, name, func)


def add_format_tests(cls, tests, attrs, prefix):
    """Add tests which require extra format data to be provided."""

    for test in tests:
        if test in attrs:
            name = f'test_{test}'
            func = globals()[f'{prefix}_test_{test}']
            setattr_default(cls, name, func)


def is_exception(obj):
    """Check if an object is an exception."""
    return inspect.isclass(obj) and issubclass(obj, Exception)


# TEST CASE


class TestCase(unittest.TestCase):
    """Asynchronous-aware test case suite."""

    def __init__(self, methodName='runTest', loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self._cache = {}
        super().__init__(methodName=methodName)

    def coroutine_function_decorator(self, func):
        def wrapper(*args, **kw):
            return self.loop.run_until_complete(func(*args, **kw))
        return wrapper

    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)
        if asyncio.iscoroutinefunction(attr):
            if item not in self._cache:
                self._cache[item] = self.coroutine_function_decorator(attr)
            return self._cache[item]
        return attr


# ENUM TEST CASE

ENUM_TESTS = [
    'description',
    'value',
    'repr',
    'str',
    'eq',
    'ord',
]


def enum_test_description(self):
    """Test the enum description method."""

    for enumeration, description in zip(self.enums, self.descriptions):
        self.assertTrue(enumeration.description().startswith(description))


def enum_test_value(self):
    """Test the enum value property."""

    for enumeration, value in zip(self.enums, self.values):
        self.assertEqual(value, enumeration.value)


def enum_test_repr(self):
    """Test the enum __repr__ method."""

    clsname = self.type.__name__
    for enumeration in self.enums:
        expected = f'<{clsname}.{enumeration.name}: {repr(enumeration.value)}>'
        self.assertEqual(repr(enumeration), expected)


def enum_test_str(self):
    """Test the enum __str__ method."""

    clsname = self.type.__name__
    for enumeration in self.enums:
        self.assertEqual(str(enumeration), f'{clsname}.{enumeration.name}')


def enum_test_eq(self):
    """Test the enum __eq__ method."""

    enums = list(set(self.enums))
    for index, enumeration in enumerate(enums):
        self.assertEqual(enumeration, enums[index])
        for other in enums[index + 1:]:
            self.assertNotEqual(enumeration, other)


def enum_test_ord(self):
    """Test the enum __lt__ method."""

    enums = sorted(set(self.enums))
    for index, enumeration in enumerate(enums):
        self.assertLessEqual(enumeration, enums[index])
        for other in enums[index + 1:]:
            self.assertLess(enumeration, other)


def enum_test_dto(self):
    """Test the conversion to and from DTO."""

    for enumeration, dto in zip(self.enums, self.dto):
        self.assertEqual(dto, enumeration.to_dto())


def enum_test_catbuffer(self):
    """Test the conversion to and from catbuffer."""

    for enumeration, catbuffer in zip(self.enums, self.catbuffer):
        self.assertEqual(catbuffer, enumeration.to_catbuffer())


def enum_setup_fn(attrs):
    """Generate the setup function for enums."""

    assert len(attrs['enums']) == len(attrs['descriptions'])
    assert len(attrs['enums']) == len(attrs['values'])
    assert 'dto' not in attrs or len(attrs['enums']) == len(attrs['dto'])
    assert 'catbuffer' not in attrs or len(attrs['enums']) == len(attrs['catbuffer'])
    for test in attrs.get('custom', ()):
        inputs = test.get('inputs') or attrs['enums']
        results = test.get('results') or attrs['enums']
        assert len(inputs) == len(results)

    def func(self):
        self.type = attrs['type']
        self.enums = attrs['enums']
        self.values = attrs['values']
        self.descriptions = attrs['descriptions']
        self.dto = attrs.get('dto')
        self.catbuffer = attrs.get('catbuffer')
        self.extras = attrs.get('extras', {})

    return func


def enum_add_custom_tests(cls, tests):
    """Add custom tests, which provide a name, callback, and expected results."""

    def decorator(callback, inputs, results):
        def func(self):
            tests = zip(inputs or self.enums, results or self.enums)
            for in_value, out_value in tests:
                if is_exception(out_value):
                    with self.assertRaises(out_value):
                        callback(self, in_value)
                else:
                    self.assertEqual(out_value, callback(self, in_value))
        return func

    for test in tests:
        callback = test['callback']
        inputs = test.get('inputs')
        results = test.get('results')
        setattr_default(cls, test['name'], decorator(callback, inputs, results))


def enum_test_case(attrs):
    """
    Decorator that auto-generates the test suite from model data.

    Auto-generates and binds a model to the class, and then defines
    tests automatically from the bound data.

    Available tests are:
        test_description
        test_value
        test_repr
        test_str
        test_eq
        test_ord
    """

    def decorator(cls):
        setattr_default(cls, 'setUp', enum_setup_fn(attrs))
        add_tests(cls, ENUM_TESTS, attrs, prefix='enum')
        add_format_tests(cls, ['catbuffer', 'dto'], attrs, prefix='enum')
        enum_add_custom_tests(cls, attrs.get('custom', ()))
        return cls

    return decorator


# MODEL TEST CASE

MODEL_TESTS = [
    'init',
    'frozen',
    'slots',
    'eq',
    'repr',
    'str',
    'copy',
    'deepcopy',
    'replace',
    'asdict',
    'astuple',
    'fields',
]


def model_test_init(self):
    """Test if the model fields are properly set from the initializer."""

    if dataclasses.is_dataclass(self.type):
        for name, value in self.data.items():
            self.assertEqual(getattr(self.model, name), value)
    elif issubclass(self.type, abc.Sequence):
        self.assertEqual(tuple(self.data), tuple(self.model))
    elif issubclass(self.type, abc.Mapping):
        self.assertEqual(dict(self.data), dict(self.model))
    else:
        raise NotImplementedError


def model_test_frozen(self):
    """Test the model's attributes are frozen."""

    if dataclasses.is_dataclass(self.type):
        fields = [i.name for i in dataclasses.fields(self.model)]
        for field in fields:
            value = getattr(self.model, field)
            with self.assertRaises(dataclasses.FrozenInstanceError):
                setattr(self.model, field, value)
    elif issubclass(self.type, abc.Sequence):
        for index, value in enumerate(self.model):
            with self.assertRaises(TypeError):
                self.model[index] = value
    elif issubclass(self.type, abc.Mapping):
        for key, value in self.model.items():
            with self.assertRaises(TypeError):
                self.model[key] = value
    else:
        raise NotImplementedError


def model_test_slots(self):
    """Test if the model has slots, and therefore is efficiently stored."""

    with self.assertRaises((TypeError, AttributeError)):
        self.model.__dict__


def next_byte_power(value):
    """Calculate the next power of 2 from a value."""

    char_bit = 8
    byte_length = int(math.ceil(value.bit_length() / char_bit))
    return 2 ** (char_bit * byte_length)


def bitwise_not(value):
    """Calculate bitwise not of value as an unsigned integer."""
    # We want to get 1 - next power of 2, so we can get the 0xFF bit pattern.
    # We can then use xor to invert all the bits in the input.
    # We want to use value + 1, since if the value is, say, 256, it requires
    # 9 bits of storage, not 8.
    max_int = next_byte_power(value + 1) - 1
    return max_int ^ value


def model_test_eq(self):
    """Test the model __eq__ method."""

    def permute_sequence(data):
        return type(data)([permute(i) for i in data])

    def permute_mapping(data):
        return type(data)([(k, permute(v)) for k, v in data.items()])

    def permute(value):
        # In bytes and strings, the first 2 values may be used as a
        # sentinel. We want to keep those the same. 1 for bytes,
        # 2 for hex.
        if hasattr(value, '_permute_'):
            # Specialized method for testing.
            return value._permute_(permute)
        elif isinstance(value, enum.Enum):
            return value
        elif isinstance(value, datetime.datetime):
            timestamp = value.replace(tzinfo=datetime.timezone.utc).timestamp()
            negated = bitwise_not(int(timestamp))
            utc = datetime.datetime.fromtimestamp(negated, datetime.timezone.utc)
            return utc.replace(tzinfo=None)
        elif isinstance(value, int):
            return bitwise_not(value)
        elif isinstance(value, (bytes, bytearray)):
            return value[:1] + value[-2::-1]
        elif isinstance(value, str):
            return value[:2] + value[-3::-1]
        elif isinstance(value, abc.Sequence):
            return permute_sequence(value)
        elif isinstance(value, abc.Mapping):
            return permute_mapping(value)
        elif dataclasses.is_dataclass(value):
            fields = get_argnames(value.__init__)[1:]
            asdict = {i: getattr(value, i) for i in fields}
            return type(value)(**permute_mapping(asdict))
        return value

    m1 = copy.copy(self.model)
    m2 = copy.copy(self.model)
    m3 = permute(self.model)

    self.assertTrue(m1 == m1)
    self.assertTrue(m1 == m2)
    self.assertFalse(m1 == m3)
    self.assertTrue(m2 == m2)
    self.assertFalse(m2 == m3)
    self.assertTrue(m3 == m3)


def model_test_repr(self):
    """Test the model __repr__ method."""

    name = type(self.model).__name__
    if dataclasses.is_dataclass(self.type):
        fields = [i.name for i in dataclasses.fields(self.model)]
        values = [getattr(self.model, i) for i in fields]
        tupletype = collections.namedtuple(name, fields)
        self.assertEqual(repr(tupletype(*values)), repr(self.model))
    elif issubclass(self.type, abc.Sequence):
        self.assertEqual(repr(self.model), f'{name}({repr(list(self.model))})')
    elif issubclass(self.type, abc.Mapping):
        self.assertEqual(repr(self.model), f'{name}({repr(dict(self.model))})')
    else:
        raise NotImplementedError


def model_test_str(self):
    """Test the model __str__ method."""
    self.assertEqual(str(self.model), repr(self.model))


def model_test_copy(self):
    """Test the model __copy__ method."""
    self.assertEqual(self.model, copy.copy(self.model))


def model_test_deepcopy(self):
    """Test the model __deepcopy__ method."""
    self.assertEqual(self.model, copy.deepcopy(self.model))


def model_test_replace(self):
    """Test the model replace method."""
    self.assertEqual(self.model, self.model.replace())


def model_test_asdict(self):
    """Test the model asdict method."""

    asdict = self.model.asdict(recurse=False)
    if dataclasses.is_dataclass(self.type):
        fields = [i.name for i in dataclasses.fields(self.model)]
        self.assertIsInstance(asdict, dict)
        self.assertEqual(len(asdict), len(fields))
        for field in fields:
            self.assertEqual(asdict[field], getattr(self.model, field))
    elif issubclass(self.type, abc.Mapping):
        for key, value in self.model.items():
            self.assertEqual(asdict[key], value)
    else:
        raise NotImplementedError


def model_test_astuple(self):
    """Test the model astuple method."""

    astuple = self.model.astuple(recurse=False)
    if dataclasses.is_dataclass(self.type):
        fields = [i.name for i in dataclasses.fields(self.model)]
        self.assertIsInstance(astuple, tuple)
        self.assertEqual(len(astuple), len(fields))
        for index, field in enumerate(fields):
            self.assertEqual(astuple[index], getattr(self.model, field))
    elif issubclass(self.type, abc.Mapping):
        self.assertEqual(astuple, tuple(self.model.values()))
    elif issubclass(self.type, abc.Sequence):
        self.assertEqual(astuple, tuple(self.model))
    else:
        raise NotImplementedError


def model_test_fields(self):
    """Test the model fields method."""

    fields = self.model.fields()
    self.maxDiff = 2048
    self.assertIsInstance(fields, tuple)
    self.assertEqual(fields, dataclasses.fields(self.model))


def model_test_dto(self):
    """Test the conversion to and from DTO."""

    nt = self.network_type
    self.maxDiff = 2048
    self.assertEqual(self.model.to_dto(nt), self.dto)
    self.assertEqual(self.model, self.type.create_from_dto(self.dto, nt))


def model_test_catbuffer(self):
    """Test the conversion to and from catbuffer."""

    nt = self.network_type
    encoded = util.encode_hex(self.catbuffer)
    decoded = util.decode_hex(self.catbuffer)
    self.maxDiff = 2048
    self.assertEqual(util.hexlify(self.model.to_catbuffer(nt, fee_strategy=util.FeeCalculationStrategy.ZERO)), encoded)
    self.assertEqual(self.model, self.type.create_from_catbuffer(decoded, nt))


def load_model(model_type, data):
    """Generate the model from the provided data."""

    if issubclass(model_type, (abc.Sequence, abc.Mapping)):
        return model_type(data)
    return model_type(**data)


def model_setup_fn(attrs):
    """Generate the setup function for models."""

    model = load_model(attrs['type'], attrs['data'])

    def func(self):
        self.model = model
        self.type = attrs['type']
        self.data = attrs['data']
        self.network_type = attrs['network_type']
        self.dto = attrs.get('dto')
        self.catbuffer = attrs.get('catbuffer')
        self.extras = attrs.get('extras', {})

    return func


def model_test_case(attrs):
    """
    Decorator that auto-generates the test suite from model data.

    Auto-generates and binds a model to the class, and then defines
    tests automatically from the bound data.

    Available tests are:
        test_init
        test_frozen
        test_slots
        test_eq
        test_repr
        test_str
        test_copy
        test_deepcopy
        test_replace
        test_asdict
        test_astuple
        test_fields
    """

    def decorator(cls):
        setattr_default(cls, 'setUp', model_setup_fn(attrs))
        add_tests(cls, MODEL_TESTS, attrs, prefix='model')
        add_format_tests(cls, ['catbuffer', 'dto'], attrs, prefix='model')
        return cls

    return decorator


# TRANSACTION TEST CASE

TRANSACTION_TESTS = MODEL_TESTS + [
    'to_aggregate',
    'sign_with',
]

transaction_test_init = model_test_init
transaction_test_frozen = model_test_frozen
transaction_test_slots = model_test_slots
transaction_test_eq = model_test_eq
transaction_test_repr = model_test_repr
transaction_test_str = model_test_str
transaction_test_copy = model_test_copy
transaction_test_deepcopy = model_test_deepcopy
transaction_test_replace = model_test_replace
transaction_test_asdict = model_test_asdict
transaction_test_astuple = model_test_astuple
transaction_test_fields = model_test_fields
transaction_test_dto = model_test_dto
transaction_test_catbuffer = model_test_catbuffer


def transaction_test_to_aggregate(self):
    """Test embedding the transaction with a signer."""

    # Get the signer
    private_key = self.extras['private_key']
    signer = models.Account.create_from_private_key(private_key, self.network_type)

    # Convert to inner transaction and serialize.
    inner = self.model.to_aggregate(signer.public_account)
    catbuffer = inner.to_catbuffer(fee_strategy=self.extras['fee_strategy'])
    self.maxDiff = 2048
    self.assertEqual(util.hexlify(catbuffer), self.extras['embedded'])

    with self.assertRaises(TypeError):
        inner.__dict__


def transaction_test_sign_with(self):
    """Test transaction signing with a signer."""

    # Get the signer
    private_key = self.extras['private_key']
    signer = models.Account.create_from_private_key(private_key, self.network_type)

    # Sign transaction and check signed data.
    signed_transaction = self.model.sign_with(signer, self.extras['gen_hash'], fee_strategy=self.extras['fee_strategy'])
    self.maxDiff = 2048
    self.assertEqual(signed_transaction.payload, self.extras['signed']['payload'])
    self.assertEqual(signed_transaction.hash, self.extras['signed']['hash'])
    self.assertEqual(signed_transaction.signer, signer.public_key)
    self.assertEqual(signed_transaction.type, self.model.type)
    self.assertEqual(signed_transaction.network_type, self.network_type)


def transaction_test_case(attrs):
    """
    Decorator that auto-generates the test suite from transaction data.

    Auto-generates and binds a model to the class, and then defines
    tests automatically from the bound data. Supports all tests from
    model data, including a few more.

    Available tests are:
        test_to_aggregate
        test_sign_with
    """

    def decorator(cls):
        setattr_default(cls, 'setUp', model_setup_fn(attrs))
        add_tests(cls, TRANSACTION_TESTS, attrs, prefix='transaction')
        add_format_tests(cls, ['catbuffer', 'dto'], attrs, prefix='transaction')
        return cls

    return decorator


# HTTP TEST CASE


def make_request(http, method, params):
    """Make HTTP request from test data."""

    callback = getattr(http, method)
    return callback(*params)


def http_test(cls, sync_client, async_client, test):
    """Add a custom test for a mocked HTTP response."""

    @async_test(sync_client, async_client)
    async def func(self, data, await_cb, with_cb):
        async with with_cb(data(responses.ENDPOINT)) as http:
            request = make_request(http, test['method'], test['params'])
            response = await await_cb(request)
            for validator in test['validation']:
                self.assertEqual(*validator(response))

    func.__name__ = test['name']
    setattr_default(cls, test['name'], func)


def http_test_case(attrs):
    """Decorator that auto-generates HTTP test cases from attrs."""

    sync_client, async_client = attrs['clients']

    def decorator(cls):
        for test in attrs['tests']:
            http_test(cls, sync_client, async_client, test)
        return cls

    return decorator


# MOCKED HTTP TEST CASE


def mocked_http_test(cls, network_type, sync_client, async_client, test):
    """Add a custom test for a mocked HTTP response."""

    sync_data = (sync_client, requests)
    async_data = (async_client, aiohttp)
    network_response = responses.NETWORK_TYPE[network_type.name]
    method = test['method']
    params = test['params']
    error = test.get('error')

    @async_test(sync_data, async_data)
    async def func(self, data, await_cb, with_cb):
        async with with_cb(data[0](responses.ENDPOINT)) as http:
            # Set the network type, so we can make the actual request.
            with data[1].default_response(200, **network_response):
                await await_cb(http.network_type)

            # Make the actual request and validate the response.
            with data[1].default_response(200, **test['response']):
                if error is not None:
                    with self.assertRaises(error):
                        await await_cb(make_request(http, method, params))
                else:
                    response = await await_cb(make_request(http, method, params))
                    for validator in test.get('validation', ()):
                        self.assertEqual(*validator(response))

    func.__name__ = test['name']
    setattr_default(cls, test['name'], func)


def mocked_http_test_case(attrs):
    """Decorator that auto-generates mocked HTTP test cases from attrs."""

    sync_client, async_client = attrs['clients']
    network_type = attrs['network_type']

    def decorator(cls):
        for test in attrs['tests']:
            mocked_http_test(cls, network_type, sync_client, async_client, test)
        return cls

    return decorator


# LISTENER TEST


def listener_test(cls, test):
    """Add a custom test for a listener response."""

    async def func(self):
        async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
            # Subscribe to the desired channels.
            for subscription in test['subscriptions']:
                await getattr(listener, subscription)()

            # Iterate over all the messages.
            count = len(test['validation'])
            messages = [i async for i in aitertools.aslice(listener, count)]
            for message, validators in zip(messages, test['validation']):
                for validator in validators:
                    self.assertEqual(*validator(message))

    func.__name__ = test['name']
    setattr_default(cls, test['name'], func)


def listener_test_case(attrs):
    """Decorator that auto-generates listener test cases from attrs."""

    def decorator(cls):
        for test in attrs['tests']:
            listener_test(cls, test)
        return cls

    return decorator


# MOCKED LISTENER TEST


def mocked_listener_test(cls, test):
    """Add a custom test for a mocked listener response."""

    async def func(self):
        async with client.Listener(f'{responses.ENDPOINT}/ws') as listener:
            # Get the UID for the websockets client..
            with websockets.default_response([json.dumps({'uid': test['uid']})]):
                self.assertEqual(await listener.uid, test['uid'])

            # Subscribe to the desired channels.
            for subscription in test['subscriptions']:
                await getattr(listener, subscription)()

            # Iterate over all the messages.
            with websockets.default_response(test['response']):
                count = len(test['validation'])
                messages = [i async for i in aitertools.aslice(listener, count)]
                for message, validators in zip(messages, test['validation']):
                    for validator in validators:
                        self.assertEqual(*validator(message))

    func.__name__ = test['name']
    setattr_default(cls, test['name'], func)


def mocked_listener_test_case(attrs):
    """Decorator that auto-generates mocked listener test cases from attrs."""

    def decorator(cls):
        for test in attrs['tests']:
            mocked_listener_test(cls, test)
        return cls

    return decorator


# ASYNC TEST


def async_test(sync_data, async_data):
    """
    Generate synchronous and asynchronous tests from a single function.

    :param sync_data: Data to be passed to the synchronous test case.
    :param async_data: Data to be passed to the asynchronous test case.
    """

    def decorator(f):
        async def sync_cb(x):
            return x

        async def async_cb(x):
            return await x

        @contextlib.asynccontextmanager
        async def sync_with(x):
            with x as y:
                yield y

        @contextlib.asynccontextmanager
        async def async_with(x):
            async with x as y:
                yield y

        @functools.wraps(f)
        async def wrapped(self):
            await f(self, sync_data, sync_cb, sync_with)
            await f(self, async_data, async_cb, async_with)

        return wrapped

    return decorator

# IGNORE WARNING TEST


def ignore_warnings_test(test):
    """Wrap a function body in a warnings.catch_warnings() block."""

    def wrapper(self, *args, **kwds):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test(self, *args, **kwds)

    return wrapper


# RANDOM

with contextlib.suppress(ImportError):
    # Check we can import all our dependencies and generate the decorators.
    from collections import deque
    import logging
    import os.path
    import random
    import rstr
    import sys

    # CONFIG
    DEFAULT_CALLS = 20
    DEFAULT_MIN_STRLEN = 5
    DEFAULT_MAX_STRLEN = 40
    DEFAULT_MIN_SEQLEN = 1
    DEFAULT_MAX_SEQLEN = 10
    DEFAULT_MIN_MAPLEN = 1
    DEFAULT_MAX_MAPLEN = 10

    # TYPE HINTS
    # Define type hints so we can generate random data within the expected
    # bounds.
    U8 = typing.TypeVar('U8', bound=int)
    U16 = typing.TypeVar('U16', bound=int)
    U32 = typing.TypeVar('U32', bound=int)
    U64 = typing.TypeVar('U64', bound=int)
    U128 = typing.TypeVar('U128', bound=int)
    I8 = typing.TypeVar('I8', bound=int)
    I16 = typing.TypeVar('I16', bound=int)
    I32 = typing.TypeVar('I32', bound=int)
    I64 = typing.TypeVar('I64', bound=int)
    I128 = typing.TypeVar('I128', bound=int)
    F32 = typing.TypeVar('F32', bound=float)
    F64 = typing.TypeVar('F64', bound=float)

    class BytesPattern(bytes):
        """Indicates you want to match against a bytes regular expression."""

    class StrPattern(str):
        """Indicates you want to match against a str regular expression."""

    def boolgen():
        """Define a new generator for boolean values."""

        def generator() -> bool:
            return random.choice([True, False])

        return generator

    def intgen(min_value: int = -sys.maxsize, max_value: int = sys.maxsize):
        """Define a new generator for integral values (inclusive)."""

        def generator() -> int:
            return random.randint(min_value, max_value)

        return generator

    def structgen(bits: int, format: str):
        """Generate data from random bytes."""

        assert struct.calcsize(f'<{format}') == bits // 8
        nbytes = bits // 8

        def generator():
            data = int.to_bytes(random.getrandbits(bits), nbytes, 'little')
            return struct.unpack(f'<{format}', data)[0]

        return generator

    def floatgen(
        min_magnitude: float = 1e-7,
        max_magnitude: float = 1e10,
        positive: bool = False,
        **kwds
    ):
        """
        Define a new generator for floating-point values.
        Chance of 0 scales with the size of the range.
        """

        next_pos = boolgen()
        zero_bits = kwds.get('zero_bits', int(math.log2(max_magnitude - min_magnitude)))

        def generator() -> float:
            # Floats have a symmetric range for both positive and negative
            # values due to dedicated sign bit in IEEE754.
            if random.getrandbits(zero_bits) == 0:
                return 0.0
            elif positive or next_pos():
                return random.uniform(min_magnitude, max_magnitude)
            return random.uniform(-min_magnitude, -max_magnitude)

        return generator

    def regen(pattern: str):
        """Define a new generator based off a regular expression."""

        def generator() -> str:
            return rstr.xeger(pattern)

        return generator

    def lettergen(letters: str = string.printable, **kwds):
        """Define new letter-based string generator."""

        fixed_length = kwds.get('fixed_length')
        if fixed_length is not None:
            min_length = fixed_length
            max_length = fixed_length
        else:
            min_length = kwds.get('min_length', DEFAULT_MIN_STRLEN)
            max_length = kwds.get('max_length', DEFAULT_MAX_STRLEN)

        def generator() -> str:
            length = random.randint(min_length, max_length)
            return ''.join([random.choice(letters) for i in range(length)])

        return generator

    def strgen(**kwds):
        """Define a new generator for str."""

        if 'pattern' in kwds:
            return regen(kwds.pop('pattern'), **kwds)
        return lettergen(**kwds)

    def bytesgen(letters: bytes = bytes(range(256)), **kwds):
        """Define a new generator for bytes."""

        fixed_length = kwds.get('fixed_length')
        if fixed_length is not None:
            min_length = fixed_length
            max_length = fixed_length
        else:
            min_length = kwds.get('min_length', DEFAULT_MIN_STRLEN)
            max_length = kwds.get('max_length', DEFAULT_MAX_STRLEN)

        def generator() -> bytes:
            length = random.randint(min_length, max_length)
            return bytes([random.choice(letters) for i in range(length)])

        return generator

    def enumgen(type: typing.Type[enum.Enum]):
        """Randomly generate variants of an enumeration."""

        members = list(type.__members__.values())

        def generator() -> enum.Enum:
            return random.choice(members)

        return generator

    _T = typing.TypeVar('_T')
    _U = typing.TypeVar('_U')

    def _generator(type: typing.Type, kwds: typing.Optional[dict] = None):
        """Convert a type annotation and keyword arguments to a new generator."""

        # First, try an enumeration.
        if inspect.isclass(type) and issubclass(type, enum.Enum):
            return enumgen(type)

        # Next, try pre-defined generators.
        with contextlib.suppress(KeyError):
            return GENERATORS[type]

        # Try a sequence or mapping type. This will fail for TypeVars and Unions,
        # raising a KeyError by design. Ignore that.
        kwds = kwds or {}
        with contextlib.suppress(AttributeError):
            origin = type.__origin__
            args = type.__args__
            return PROTO_GENERATORS[origin](*args, **kwds)

        # Go to our fallback.
        return PROTO_GENERATORS[type](**kwds)

    def _seqgen(value_type: typing.Type[_T], **kwds):
        """Generate sequence type with defined value type."""

        # Process our arguments for the value type generator.
        valuegen = _generator(value_type, kwds.get('value'))

        # Process our arguments for the sequence generator.
        fixed_length = kwds.get('fixed_length')
        if fixed_length is not None:
            min_length = fixed_length
            max_length = fixed_length
        else:
            min_length = kwds.get('min_length', DEFAULT_MIN_SEQLEN)
            max_length = kwds.get('max_length', DEFAULT_MAX_SEQLEN)

        def generator() -> typing.Sequence[_T]:
            length = random.randint(min_length, max_length)
            return [valuegen() for _ in range(length)]

        return generator

    def _mapgen(key_type: typing.Type[_T], value_type: typing.Type[_U], **kwds):
        """Generate mapping type with defined key/value types."""

        # Process our arguments for the key and value type generators.
        keygen = _generator(key_type, kwds.get('key'))
        valuegen = _generator(value_type, kwds.get('value'))

        # Process our arguments for the sequence generator.
        fixed_length = kwds.get('fixed_length')
        if fixed_length is not None:
            min_length = fixed_length
            max_length = fixed_length
        else:
            min_length = kwds.get('min_length', DEFAULT_MIN_SEQLEN)
            max_length = kwds.get('max_length', DEFAULT_MAX_SEQLEN)

        def generator() -> typing.Mapping[_T, _U]:
            length = random.randint(min_length, max_length)
            return {keygen(): valuegen() for _ in range(length)}

        return generator

    def listgen(value_type: typing.Type[_T], **kwds):
        """Generate sequence of values as list."""

        seq_generator = _seqgen(value_type, **kwds)

        def generator() -> typing.List[_T]:
            return list(seq_generator())

        return generator

    def setgen(value_type: typing.Type[_T], **kwds):
        """Generate sequence of values as set."""

        seq_generator = _seqgen(value_type, **kwds)

        def generator() -> typing.Set[_T]:
            return set(seq_generator())

        return generator

    def frozensetgen(value_type: typing.Type[_T], **kwds):
        """Generate sequence of values as frozenset."""

        seq_generator = _seqgen(value_type, **kwds)

        def generator() -> typing.FrozenSet[_T]:
            return frozenset(seq_generator())

        return generator

    def dequegen(value_type: typing.Type[_T], **kwds):
        """Generate sequence of values as deque."""

        seq_generator = _seqgen(value_type, **kwds)

        def generator() -> typing.Deque[_T]:
            return deque(seq_generator())

        return generator

    def dictgen(key_type: typing.Type[_T], value_type: typing.Type[_U], **kwds):
        """Generate mapping of keys and values as dict."""

        map_generator = _mapgen(key_type, value_type, **kwds)

        def generator() -> typing.Dict[_T, _U]:
            return dict(map_generator())

        return generator

    PROTO_GENERATORS = {
        bool: boolgen,
        int: intgen,
        float: floatgen,
        str: strgen,
        bytes: bytesgen,
        list: listgen,
        set: setgen,
        frozenset: frozensetgen,
        deque: dequegen,
        dict: dictgen,
    }

    GENERATORS = {
        # INT
        U8: intgen(0, (1 << 8) - 1),
        U16: intgen(0, (1 << 16) - 1),
        U32: intgen(0, (1 << 32) - 1),
        U64: intgen(0, (1 << 64) - 1),
        U128: intgen(0, (1 << 128) - 1),
        I8: intgen(-(1 << 7), (1 << 7) - 1),
        I16: intgen(-(1 << 15), (1 << 15) - 1),
        I32: intgen(-(1 << 31), (1 << 31) - 1),
        I64: intgen(-(1 << 63), (1 << 63) - 1),
        I128: intgen(-(1 << 127), (1 << 127) - 1),

        # FLOAT
        F32: structgen(32, 'f'),
        F64: structgen(64, 'd'),
    }

    INITIALIZED_LOGGER = False

    def log_error(error, testname, arguments, exc_info):
        """Log error, and if not present, seed."""

        global INITIALIZED_LOGGER
        testdir = '.test_harness'

        if not os.path.exists(testdir):
            os.mkdir(testdir)
        if not INITIALIZED_LOGGER:
            now = datetime.datetime.now()
            strtime = now.strftime("%Y-%m-%d-%H-%M-%S")
            logging.basicConfig(filename=f'{testdir}/random-{strtime}.log')
            INITIALIZED_LOGGER = True
            with open(f'{testdir}/random-{strtime}.seed', 'w') as f:
                f.write(str(random.getstate()))

        argstr = ', '.join(f'{k}={v!r}' for k, v in arguments.items())
        logging.error(
            f'Exception in randomly-generated unittest'
            f' {testname}, arguments were: ({argstr})',
            exc_info=exc_info
        )

    def randomize_function(f, gv, lv, **kwds):
        """Determine the type signature of the function and provide random data."""

        # Unwrap our annotations to determine our argument types.
        calls = kwds.get('calls', DEFAULT_CALLS)
        args = f.__annotations__.copy()
        args.pop('self', None)
        args.pop('return', None)
        args = {k: eval(v, gv, lv) if isinstance(v, str) else v for k, v in args.items()}
        generators = {n: _generator(t, kwds.get(n)) for n, t in args.items()}

        @functools.wraps(f)
        def test(self):
            for _ in range(calls):
                arguments = {k: v() for k, v in generators.items()}
                try:
                    f(self, **arguments)
                except Exception as error:
                    testname = f'{self.__class__.__name__}.{f.__name__}'
                    exc_info = sys.exc_info()
                    log_error(error, testname, arguments, exc_info)
                    raise

        return test

    def randomize_kwds(gv, lv, kwds):
        """Generator a function decorator with the bound keywords."""

        def decorator(f):
            return randomize_function(f, gv, lv, **kwds)

        return decorator

    def randomize(*args, **kwds):
        """Randomize arguments to a function call."""

        # Get global/local vars to evaluate forward refs.
        frame = inspect.stack()[1].frame
        gv = frame.f_globals
        lv = frame.f_locals

        # Process our arguments.
        if len(args) == 1 and callable(args[0]) and not kwds:
            return randomize_function(args[0], gv, lv)
        elif len(args):
            raise ValueError('randomize does not support positional arguments.')
        return randomize_kwds(gv, lv, kwds)
