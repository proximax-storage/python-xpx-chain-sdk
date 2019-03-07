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

import asyncio
import unittest


class TestCase(unittest.TestCase):

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


CACHE = {}

def create(qualname, sync_cls, async_cls):
    """Generate synchronous and asynchronous tests from a single function."""

    def decorator(f):
        assert f.__name__ == 'test'

        async def sync_value(x):
            return x

        async def async_value(x):
            return await x

        async def sync_wrap(self):
            return await f(self, sync_cls, sync_value)

        async def async_wrap(self):
            return await f(self, async_cls, async_value)

        CACHE[qualname] = sync_wrap, async_wrap

    return decorator


def new_sync(qualname):
    """Implement the synchronous test case."""

    return CACHE[qualname][0]


def new_async(qualname):
    """Implement the asynchronous test case."""

    return CACHE[qualname][1]
