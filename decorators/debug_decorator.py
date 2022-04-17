"""Module for debug decorator."""
import math
import functools


def debug(func):
    """Print the function arguments and return value."""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  
        signature = ", ".join(args_repr + kwargs_repr)           
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           
        return value
    return wrapper_debug


math.factorial = debug(math.factorial)


@debug
def approximate_exp(num_terms=10):
    return sum(1/math.factorial(num) for num in range(num_terms))


if __name__ == "__main__":
    approximate_exp(5)
