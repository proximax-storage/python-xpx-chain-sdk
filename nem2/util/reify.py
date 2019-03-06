"""
    reify
    =====

    Data descriptor that memoizes the returned value.

    Function decorator that only makes a single call to the wrapped
    function, replacing any subsequent calls by directly returning
    the stored value.
"""

import functools
import typing


class reify:
    """
    Data descriptor that memoizes the returned value.

    :cvars fget: Wrapped get function.
    :cvars fset: Wrapped property set function (always None).
    :cvars fdel: Wrapped property del function (always None).
    """

    def __init__(self, fget: typing.Any, doc=None):
        """
        :param fget: Getter function.
        """
        self.fget = fget
        self.fset = None
        self.fdel = None
        if doc is not None:
            self.__doc__ = doc
        functools.update_wrapper(self, fget)

    def __get__(self, inst: typing.Any, owner: typing.Any = None):
        # Skip if type is None.
        if inst is None:
            return self

        # Try to return the memoized value, and if not present,
        # call the wrapped function..
        try:
            return getattr(self, "_value")
        except AttributeError:
            value = self.fget(inst)
            setattr(self, "_value", value)
            return value

    def __set__(self, inst: typing.Any, value: typing.Any) -> None:
        raise AttributeError("reified property is read-only.")

    def __delete__(self, inst: typing.Any) -> None:
        raise AttributeError("reified property is read-only.")

    def getter(self, fget: typing.Any) -> 'reify':
        return type(self)(fget, doc=self.__doc__)

    def setter(self, fset: typing.Any) -> 'reify':
        raise AttributeError("reified property is read-only.")

    def deleter(self, fdel: typing.Any) -> 'reify':
        raise AttributeError("reified property is read-only.")
