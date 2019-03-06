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

import inspect
from functools import wraps


def isproperty(f):
    """Check to see if a callable is a property."""

    return isinstance(f, property)


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

    @wraps(f)
    def wrapper(*args, **kwds):
        return f(*args, **kwds)

    wrapper.__doc__ = doc
    return wrapper


def undoc_function(f):
    """Remove documentation from a function."""

    @wraps(f)
    def wrapper(*args, **kwds):
        return f(*args, **kwds)

    wrapper.__doc__ = None
    return wrapper


def wrap_property(f, callback):
    """Wrap and remove doc string from a property."""

    kwds = {'doc': None}
    if isfunction(f.fget):
        kwds['fget'] = wrap_function(f.fget, callback)
    if isfunction(f.fset):
        kwds['fset'] = wrap_function(f.fset, callback)
    if isfunction(f.fdel):
        kwds['fdel'] = wrap_function(f.fdel, callback)

    return property(**kwds)


def wrap_function(f, callback):
    """Wrap and remove doc string from a function."""

    return callback(f)


def wrap_classmethod(f, callback):
    """Wrap and remove doc string from a classmethod."""

    value = classmethod(wrap_function(f.__func__, callback))
    value.__doc__ = f.__func__.__doc__
    return value


def wrap_staticmethod(f, callback):
    """Wrap and remove doc string from a staticmethod."""

    value = staticmethod(wrap_function(f.__func__, callback))
    value.__doc__ = f.__func__.__doc__
    return value


def doc(doc):
    """Wrap a callable, copying over all attributes with a new doc string."""

    # Remove doc strings if we'd like to clone the doc string from an
    # existing function.
    if not isinstance(doc, str):
        doc = doc.__doc__

    def decorator(f):
        callback = lambda x: doc_function(x, doc)
        if isproperty(f):
            # Properties
            return wrap_property(f, callback)
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


def undoc(f):
    """Wrap a callable, copying over all attributes except the doc string."""

    if isproperty(f):
        # Properties
        return wrap_property(f, undoc_function)
    elif isfunction(f):
        # Functions, methods
        return wrap_function(f, undoc_function)
    elif isclassmethod(f):
        # Classmethods
        return wrap_classmethod(f, undoc_function)
    elif isstaticmethod(f):
        # Staticmethods
        return wrap_staticmethod(f, undoc_function)
    raise NotImplementedError
