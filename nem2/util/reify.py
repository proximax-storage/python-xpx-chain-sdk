"""
    reify
    =====

    Data descriptor that memoizes the returned value.

    Function decorator that only makes a single call to the wrapped
    function, replacing any subsequent calls by directly returning
    the stored value.

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
import functools


class reify:
    """
    Data descriptor that memoizes the returned value.

    :ivars fget: Wrapped property get function.
    :ivars fset: Wrapped property set function (always None).
    :ivars fdel: Wrapped property del function (always None).
    """

    def __init__(self, fget=None, key=None, doc=None):
        """
        :param fget: Getter function.
        """
        self.fget = fget
        self._key = key or "_{}_".format(fget.__name__)
        if doc is not None:
            self.__doc__ = doc

        # Update signature and annotations.
        if fget is not None:
            functools.update_wrapper(self, fget)
            self.__get__.__func__.__annotations__ = fget.__annotations__

    @property
    def fset(self):
        return None

    @property
    def fdel(self):
        return None

    def __get__(self, inst, owner=None):
        if self.fget is None:
            raise AttributeError('unreadable attribute')
        # Skip if type is None.
        if inst is None:
            return self

        # Try to return the memoized value, and if not present,
        # call the wrapped function.
        try:
            return getattr(inst, self._key)
        except AttributeError:
            value = self.fget(inst)
            setattr(inst, self._key, value)
            return value

    def __set__(self, inst, value):
        raise TypeError("reified property is read-only.")

    def __delete__(self, inst):
        raise TypeError("reified property is read-only.")

    def getter(self, fget):
        return type(self)(fget, key=self._key, doc=self.__doc__)

    def setter(self, fset):
        raise TypeError("reified property is read-only.")

    def deleter(self, fdel):
        raise TypeError("reified property is read-only.")
