"""Module for timer decorator."""
import functools
import time


def timing_func(func):
    """Prints the runtime of any decorated function."""
    @functools.wraps(func)
    def timer_wrapper(*args, **kwargs):
        # perf_counter is used her to measure time intervals
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        # total run time
        run_time = end_time - start_time
        # printing the repr of the function name and
        # the time in seconds
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return timer_wrapper


@timing_func  # wrapping the function
# function to test the timing_func decorator
def timer_testing(some_num_time):
    for _ in range(some_num_time):
        # creating a list of cubed numbers
        # and adding them up
        sum([i**3 for i in range(10000)])


if __name__ == "__main__":
    timer_testing(1000)
