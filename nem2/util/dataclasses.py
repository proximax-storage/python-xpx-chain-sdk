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

from __future__ import annotations
import contextlib
import copy
import dataclasses
import inspect
import typing

__all__ = [
    'Field',
    'FrozenInstanceError',
    'InitVar',
    'MISSING',
    'dataclass',
    'is_dataclass',
]

# HELPERS

Field = dataclasses.Field
FrozenInstanceError = dataclasses.FrozenInstanceError
InitVar = dataclasses.InitVar
MISSING = dataclasses.MISSING
is_dataclass = dataclasses.is_dataclass
# ForwardRef isn't part of the public API.
# If it's not present, just skip it.
ForwardRef = getattr(typing, 'ForwardRef', str)
Vars = typing.Dict[str, typing.Any]
DictType = typing.Mapping[str, typing.Any]
TupleType = typing.Sequence[typing.Any]
DictFactory = typing.Callable[..., DictType]
TupleFactory = typing.Callable[..., TupleType]

# NEW METHODS


def get_argnames(func):
    """Get the argument names from a function."""

    # Get all positional arguments in __init__, including named
    # and named optional arguments. `co_varnames` stores all argument
    # names (including local variable names) in order, starting with
    # function arguments, so only grab `co_argcount` varnames.
    code = func.__code__
    argcount = code.co_argcount
    return code.co_varnames[:argcount]


def set_defaults(
    cls: typing.Type,
    defaults: Vars,
) -> None:
    """Set and validate optional default arguments."""

    if not defaults:
        return

    # Need to validate we aren't adding defaults for interior items.
    init = cls.__init__
    varnames = get_argnames(init)
    count = len(defaults)
    if not all(i in defaults for i in varnames[-count:]):
        raise SyntaxError("non-default argument follows default argument")
    if init.__defaults__ is not None:
        raise SyntaxError("__defaults__ should be none.")

    init.__defaults__ = tuple(defaults.values())


def fix_annotation(type, global_vars: Vars, local_vars: Vars):
    """Fix annotation for field with type."""

    if isinstance(type, str):
        try:
            # Silence a warning about sec, all the arguments passed.
            # Eval only gets passed for internal type annotations.
            return eval(type, global_vars, local_vars)  # nosec
        except NameError:
            return type
    elif isinstance(type, ForwardRef):
        arg = fix_annotation(type.__forward_arg__, global_vars, local_vars)
        is_argument = type.__forward_is_argument__
        if isinstance(arg, str):
            return ForwardRef(arg, is_argument)
        return arg
    elif hasattr(type, '__args__'):
        args = type.__args__
        args = tuple((fix_annotation(i, global_vars, local_vars) for i in args))
        type.__args__ = args

    return type


def fix_annotations(
    cls: typing.Type,
    clsdict: Vars,
    global_vars: Vars,
    local_vars: Vars,
) -> None:
    """Fix any forward references to variables defined in the callee scope."""

    # Don't care except when enforcing types.
    if typing.TYPE_CHECKING:
        annotations = clsdict['__annotations__']
        for field, type in annotations.items():
            type = fix_annotation(type, global_vars, local_vars)
            annotations[field] = type


def is_classvar(x, global_vars: Vars, local_vars: Vars) -> bool:
    """Determine if x is a ClassVar."""

    if isinstance(x, str):
        # Silence a warning about sec, all the arguments passed.
        # Eval only gets passed for internal type annotations.
        x = eval(x, global_vars, local_vars)    # nosec
    return getattr(x, '__origin__', None) is typing.ClassVar


def set_slots(
    cls: typing.Type,
    clsdict: Vars,
    slots: bool,
    global_vars: Vars,
    local_vars: Vars,
) -> None:
    """Set default __slots__ implementation."""

    if not slots or '__slots__' in clsdict:
        return
    annotations = clsdict['__annotations__']
    is_cv = lambda x: is_classvar(x, global_vars, local_vars)
    slots = (k for k, v in annotations.items() if not is_cv(v))
    clsdict['__slots__'] = tuple(slots)


