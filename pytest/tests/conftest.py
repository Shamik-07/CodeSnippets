import pytest

@pytest.fixture(scope="session")
def input_value():
   input = 39
   yield input
   print("executing after yield statement as a tear down")
   del input

@pytest.fixture(scope="session")
def generated_yyyy_mm_dd():
    yyyy, mm, dd = map(int, "1992/09/08".split("/"))
    yield yyyy, mm, dd
    print("executing after yield statement as a tear down")
    del yyyy, mm, dd
