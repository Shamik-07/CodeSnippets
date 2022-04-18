'''This uses a static enclosure i.e. the exponent
argument of the `raise_number_to` function doesn't change.
Module to calculate power of a number.'''


def raise_number_to(exponent):
    """Choose the exponent to raise the number to."""

    def power(base):
        """The number to raise the power to."""
        return base ** exponent

    return power


if __name__ == "__main__":
    print('Generating power of 2 for number 4.')
    power_of_two = raise_number_to(2)
    print(power_of_two(4))

    print('Generating power of 3 for number 2.')
    power_of_three = raise_number_to(3)
    print(power_of_three(2))
