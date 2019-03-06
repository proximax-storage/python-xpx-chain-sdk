"""
    documentation
    =============

    Functions to modify doc strings.

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

import functools
import inspect
import typing

from .reify import reify


def isproperty(f: typing.Any) -> bool:
    """Check to see if a callable is a property."""

    return isinstance(f, property)


def isreify(f: typing.Any) -> bool:
    """Check to see if a callable is a reified property."""

    return isinstance(f, reify)


def isfunction(f: typing.Any) -> bool:
    """Check to see if a callable is a function."""

    return inspect.isfunction(f)


def isclassmethod(f: typing.Any) -> bool:
    """Check to see if a callable is a classmethod."""

    return isinstance(f, classmethod)


def isstaticmethod(f: typing.Any) -> bool:
    """Check to see if a callable is a staticmethod."""

    return isinstance(f, staticmethod)


def doc_function(f: typing.Callable, doc: typing.Optional[str]) -> typing.Callable:
    """Add documentation to a function."""

    @functools.wraps(f)
    def wrapper(*args, **kwds):
        return f(*args, **kwds)

    wrapper.__doc__ = doc
    return wrapper


def wrap_property(f: property, callback: typing.Callable) -> property:
    """Wrap and remove doc string from a property."""

    kwds = {'doc': None}
    if isfunction(f.fget):
        kwds['fget'] = wrap_function(f.fget, callback)
    if isfunction(f.fset):
        kwds['fset'] = wrap_function(f.fset, callback)
    if isfunction(f.fdel):
        kwds['fdel'] = wrap_function(f.fdel, callback)

    return property(**kwds)


def wrap_reify(f: reify, callback: typing.Callable) -> reify:
    """Wrap and remove doc string from a reified property."""

    kwds = {'doc': reify.__doc__}
    if isfunction(f.fget):
        kwds['fget'] = wrap_function(f.fget, callback)

    return reify(**kwds)


def wrap_function(f: typing.Callable, callback: typing.Callable) -> typing.Callable:
    """Wrap and remove doc string from a function."""

    return callback(f)


def wrap_classmethod(f: classmethod, callback: typing.Callable) -> classmethod:
    """Wrap and remove doc string from a classmethod."""

    value = classmethod(wrap_function(f.__func__, callback))
    value.__doc__ = f.__func__.__doc__
    return value


def wrap_staticmethod(f: staticmethod, callback: typing.Callable) -> staticmethod:
    """Wrap and remove doc string from a staticmethod."""

    value = staticmethod(wrap_function(f.__func__, callback))
    value.__doc__ = f.__func__.__doc__
    return value


def wrapper(doc: typing.Optional[str]) -> typing.Callable:
    """Implied wrapper for both doc and undoc."""

    def decorator(f: typing.Callable) -> typing.Any:
        callback = lambda x: doc_function(x, doc)
        if isproperty(f):
            # Properties
            return wrap_property(f, callback)
        elif isreify(f):
            # Reified properties
            return wrap_reify(f, callback)
        elif isfunction(f):
            # Functions, methods
            return wrap_function(f, callback)
        elif isclassmethod(f):
            # Classmethods
            return wrap_classmethod(f, callback)
        elif isstaticmethod(f):
            # Staticmethods
            return wrap_staticmethod(f, callback)
        raise NotImplementedError

    return decorator


def doc(doc: typing.Any) -> typing.Callable:
    """Wrap a callable, copying over all attributes with a new doc string."""

    # Remove doc strings if we'd like to clone the doc string from an
    # existing function.
    if not isinstance(doc, str):
        doc = doc.__doc__

    return wrapper(doc)


def undoc(f: typing.Any) -> typing.Any:
    """Wrap a callable, copying over all attributes except the doc string."""

    return wrapper(None)(f)
