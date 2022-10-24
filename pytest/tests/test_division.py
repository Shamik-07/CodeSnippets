import pytest

def test_divisible_by_3(input_value):
   assert input_value % 3 == 0

def test_divisible_by_6(input_value):
    with pytest.raises(AssertionError):
        assert input_value % 6 == 0

def test_divisible_by_13(input_value):
   assert input_value % 13 == 0
