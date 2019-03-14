"""
    dataclasses
    ===========

    Wrappers around Python's dataclasses to support slots and defaults.

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

import contextlib
import copy
import dataclasses
import inspect
import re
import typing

SNAKE_CASE = re.compile(r'(.*?)_([a-z])')


def snake_to_camel(name: str) -> str:
    """Convert value with snake_case name to camelCase."""

    return SNAKE_CASE.sub(lambda x: x.group(1) + x.group(2).upper(), name)


def set_defaults(cls, defaults):
    """Set and validate optional default arguments."""

    if not defaults:
        return

    # Need to validate we aren't adding defaults for interior items.
    init = cls.__init__
    code = init.__code__
    varnames = code.co_varnames
    count = len(defaults)
    if not all(i in defaults for i in varnames[-count:]):
        raise SyntaxError("non-default argument follows default argument")
    if init.__defaults__ is not None:
        raise SyntaxError("__defaults__ should be none.")

    init.__defaults__ = tuple(defaults.values())


def global_annotation(global_vars, type):
    """Fix annotation for field with type."""

    if isinstance(type, str):
        if type in global_vars:
            return global_vars[type]
    elif isinstance(type, typing.ForwardRef):
        arg = global_annotation(global_vars, type.__forward_arg__)
        is_argument = type.__forward_is_argument__
        if isinstance(arg, str):
            return typing.ForwardRef(arg, is_argument)
        return arg
    elif hasattr(type, '__args__'):
        args = type.__args__
        args = tuple((global_annotation(global_vars, i) for i in args))
        type.__args__ = args

    return type


def fix_annotations(cls, clsdict, global_vars):
    """Fix any forward references to variables defined in the callee scope."""

    # Don't care except when enforcing types.
    if not typing.TYPE_CHECKING:
        return

    annotations = clsdict['__annotations__']
    for field, type in annotations.items():
        type = global_annotation(global_vars, type)
        annotations[field] = type


def set_slots(cls, clsdict, slots):
    """Set default __slots__ implementation."""

    if not slots or '__slots__' in clsdict:
        return
    annotations = clsdict['__annotations__']
    is_classvar = lambda x: getattr(x, '__origin__', None) is not typing.ClassVar
    slots = (k for k, v in annotations.items() if is_classvar(v))
    clsdict['__slots__'] = tuple(slots)


def set_copy(cls, clsdict, copy) -> None:
    """Set default __copy__ implementation."""

    if not copy or '__copy__' in clsdict:
        return

    def func(self):
        return dataclasses.replace(self)

    func.__name__ = '__copy__'
    func.__qualname__ = f'{cls.__qualname__}.__copy__'
    func.__module__ = cls.__module__
    clsdict['__copy__'] = func


def set_deepcopy(cls, clsdict, deepcopy):
    """Set default __deepcopy__ implementation."""

    if not deepcopy or '__deepcopy__' in clsdict:
        return

    def func(self):
        data = copy.deepcopy(dataclasses.asdict(self))
        return cls(**data)

    func.__name__ = '__deepcopy__'
    func.__qualname__ = f'{cls.__qualname__}.__deepcopy__'
    func.__module__ = cls.__module__
    clsdict['__deepcopy__'] = func


def set_asdict(cls, clsdict, asdict):
    """Set default asdict implementation."""

    if not asdict or 'asdict' in clsdict:
        return

    def func(self, dict_factory=dict) -> dict:
        return dataclasses.asdict(self, dict_factory=dict_factory)

    func.__name__ = 'asdict'
    func.__qualname__ = f'{cls.__qualname__}.asdict'
    func.__module__ = cls.__module__
    clsdict['asdict'] = func


def set_astuple(cls, clsdict, astuple):
    """Set default astuple implementation."""

    if not astuple or 'astuple' in clsdict:
        return

    def func(self, tuple_factory=tuple) -> tuple:
        return dataclasses.astuple(self, tuple_factory=tuple_factory)

    func.__name__ = 'astuple'
    func.__qualname__ = f'{cls.__qualname__}.astuple'
    func.__module__ = cls.__module__
    clsdict['astuple'] = func


def set_fields(cls, clsdict, fields):
    """Set default fields implementation."""

    if not fields or 'fields' in clsdict:
        return

    def func(self) -> tuple:
        return dataclasses.fields(self)

    func.__name__ = 'fields'
    func.__qualname__ = f'{cls.__qualname__}.fields'
    func.__module__ = cls.__module__
    clsdict['fields'] = func


def set_replace(cls, clsdict, replace):
    """Set default replace implementation."""

    if not replace or 'replace' in clsdict:
        return

    def func(self, **changes) -> tuple:
        return dataclasses.replace(self, **changes)

    func.__name__ = 'replace'
    func.__qualname__ = f'{cls.__qualname__}.replace'
    func.__module__ = cls.__module__
    clsdict['replace'] = func


def set_camelcase_properties(cls, clsdict, camelcase_properties):
    """Adds camelcase properties if desired."""

    if not camelcase_properties:
        return

    def wrapper(field, type):
        def fget(self):
            return getattr(self, field)

        def fset(self, value) -> None:
            setattr(self, field, value)

        def fdel(self) -> None:
            delattr(self, field)

        return fget, fset, fdel

    for field, type in clsdict['__annotations__'].items():
        camelcase = snake_to_camel(field)
        if field != camelcase:
            fget, fset, fdel = wrapper(field, type)
            fget.__name__ = camelcase
            fget.__qualname__ = f'{cls.__qualname__}.{camelcase}'
            fget.__module__ = cls.__module__
            clsdict[camelcase] = property(fget, fset, fdel)


def wrap_dataclass(
    cls,
    global_vars,
    slots=True,
    copy=True,
    deepcopy=True,
    asdict=True,
    astuple=True,
    fields=True,
    replace=True,
    camelcase_properties=True
):
    """Wrap a dataclass base with the desired methods."""

    mcls = cls.__class__
    name = cls.__name__
    bases = cls.__bases__
    clsdict = cls.__dict__.copy()
    fix_annotations(cls, clsdict, global_vars)
    set_slots(cls, clsdict, slots)
    set_copy(cls, clsdict, copy)
    set_deepcopy(cls, clsdict, deepcopy)
    set_asdict(cls, clsdict, asdict)
    set_astuple(cls, clsdict, astuple)
    set_fields(cls, clsdict, fields)
    set_replace(cls, clsdict, replace)
    set_camelcase_properties(cls, clsdict, camelcase_properties)

    return mcls.__new__(mcls, name, bases, clsdict)


def update_closure(cls, new_cls):
    """
    Due to our dynamic creation of a new class, our old class may still
    be present in some closures, and injected later on, through __class__.
    Most notably, this is pernicious with super(), especially in __init__.
    To rectify this, we can check if '__class__' is in nonlocal vars
    for the function (`func.__code__.co_freevars`), and if it is,
    and the old class is bound, update it.

    This is all well-documented in the Python data model:
        __code__: Contains compiled function bytecode.
        co_freevars: Contains free variables referenced inside closure.
        __closure__: None or tuple of cells for the functions free variables.
        cell_contents: Get value of cell.

    Since we want a value injected locally (a free variable), with the
    name `__class__`, we can use these attributes to determine if the old
    class is bound to `__class__`, and if so, overwrite it.
    """

    funcs = inspect.getmembers(new_cls, inspect.isroutine)
    for _, func in funcs:
        # Unwrap method if applicable.
        func = getattr(func, '__func__', func)
        with contextlib.suppress(AttributeError):
            # Builtin functions won't have __code__.
            code = func.__code__
            closure = func.__closure__
            freevars = code.co_freevars
            if closure and freevars and '__class__' in freevars:
                # Have a specified class in freevars, must fix in closure.
                # Only change if the cell_contents is the old cls,
                # which we need to replace with the new cls.
                for cell in closure:
                    if cell.cell_contents is cls:
                        cell.cell_contents = new_cls


def dataclass(
    cls=None,
    *,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
    slots=True,
    copy=True,
    deepcopy=True,
    asdict=True,
    astuple=True,
    fields=True,
    replace=True,
    camelcase_properties=True,
    **defaults
):
    """Generate a slotted dataclass with optional default arguments."""

    frame = inspect.stack()[1].frame
    global_vars = frame.f_globals
    dataclass_kwds = {
        'init': init,
        'repr': repr,
        'eq': eq,
        'order': order,
        'unsafe_hash': unsafe_hash,
        'frozen': frozen,
    }
    wrap_kwds = {
        'slots': slots,
        'copy': copy,
        'deepcopy': deepcopy,
        'asdict': asdict,
        'astuple': astuple,
        'fields': fields,
        'replace': replace,
        'camelcase_properties': camelcase_properties,
    }

    def wrap(cls):
        base = wrap_dataclass(cls, global_vars, **wrap_kwds)
        new_cls = dataclasses.dataclass(**dataclass_kwds)(base)
        set_defaults(new_cls, defaults)
        update_closure(cls, new_cls)
        return new_cls

    if cls is None:
        return wrap
    return wrap(cls)
