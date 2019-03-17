"""
    from_coroutine
    ==============

    RxPy extension to generate an observable from a coroutine.

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
import rx
from rx.internal import extensionclassmethod


def from_coroutine(cls, coroutine, scheduler=None, loop=None):
    """
    Generate observable from an asynchronous coroutine.

    :param coroutine: Coroutine to wrap as observable.
    :param scheduler: (Optional) scheduler to determine the event loop.
    :param loop: (Optional) Event loop. Has higher precedence than scheduler.
    """

    # Get the current event loop.
    if loop is None:
        loop = asyncio.get_event_loop()
    elif scheduler is not None:
        loop = scheduler.loop

    task = loop.create_task(coroutine)
    return cls.from_future(task)


extensionclassmethod(rx.AnonymousObservable)(from_coroutine)
extensionclassmethod(rx.Observable)(from_coroutine)
