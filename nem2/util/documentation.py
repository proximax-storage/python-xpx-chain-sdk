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

from .reify import reify


def isproperty(f):
    """Check to see if a callable is a property."""

    return isinstance(f, property)


def isreify(f):
    """Check to see if a callable is a reified property."""

    return isinstance(f, reify)


def isfunction(f):
    """Check to see if a callable is a function."""

    return inspect.isfunction(f)


def isclassmethod(f):
    """Check to see if a callable is a classmethod."""

    return isinstance(f, classmethod)


def isstaticmethod(f):
    """Check to see if a callable is a staticmethod."""

    return isinstance(f, staticmethod)


def doc_function(f, doc):
    """Add documentation to a function."""

    @functools.wraps(f)
    def wrapper(*args, **kwds):
        return f(*args, **kwds)

    wrapper.__doc__ = doc
    return wrapper


def wrap_property(f, callback):
    """Wrap and modify doc string on a property."""

    kwds = {'doc': None}
    if isfunction(f.fget):
        kwds['fget'] = wrap_function(f.fget, callback)
    if isfunction(f.fset):
        kwds['fset'] = wrap_function(f.fset, callback)
    if isfunction(f.fdel):
        kwds['fdel'] = wrap_function(f.fdel, callback)

    return property(**kwds)


def wrap_reify(f, callback):
    """Wrap and modify doc string on a reified property."""

    kwds = {'doc': f.__doc__}
    if isfunction(f.fget):
        kwds['fget'] = wrap_function(f.fget, callback)

    return reify(**kwds)


def wrap_function(f, callback):
    """Wrap and modify doc string on a function."""

    return callback(f)


def wrap_classmethod(f, callback):
    """Wrap and modify doc string on a classmethod."""

    value = classmethod(wrap_function(f.__func__, callback))
    value.__doc__ = f.__func__.__doc__
    return value


def wrap_staticmethod(f, callback):
    """Wrap and modify doc string on a staticmethod."""

    value = staticmethod(wrap_function(f.__func__, callback))
    value.__doc__ = f.__func__.__doc__
    return value


def wrapper(doc):
    """Implied wrapper for both doc and undoc."""

    def decorator(f):
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


def doc(doc):
    """Wrap a callable, copying over all attributes with a new doc string."""

    # Remove doc strings if we'd like to clone the doc string from an
    # existing function.
    if not isinstance(doc, str):
        doc = doc.__doc__

    return wrapper(doc)


def undoc(f):
    """Wrap a callable, copying over all attributes except the doc string."""

    return wrapper(None)(f)


def inherit_doc(cls):
    """Inherit documentation from a base class."""

    # Ignore anything coming from Python internally, or that
    # is private to begin with.
    bases = [i for i in cls.__bases__ if i is not object]
    members = inspect.getmembers(cls, inspect.isroutine)
    members = ((k, v) for k, v in members if not k.startswith('_') and v.__doc__ is None)
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
