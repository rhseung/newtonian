from sortedcontainers import SortedDict
from typing import get_type_hints, get_args, get_origin, Callable, Union, Any
from types import UnionType, FunctionType, MethodType
from functools import wraps
from collections.abc import Callable as CallableABC

class DefaultSortedDict(SortedDict):
    def __init__(self, *args, default=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.default = default

    def __missing__(self, key):
        self[key] = self.default
        return self[key]

def isinstance_generic(obj: Any, cls: Any) -> bool:
    """
    An extension of `isinstance` that supports generic types.
    cautions: `obj` does not support lambda expressions. (e.g. `lambda x: x > 0`)

    >>> isinstance_generic(3, int)
    True
    >>> isinstance_generic(3.5, int | float)
    True
    >>> isinstance_generic([3, 3.5, 7], list[int | float])
    True
    >>> isinstance_generic((3, 3.5, 'a'), tuple[int, float, str])
    True
    >>> isinstance_generic({'a': 3, 'b': 3.5}, dict[str, int | float])
    True
    >>> isinstance_generic({3, 3.5}, set[int | float])
    True
    >>> def identity(x: int) -> int: return x
    >>> isinstance_generic(identity, Callable[[int], int])
    True
    >>> isinstance_generic(identity, Callable[[int], float])
    False
    >>> isinstance_generic(3, Any)
    True
    """

    if cls == Any:
        return True

    if (origin := get_origin(cls)) is None or origin == UnionType:
        return isinstance(obj, cls)

    args = get_args(cls)

    if origin is list:
        return isinstance(obj, list) and all(isinstance_generic(e, args[0]) for e in obj)
    elif origin is tuple:
        return isinstance(obj, tuple) and all(isinstance_generic(obj[i], args[i]) for i in range(len(obj)))
    elif origin is dict:
        return isinstance(obj, dict) and all(
            isinstance_generic(k, args[0]) and isinstance_generic(v, args[1]) for k, v in obj.items())
    elif origin is set:
        return isinstance(obj, set) and all(isinstance_generic(e, args[0]) for e in obj)
    elif origin is CallableABC:
        args = *args[0], args[1]
        return isinstance(obj, Callable) and tuple(get_type_hints(obj).values()) == args
    else:
        raise NotImplementedError(f'isinstance_generic not implemented for {origin}')

class TypeHintError(TypeError):
    pass

def type_check(func):
    """
    A decorator that checks the type hints of the arguments and the return value of the function.
    attach this decorator to the function or method which fully have type hints you want to check the type hints.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        hints = get_type_hints(func)    # self argument is not included in the `hints`
        is_method = func.__code__.co_argcount > 0 and func.__code__.co_varnames[0] in ['self', 'cls']

        # `len(hints)` is always 1 more than the `len(args) + len(kwargs)`, because it includes the return type.
        # So, the following expression is satisfied when `len(args)` includes `self`.
        if is_method and not (len(args) + len(kwargs) == len(hints)):
            # this error message counts the number of arguments including `self` which pure python's error message does.
            raise TypeHintError(f'Expected {len(args) + len(kwargs)} arguments, but only {len(hints)} were type-hinted')
        elif not is_method and not (len(args) + len(kwargs) == len(hints) - 1):
            raise TypeHintError(f'Expected {len(args) + len(kwargs)} arguments, but only {len(hints) - 1} were type-hinted')

        for i, (arg, hint) in enumerate(zip(args[int(is_method):], hints.values())):
            if not isinstance_generic(arg, hint):
                raise TypeError(f'Expected {hint} for `{list(hints.keys())[i]}`, but got {type(arg)}')

        for arg, value in kwargs.items():
            if arg not in hints:
                raise TypeHintError(f'No type-hinted argument {arg}')
            if not isinstance_generic(value, hints[arg]):
                raise TypeError(f'Expected {hints[arg]} for `{arg}`, but got {type(value)}')

        return_value = func(*args, **kwargs)

        if not isinstance_generic(return_value, hints['return']):
            raise TypeError(f'Expected {hints["return"]} for return type, but got {type(return_value)}')

        return return_value

    return wrapper

@type_check
def f(x: int, y: float, z: int = 3) -> int | float:
    return x + y + z

class A:
    def __init__(self, x: int) -> None:
        self.x = x

    @type_check
    def __add__(self, other: 'A') -> int:
        return self.x + other.x

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(x={self.x})'

print(f(3, 4.5))
# FIXME: Expected 2 arguments, but only 3 were type-hinted
