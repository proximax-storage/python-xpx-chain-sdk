"""
    asyncio
    =======

    Asynchronous utilities.

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
import asyncio
import typing

__all__ = [
    'LoopType',
    'OptionalLoopType',
    'get_event_loop',
    'get_running_loop',
]

LoopType = asyncio.AbstractEventLoop
OptionalLoopType = typing.Optional[LoopType]


def get_event_loop(loop: OptionalLoopType = None) -> LoopType:
    """Get event loop."""

    if loop is None:
        loop = asyncio.get_event_loop()
    return loop


def get_running_loop(loop: OptionalLoopType = None) -> LoopType:
    """Get running event loop."""

    loop = get_event_loop(loop)
    if not loop.is_running():
        raise RuntimeError("No running event loop.")
    return loop
