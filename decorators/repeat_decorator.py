"""Module for creating a decorator, which works with/without
an argument. This decorator repeats the function any number of times
or just once."""

import functools


def repeat_func(_func=None, *, num_times=1):
    """Repeating a function once/any number of times.
    This function works with or without the kwarg num_times.
    """
    def repeat_decorator(func):
        """Wrapper function for repeating the function.
        This will create function object for the repeat_func.
        As we reserve the repeat_func for using it as a decorator,
        and it requires arguments, this function is required."""

        @functools.wraps(func)
        def repeat_wrapper(*args, **kwargs):
            # repeating function n number of times
            # but returning only the function value once
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return repeat_wrapper

# The parameter _func takes two values, either None, when there's
# num_times provided otherwise the decorator function being
# passed to _func.
    if _func is None:
        return repeat_decorator
    else:
        return repeat_decorator(_func)


@repeat_func
def say_hi_once():
    """Python says hi to you! 😀"""
    print('Hello there! 😀')
    return {'H': 0, 'e': 1, 'l': 2, 'l': 3, 'o': 4}


@repeat_func(num_times=3)
def say_hi_thrice():
    """Python says hi to you! 😀"""
    print('Hello there! 😀')
    return {'H': 0, 'e': 1, 'l': 2, 'l': 3, 'o': 4}


if __name__ == "__main__":
    print('Saying hi once.')
    say_hi_once()
    print()
    print('Saying hi thrice.')
    say_hi_thrice()
