"""
    aitertools
    ==========

    Itertools for asynchronous operations.

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

import sys


async def aenumerate(aiterable):
    """`enumerate` for asynchronous generators."""

    n = 0
    async for value in aiterable:
        yield (n, value)
        n += 1


async def aslice(aiterable, *args):
    """`islice` for asynchronous generators."""

    # Normalize the input arguments.
    slc = slice(*args)
    start = slc.start or 0
    stop = slc.stop or sys.maxsize
    assert slc.step is None or slc.step == 1

    async for (index, value) in aenumerate(aiterable):
        if index < start:
            continue
        elif index >= stop:
            break
        yield value
