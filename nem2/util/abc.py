"""
    abc
    ====

    Abstract base classes for NEM models.

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

import abc
import enum
import inspect
import sys
import types
from .format import InterchangeFormat


__all__ = [
    'ABCEnumMeta',
    'Dto',
    'Catbuffer',
    'Model',
    'Tie',
    'enum_catbuffer',
    'enum_dto',
    'enum_model',
]

# ABC ENU META
# ------------


def abc_enum_error(cls):
    """Raise TypeError for abstract enum without all methods implemented."""

    raise TypeError(f"Can't instantiate abstract class {cls.__name__} with abstract methods {set(cls.__abstractmethods__)}")


def check_abstractmethods(cls, base):
    """Ensure all abstractmethods are defined in the cls."""

    # Check all abstract members are defined
    for item in base.__abstractmethods__:
        abc_value = getattr(base, item)
        derived_value = getattr(cls, item)
        if inspect.isfunction(abc_value):
            # Functions, Staticmethods
            if abc_value is derived_value:
                abc_enum_error(base)
        elif inspect.ismethod(abc_value):
            # Classmethods
            if abc_value.__func__ is derived_value.__func__:
                abc_enum_error(base)
        elif isinstance(abc_value, property):
            # Properties
            if abc_value is derived_value:
                abc_enum_error(base)


def add_nonabc(cls, base):
    """Add over all methods not present in abc.ABC from a base to a cls."""

    abc_dict = abc.ABC.__dict__
    for key, value in base.__dict__.items():
        if key not in abc_dict:
            if inspect.isfunction(value):
                # Functions, Staticmethods
                setattr(cls, key, value)
            elif inspect.ismethod(value):
                # Classmethods
                setattr(cls, key, types.MethodType(value.__func__, cls))
            elif isinstance(value, property):
                # Properties
                setattr(cls, key, value)
            else:
                # Other variables, like class variables
                setattr(cls, key, value)


if sys.version_info < (3, 7):
    # < Python 3.7, uses object.__new__ for enum subtype, must fake
    # inheritance.
    class ABCEnumMeta(abc.ABCMeta, enum.EnumMeta):
        """Abstract metaclass that is both abstract and an enumeration."""

        # Store abstract base classes to fake inheritance for
        # Python <= 3.7.
        abc_memo = {}

        @property
        def abcs(cls):
            return cls.abc_memo[id(cls)]

        @abcs.setter
        def abcs(cls, value):
            cls.abc_memo[id(cls)] = value

        @property
        def __mro__(cls):
            mro = type.__dict__['__mro__'].__get__(cls)
            return (mro[0], *cls.abcs, abc.ABC, *mro[2:],)

        @property
        def __base__(cls):
            mro = type.__dict__['__mro__'].__get__(cls)
            return mro[2]

        @property
        def __bases__(cls):
            return (*cls.abcs, cls.__base__,)

        def __new__(mcls, *args, **kwds):
            # Sub Python 3.7, the default new uses the wrong constructor
            # for mixins. Since `__new__` effectively ingores the other bases,
            # we can simply remove all but the enumeration bases.
            # This is effectively a hack so we can add all non-abstract methods
            # to the Enum, while also raising a typeerror if any abstractmethods
            # are missing.
            # Validate the bases of our enumeration.
            bases = args[1]
            abcs = tuple((i for i in bases if issubclass(i, abc.ABC)))
            enums = tuple((i for i in bases if issubclass(i, enum.Enum)))
            if len(abcs) + len(enums) != len(bases):
                raise TypeError(f'Cannot instantiate abstract enum with non-abstract bases.')

            # Check abstract methods and add any non-abstract methods present.
            # Add an intermediary derived class so super() uses this, which
            # has all the nonabc methods.
            class derived(*enums):  pass
            for base in abcs:
                add_nonabc(derived, base)

            # Instantiate the superclass
            args = (args[0], (derived,), *args[2:])
            cls = super().__new__(mcls, *args, **kwds)
            for base in abcs:
                check_abstractmethods(cls, base)

            # Need to override how we get the `__mro__` for inheritance checks.
            # We do this through a memoized list of the abstract base classes.
            cls.abcs = abcs
            cls.mro = types.MethodType(lambda x: list(x.__mro__), cls)

            return cls

        def __call__(cls, *args, **kwds):
            if getattr(cls, "__abstractmethods__", None):
                abc_enum_error(cls)
            return super().__call__(*args, **kwds)

else:
    # >= Python 3.7, uses proper __new__ for enum subtype.
    class ABCEnumMeta(abc.ABCMeta, enum.EnumMeta):
        """Abstract metaclass that is both abstract and an enumeration."""

        def __new__(mcls, *args, **kwds):
            cls = super().__new__(mcls, *args, **kwds)
            abstractmethods = getattr(cls, "__abstractmethods__", None)
            if issubclass(cls, enum.Enum) and abstractmethods:
                abc_enum_error(cls)

            return cls

        def __call__(cls, *args, **kwds):
            if getattr(cls, "__abstractmethods__", None):
                abc_enum_error(cls)
            return super().__call__(*args, **kwds)

# MODELS
# ------


class Dto(abc.ABC):
    """
    Classes that can be converted to and from DTO format.

    NEM defines the DTO as a JSON-like format, which is similar to that
    defined in nem2-library-js.
    """

    @abc.abstractmethod
    def to_dto(self):
        """Convert object to DTO-serializable data."""

    def toDto(self):
        return self.to_dto()

    @classmethod
    @abc.abstractmethod
    def from_dto(cls, data):
        """Create object from DTO-serializable data."""

    @classmethod
    def fromDto(cls, data):
        return cls.from_dto(data)


class Catbuffer(abc.ABC):
    """Classes that can be converted to and from catbuffer."""

    @abc.abstractmethod
    def to_catbuffer(self):
        """Serialize object to catbuffer interchange format."""

    def toCatbuffer(self):
        return self.to_catbuffer()

    @classmethod
    @abc.abstractmethod
    def from_catbuffer(cls, data: bytes):
        """Deserialize object from catbuffer interchange format."""

    @classmethod
    def fromCatbuffer(cls, data):
        return cls.from_catbuffer(data)


class Tie(abc.ABC):
    """Simplify the implementation of special methods through `tie()`."""

    @abc.abstractmethod
    def tie(self) -> tuple:
        """Create tuple from fields, for internal use only."""

        return tuple(getattr(self, i) for i in self.__slots__)

    def __repr__(self) -> str:
        name = self.__class__.__name__
        slots = (i.lstrip('_') for i in self.__slots__)
        fields = ', '.join(i + '={!r}' for i in slots)
        string = f'{name}({fields})'
        return string.format(*self.tie())

    def __str__(self) -> str:
        name = self.__class__.__name__
        slots = (i.lstrip('_') for i in self.__slots__)
        fields = ', '.join(i + '={!s}' for i in slots)
        string = f'{name}({fields})'
        return string.format(*self.tie())

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.tie() == other.tie()


class Model(Dto, Catbuffer, Tie):
    """Base class for NEM models."""

    def serialize(self, format: InterchangeFormat):
        """Serialize data to interchange format."""

        return format.serialize(self)

    @classmethod
    def deserialize(cls, data, format: InterchangeFormat):
        """Deserialize data from interchange format."""

        return format.deserialize(data, cls)


# ENUM MODELS
# -----------

def wrap_class(meta, *bases):
    """Wrap existing class to inject bases and a metaclass into the class."""

    class metaclass(type):
        def __new__(cls, name, b, d):
            return meta(name, bases, d)

        @classmethod
        def __prepare__(cls, name, b):
            return meta.__prepare__(name, bases)

    return type.__new__(metaclass, 'tmp', (), {})


def enum_dto(*bases):
    """Create a NEM class that supports the DTO protocol from an enumeration."""

    return wrap_class(ABCEnumMeta, Dto, *bases)


def enum_catbuffer(*bases):
    """Create a NEM class that supports the catbuffer protocol from an enumeration."""

    return wrap_class(ABCEnumMeta, Catbuffer, *bases)


def enum_model(*bases):
    """Create a NEM model from an enumeration."""

    return wrap_class(ABCEnumMeta, Dto, Catbuffer, *bases)