def set_copy(
    cls: typing.Type,
    clsdict: Vars,
    copy: bool,
) -> None:
    """Set default __copy__ implementation."""

    if not copy or '__copy__' in clsdict:
        return

    def func(self):
        return type(self)(**replace_dict(self))

    func.__name__ = '__copy__'
    func.__qualname__ = f'{cls.__qualname__}.__copy__'
    func.__module__ = cls.__module__
    clsdict['__copy__'] = func


def set_deepcopy(
    cls: typing.Type,
    clsdict: Vars,
    deepcopy: bool,
) -> None:
    """Set default __deepcopy__ implementation."""

    if not deepcopy or '__deepcopy__' in clsdict:
        return

    def func(self, memo=None):
        data = copy.deepcopy(replace_dict(self), memo)
        return type(self)(**data)

    func.__name__ = '__deepcopy__'
    func.__qualname__ = f'{cls.__qualname__}.__deepcopy__'
    func.__module__ = cls.__module__
    clsdict['__deepcopy__'] = func


def shallow_asdict(self, dict_factory: DictFactory = dict) -> DictType:
    names = [i.name for i in dataclasses.fields(self)]
    return dict_factory([(i, getattr(self, i)) for i in names])


def deep_asdict(self, dict_factory: DictFactory = dict) -> DictType:
    return dataclasses.asdict(self, dict_factory=dict_factory)


def set_asdict(
    cls: typing.Type,
    clsdict: Vars,
    asdict: bool,
) -> None:
    """Set default asdict implementation."""

    if not asdict or 'asdict' in clsdict:
        return

    def func(
        self,
        recurse: bool = True,
        dict_factory: DictFactory = dict,
    ) -> DictType:
        if recurse:
            return deep_asdict(self, dict_factory=dict_factory)
        return shallow_asdict(self, dict_factory=dict_factory)

    func.__name__ = 'asdict'
    func.__qualname__ = f'{cls.__qualname__}.asdict'
    func.__module__ = cls.__module__
    clsdict['asdict'] = func


def shallow_astuple(self, tuple_factory: TupleFactory = tuple) -> TupleType:
    names = [i.name for i in dataclasses.fields(self)]
    return tuple_factory([getattr(self, i) for i in names])


def deep_astuple(self, tuple_factory: TupleFactory = tuple) -> TupleType:
    return dataclasses.astuple(self, tuple_factory=tuple_factory)


def set_astuple(
    cls: typing.Type,
    clsdict: Vars,
    astuple: bool,
) -> None:
    """Set default astuple implementation."""

    if not astuple or 'astuple' in clsdict:
        return

    def func(
        self,
        recurse: bool = True,
        tuple_factory: TupleFactory = tuple,
    ) -> TupleType:
        if recurse:
            return deep_astuple(self, tuple_factory=tuple_factory)
        return shallow_astuple(self, tuple_factory=tuple_factory)

    func.__name__ = 'astuple'
    func.__qualname__ = f'{cls.__qualname__}.astuple'
    func.__module__ = cls.__module__
    clsdict['astuple'] = func


def set_fields(
    cls: typing.Type,
    clsdict: Vars,
    fields: bool,
) -> None:
    """Set default fields implementation."""

    if not fields or 'fields' in clsdict:
        return

    def func(self) -> tuple:
        return dataclasses.fields(self)

    func.__name__ = 'fields'
    func.__qualname__ = f'{cls.__qualname__}.fields'
    func.__module__ = cls.__module__
    clsdict['fields'] = func


def replace_dict(self):
    # This is a smart-replace, any fields that are not defined
    # in the initializer are ignored, since it is assumed
    # sensible defaults are automatically provided for those.
    varnames = get_argnames(self.__init__.__func__)[1:]
    return {k: getattr(self, k) for k in varnames}


def set_replace(
    cls: typing.Type,
    clsdict: Vars,
    replace: bool,
) -> None:
    """Set default replace implementation."""

    if not replace or 'replace' in clsdict:
        return

    def func(self, **changes):
        # Convert to a dictionary and then call __init__.
        asdict = replace_dict(self)
        asdict.update(changes)
        return self.__class__(**asdict)

    func.__name__ = 'replace'
    func.__qualname__ = f'{cls.__qualname__}.replace'
    func.__module__ = cls.__module__
    clsdict['replace'] = func


