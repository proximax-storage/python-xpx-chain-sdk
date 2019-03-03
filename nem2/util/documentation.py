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


def wrapproperty(f):
    """Wrap and remove doc string from a property."""

    kwds = {'doc': None}
    if isfunction(f.fget):
        kwds['fget'] = wrapfunction(f.fget)
    if isfunction(f.fset):
        kwds['fset'] = wrapfunction(f.fset)
    if isfunction(f.fdel):
        kwds['fdel'] = wrapfunction(f.fdel)

    return property(**kwds)


def wrapfunction(f):
    """Wrap and remove doc string from a function."""

    @wraps(f)
    def hidden(*args, **kwds):
        return f(*args, **kwds)

    hidden.__doc__ = None
    return hidden

def wrapclassmethod(f):
    """Wrap and remove doc string from a classmethod."""

    return classmethod(wrapfunction(f.__func__))


def wrapstaticmethod(f):
    """Wrap and remove doc string from a staticmethod."""

    return staticmethod(wrapfunction(f.__func__))


def undoc(f):
    """Wrap a callable, copying over all attributes except the doc string."""

    if isproperty(f):
        # Properties
        return wrapproperty(f)
    elif isfunction(f):
        # Functions, methods
        return wrapfunction(f)
    elif isclassmethod(f):
        # Classmethods
        return wrapclassmethod(f)
    elif isstaticmethod(f):
        # Staticmethods
        return wrapstaticmethod(f)
    raise NotImplementedError
