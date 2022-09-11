from multiprocessing import Pool, TimeoutError
import time
import os

def f(x):
    return x*x

if __name__ == '__main__':
    # start 4 worker processes
    with Pool(processes=4) as pool:

        # print "[0, 1, 4,..., 81]"
        print("The list of numbers for which"
             " the squared numbers are to be calculated.")
        print([i for i in range(10)])
        print("Pool Map")
        print(pool.map(f, range(10)))

        # print same numbers in arbitrary order
        print("Pool imap, processes the number in arbitrary order")
        for i in pool.imap_unordered(f, range(10)):
            print(i)

        # evaluate "f(20)" asynchronously
        print("Pool apply async for one single number 20"
        " and returns the result after waiting for 1 sec.")
        res = pool.apply_async(f, (20,))      # runs in *only* one process
        print(res.get(timeout=1))             # prints "400", the timeout arg asks to wait for 1 sec 
        # before retrieving the result

        # evaluate "os.getpid()" asynchronously
        print("Pool apply async"
        " and returns the pid waiting for 1 sec.")
        res = pool.apply_async(os.getpid, ()) # runs in *only* one process
        print(res.get(timeout=1))             # prints the PID of that process

        # launching multiple evaluations asynchronously *may* use more processes
        print("Pool apply async for 4 numbers"
        " and returns each pid after waiting for 1 sec.")
        multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
        print([res.get(timeout=1) for res in multiple_results])

        # make a single worker sleep for 10 secs
        print("Purposely waiting to process after 10 sec"
        " however, we want the result after waiting for 1 sec."
        "This will raise an error of course.")
        res = pool.apply_async(time.sleep, (10,))
        try:
            print(res.get(timeout=1))
        except TimeoutError:
            print("We lacked patience and got a multiprocessing.TimeoutError")

        print("For the moment, the pool remains available for more work")

    # exiting the 'with'-block has stopped the pool
    print("Now the pool is closed and no longer available")