def set_miscellaneous(cls: typing.Type, clsdict: Vars) -> None:
    """Set miscellaneous data for the class."""

    clsdict['_set'] = object.__setattr__


# DATACLASS METACLASS


def wrap_dataclass(
    cls: typing.Type,
    global_vars: typing.Dict[str, typing.Any],
    local_vars: typing.Dict[str, typing.Any],
    slots: bool = True,
    copy: bool = True,
    deepcopy: bool = True,
    asdict: bool = True,
    astuple: bool = True,
    fields: bool = True,
    replace: bool = True,
) -> typing.Type:
    """Wrap a dataclass base with the desired methods."""

    mcls = cls.__class__
    name = cls.__name__
    bases = cls.__bases__
    clsdict = cls.__dict__.copy()
    clsdict.setdefault('__annotations__', {})
    fix_annotations(cls, clsdict, global_vars, local_vars)
    set_slots(cls, clsdict, slots, global_vars, local_vars)
    set_copy(cls, clsdict, copy)
    set_deepcopy(cls, clsdict, deepcopy)
    set_asdict(cls, clsdict, asdict)
    set_astuple(cls, clsdict, astuple)
    set_fields(cls, clsdict, fields)
    set_replace(cls, clsdict, replace)
    set_miscellaneous(cls, clsdict)

    return mcls.__new__(mcls, name, bases, clsdict)


# PATCHES


def update_method(
    cls: typing.Type,
    new_cls: typing.Type,
    func,
) -> None:
    """
    Due to our dynamic creation of a new class, our old class may still
    be present in some function closures, through `super()/__class__`.
    We should not have remnants of the old class anywhere else, since
    that would require hard-coding the actual class name, which should
    not be done for obvious reasons.

    To rectify this, we can check if '__class__' is in nonlocal vars
    for each function (`func.__code__.co_freevars`), and if it is,
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


def update_methods(cls: typing.Type, new_cls: typing.Type) -> None:
    """Replace all instances of `super()/__class__` with the new class."""

    funcs = inspect.getmembers(new_cls, inspect.isroutine)
    for _, func in funcs:
        # Unwrap method if applicable.
        func = getattr(func, '__func__', func)
        with contextlib.suppress(AttributeError):
            # Builtin functions won't have __code__.
            update_method(cls, new_cls, func)


def update_classvars(cls: typing.Type, new_cls: typing.Type) -> None:
    """Replace all instances of the old class in class variables."""

    # We're going to cheat, since this is a painfully long process.
    # We know the only classvars that can be present are in:
    #   1. TYPE_MAP

    # Mapping of transaction type to transactions.
    # We use a bidict to get O(1) inverse lookup times.
    type_map = getattr(cls, 'TYPE_MAP', None)
    if type_map is not None and cls in type_map.inverse:
        type = type_map.inverse.pop(cls)
        type_map[type] = new_cls


def update_closure(cls: typing.Type, new_cls: typing.Type) -> None:
    """
    Due to our dynamic creation of a new class, our old class
    may be present in our new class definition.

    Most notably, it may be present in:
        1. Methods using `super()/__class__`.
        2. Any class variables.
    """

    update_methods(cls, new_cls)
    update_classvars(cls, new_cls)


# DATACLASS


def dataclass(
    cls: typing.Optional[typing.Type] = None,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    slots: bool = True,
    copy: bool = True,
    deepcopy: bool = True,
    asdict: bool = True,
    astuple: bool = True,
    fields: bool = True,
    replace: bool = True,
    **defaults: typing.Any
):
    """Generate a slotted dataclass with optional default arguments."""

    frame = inspect.stack()[1].frame
    global_vars = frame.f_globals
    local_vars = frame.f_locals
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
    }

    def wrap(cls: typing.Type) -> typing.Type:
        base = wrap_dataclass(cls, global_vars, local_vars, **wrap_kwds)
        new_cls = dataclasses.dataclass(**dataclass_kwds)(base)
        set_defaults(new_cls, defaults)
        update_closure(cls, new_cls)
        return new_cls

    if cls is None:
        return wrap
    return wrap(cls)
