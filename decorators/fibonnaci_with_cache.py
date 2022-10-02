"""This decorator stores previously calculated results,
which are used in future calculations."""

import functools


@functools.lru_cache(maxsize=4)
def fibonacci(num):
    # print(f"Calculating fibonacci({num})")
    if num < 2:
        return num
    return fibonacci(num - 1) + fibonacci(num - 2)


if __name__ == "__main__":

    print("Calculating Fibonacci 1 \n", fibonacci(1))
    print("Using the cache to calculate Fibonacci"
          " of 5. \n", fibonacci(5))
    print("Calculating a large Fibonacci. \n", fibonacci(128))
