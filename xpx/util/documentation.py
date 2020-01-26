"""
    documentation
    =============

    Decorators to modify doc strings.

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
import inspect
import typing

__all__ = [
    'inherit_doc',
]


def is_public(f):
    """Check if function is public."""
    return not f.__name__.startswith('_')


def has_doc(f):
    """Check if function has doc string."""
    return f.__doc__ is not None


def needs_doc(f):
    """Check if function is public and has no doc string."""
    return is_public(f) and not has_doc(f)


def inherit_doc(cls: typing.Type) -> typing.Type:
    """Inherit documentation from a base class."""

    # Ignore anything coming from Python internally, or that
    # is private to begin with.
    bases = [i for i in cls.__bases__ if i is not object]
    members = inspect.getmembers(cls, inspect.isroutine)
    members = ((k, v) for k, v in members if needs_doc(v))
    for key, func in members:
        for base in bases:
            doc = getattr(getattr(base, key, None), '__doc__', None)
            if doc is not None:
                # Methods use a property to get the doc.
                if inspect.ismethod(func):
                    func.__func__.__doc__ = doc
                else:
                    func.__doc__ = doc

    return cls
