"""
    reify
    =====

    Data descriptor that memoizes the returned value.

    Function decorator that only makes a single call to the wrapped
    function, replacing any subsequent calls by directly returning
    the stored value.
"""

import functools


class reify:
    """
    Data descriptor that memoizes the returned value.

    :cvars fget: Wrapped get function.
    :cvars fset: Wrapped property set function (always None).
    :cvars fdel: Wrapped property del function (always None).
    """

    def __init__(self, fget, key=None, doc=None):
        """
        :param fget: Getter function.
        """
        self.fget = fget
        self._key = key or "_{}_".format(fget.__name__)
        if doc is not None:
            self.__doc__ = doc

        # Update signature and annotations.
        functools.update_wrapper(self, fget)
        self.__get__.__func__.__annotations__ = fget.__annotations__

    @property
    def fset(self):
        return None

    @property
    def fdel(self):
        return None

    def __get__(self, inst, owner=None):
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
