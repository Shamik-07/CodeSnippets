"""Module for creating a decorator, which works with/without
an argument. This decorator repeats the function any number of times
or just once."""

import functools

def repeat_func(_func=None, *, num_times=1):
    def repeat_decorator(func):
        @functools.wraps(func)
        def repeat_wrapper(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return repeat_wrapper

    if _func is None:
        return repeat_decorator
    else:
        return repeat_decorator(_func)