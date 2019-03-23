"""
    from_async_iterable
    ===================

    RxPy extension to generate an observable from an async iterable.

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


def from_async_iterable(cls, asyncgen, scheduler=None, loop=None):      # noqa: C901
    """
    Generate observable from an asynchronous iterable.

    :param asyncgen: Asynchronous iterable to wrap as observable.
    :param scheduler: (Optional) scheduler to determine the event loop.
    :param loop: (Optional) Event loop. Has higher precedence than scheduler.
    """

    # Get the current event loop.
    if loop is None:
        loop = asyncio.get_event_loop()
    elif scheduler is not None:
        loop = scheduler.loop

    def subscribe(observer):
        async def worker(aiter):
            """Worker to process all the items and create a coroutine."""

            # Only call __aiter__ if the type doesn't implement
            # __anext__, to avoid infinite recursion.
            if not hasattr(aiter, '__anext__'):
                aiter = aiter.__aiter__()

            # Simulate an `async for` loop, using `__anext__`. This
            # is to avoid recursively calling `__aiter__`, which is
            # what happens when we wrap `__aiter__` into an `Observable`.
            try:
                while True:
                    observer.on_next(await aiter.__anext__())
            except StopAsyncIteration:
                pass

        def done(future):
            """Callback for when the worker is done."""

            try:
                future.result()
                observer.on_completed()
            except Exception as ex:
                observer.on_error(ex)

        # Wrap worker into a task and signal complete when done.
        task = loop.create_task(worker(asyncgen))
        task.add_done_callback(done)

        def dispose():
            """Allow the task to be cancelable."""

            if task and task.cancel:
                task.cancel()

        return dispose

    return rx.AnonymousObservable(subscribe)


extensionclassmethod(rx.AnonymousObservable)(from_async_iterable)
extensionclassmethod(rx.Observable)(from_async_iterable)
