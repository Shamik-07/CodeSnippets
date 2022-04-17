"""Module for debug decorator."""
import math
import functools


def debug(func):
    """Print the function arguments and return value."""

    @functools.wraps(func)
    def debug_wrapper(*args, **kwargs):
        # repr to get a list of the function arguments
        args_repr = [repr(a) for a in args]
        # repr to get a list of keyword arguments and their
        # corresponding values
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        # Printing the function name and its arguments
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        # the function and their returned values
        print(f"{func.__name__!r} returned {value!r}")
        return value
    return debug_wrapper


# initialising the debug wrapper
# for the math.factorial module.
math.factorial = debug(math.factorial)

# initialising the debug module
# for the exp approximation


@debug
def approximate_exp(num_terms=10):
    """Approximating exponential by adding
    the inverse of n factorials."""

    # returning the approximated exponential
    return sum(1/math.factorial(num) for num in range(num_terms))


if __name__ == "__main__":
    approximate_exp(5)
