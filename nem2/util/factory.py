"""
    factory
    =======

    Patch objects defined in factories to avoid the factory scope.

    Patch the fully-qualified name and module of objects defined within
    a local scope (IE, in class factories).

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
import typing

from .reify import reify


def concat(*names: str) -> str:
    """Concatenate names to generate fully-qualified name."""

    return '.'.join(names)


def defactorize_method(meth, module, qualname, special):
    """Patch a method to modify the qualified name and module."""

    defactorize_function(meth.__func__, module, qualname, special)

    return meth


def defactorize_function(func, module, qualname, special):
    """Patch a function to modify the qualified name and module."""

    func.__module__ = module
    func.__qualname__ = qualname

    if typing.TYPE_CHECKING:
        # Update the annotations for any reference nonlocals.
        # These must be returned too.
        # This is very expensive, so only use it if we care about
        # annotations.
        closure_vars = inspect.getclosurevars(func)
        for key, value in func.__annotations__.items():
            if isinstance(value, str) and value in closure_vars.nonlocals:
                func.__annotations__[key] = closure_vars.nonlocals[value]

    wrapped = getattr(func, '__wrapped__', None)
    if wrapped is not None:
        defactorize_function(wrapped, module, qualname, special)

    return func


def defactorize_property(prop, module, qualname, special):
    """Patch a property to modify the qualified name and module."""

    if prop.fget is not None:
        defactorize_function(prop.fget, module, qualname, special)
    if prop.fset is not None:
        defactorize_function(prop.fset, module, qualname, special)
    if prop.fdel is not None:
        defactorize_function(prop.fdel, module, qualname, special)

    return prop


def defactorize_class(cls, module, qualname, special):
    """Patch a class to modify the qualified name and module."""

    cls.__module__ = module
    cls.__qualname__ = qualname
    members = inspect.getmembers(cls)
    for key, inner in members:
        if key in special or not key.startswith('_'):
            inner_name = concat(qualname, key)
            defactorize(inner, module, inner_name, special)

    return cls


def defactorize(obj, module=None, qualname=None, namespace=None, special={'__init__'}):
    """
    Patch an object to modify the qualified name and module.

    This is mostly for Sphinx compatibility, to avoid
    treating the class like a local variable in class factories.

    This only does a 1-depth pass, and ignores all special and private
    members (unless explicitly included via the `special` argument).

    This also only allows objects to be declared globally, anything
    passed to this function must be at the global scope.

    :param obj: Object to remove the factory scope from.
    :param module: New module for object.
    :param qualname: (Optional) New fully-qualified name for object.
    :param special: (Optional) Set of special methods to patch.

    Warning
    -------

    This method is very dependent on Python internals, and therefore
    may break at some time in the future. To avoid this, the internals
    are clearly described below, with the Python data [`model`],
    [`functools`], and [`property`] references describing these
    special attributes in more detail.

        __name__: Function/class name. Writable.
        __qualname__: Fully-qualified function/class name. Writable.
        __module__: Name module function/class defined in. Writable.
        __func__: Internal function for an instance method. Read-only.
        __wrapped__: Points to the wrapped function object. Writable.
        __annotations__: Type annotations for function parameters. Writable.
        fget: Internal function to get a value from a property. Writable.
        fset: Internal function to set a value from a property. Writable.
        fdel: Internal function to delete a value from a property. Writable.

    [`model`]: https://docs.python.org/3/reference/datamodel.html
    [`functools`]: https://docs.python.org/3/library/functools.html
    [`property`]: https://docs.python.org/3/library/functions.html#property
    """

    if module is None:
        frame = inspect.stack()[1].frame
        module = inspect.getmodule(frame).__name__
    if qualname is None:
        qualname = obj.__name__

    # Ignore private and special members
    if inspect.ismethod(obj):
        # Classmethods only
        return defactorize_method(obj, module, qualname, special)
    elif inspect.isfunction(obj):
        # Functions, methods, and static methods only.
        return defactorize_function(obj, module, qualname, special)
    elif isinstance(obj, (property, reify)):
        # Properties and reified properties only
        return defactorize_property(obj, module, qualname, special)
    elif inspect.isclass(obj):
        # Classes only.
        return defactorize_class(obj, module, qualname, special)
    elif inspect.ismethoddescriptor(obj):
        # Built-in method descriptor, ignore.
        return obj
    elif inspect.isdatadescriptor(obj):
        # Built-in data descriptor, ignore.
        return obj
    elif inspect.isgetsetdescriptor(obj):
        # Built-in get/set descriptor, ignore.
        return obj
    elif inspect.ismemberdescriptor(obj):
        # Built-in member descriptor, ignore.
        return obj
    else:
        # Error so we can handle other types without silently passing.
        raise NotImplementedError
