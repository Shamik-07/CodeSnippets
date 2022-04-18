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

if __name__=="__main__":
    @repeat_func
    def say_hi():
        """Python says hi to you! 😀"""
        print('Hello there! 😀')
        return {'H':0,'e':1,'l':2,'l':3,'o':4}
    
    @repeat_func(num_times=3)
    def say_hi():
        """Python says hi to you! 😀"""
        print('Hello there! 😀')
        return {'H':0,'e':1,'l':2,'l':3,'o':4}