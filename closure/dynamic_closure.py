'''
Module to calculate the mean of a stream of numbers.

This uses a dynamic enclosure
i.e. `mean_of_a_stream_of_numbers` doesn't take any argument.

The closure assigned to calc_mean retains the state of arg_ls
between successive calls.
Even though you define arg_ls in mean_of_a_stream_of_numbers(),
it’s still available in the closure, so you can modify it.
In this case, arg_ls works as kind of dynamic enclosing state.
'''


def mean_of_a_stream_of_numbers():
    """Mean of a stream of numbers."""
    arg_ls = []

    def mean_of_num(number):
        """Calculate the mean of the numbers
        considering all the preceeding numbers."""
        arg_ls.append(number)
        return sum(arg_ls)/len(arg_ls)
    return mean_of_num


if __name__ == "__main__":
    calc_mean = mean_of_a_stream_of_numbers()
    print('Mean of 100')
    print(calc_mean(100))

    print('Mean of 100 & 110')
    print(calc_mean(110))

    print('Mean of 100, 110 & 115')
    print(calc_mean(115))
