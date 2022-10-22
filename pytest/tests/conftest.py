import pytest

@pytest.fixture
def input_value():
   input = 39
   return input

@pytest.fixture(scope="session")
def generated_yyyy_mm_dd():
    yyyy, mm, dd = map(int, "1992/09/08".split("/"))
    return yyyy, mm, dd
