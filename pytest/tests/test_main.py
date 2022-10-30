"""Pytest Tutorial"""
import pytest
import datetime
import sys
import time

def increment_by_1(x):
    x += 1
    return x

def increment_by_2(x):
    pass

def get_age(yyyy:int, mm:int, dd:int) -> int:
    dob = datetime.date(yyyy, mm, dd)
    today = datetime.date.today()
    age = round((today - dob).days / 365)
    return age

def test_get_age():
    yyyy, mm, dd = map(int, "1992/09/08".split("/"))
    assert get_age(yyyy, mm, dd) == 30

# PYTEST FIXTURE
# the fixture for this is in conftest.py
def test_get_age_w_fixture(generated_yyyy_mm_dd):
    yyyy, mm, dd = generated_yyyy_mm_dd
    assert get_age(yyyy, mm, dd) == 30

# the fixture for this is in conftest.py
def test_get_age_w_fixture_raise_error(generated_yyyy_mm_dd):
    yyyy, mm, dd = generated_yyyy_mm_dd
    with pytest.raises(AssertionError):
        assert get_age(yyyy, mm, dd) == 31

# Pytest parameterise
# If we would like to run a single test with multiple inputs
@pytest.mark.parametrize(
    "test_input, expected_output", 
    [
        (1, 2),
        (0, 1),
        (-1, 0),
        (9, 10)
    ]
)
def test_increment_by_1_w_multiple_inputs(test_input, expected_output):
    assert increment_by_1(test_input) == expected_output


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, 2),
        pytest.param(1, 0, marks=pytest.mark.xfail),
        pytest.param(1, 3, marks=pytest.mark.xfail(reason="***some bug***")),
        (2, 3),
        (3, 4),
        (4, 5),
        pytest.param(
            1, 0, marks=pytest.mark.skip(reason="***this is just an illustration***")
        ),
        pytest.param(
            10, 11, marks=pytest.mark.skipif(sys.version_info >= (3, 0),
                                             reason="***needs to run on python2***")
        ),
    ],
)
def test_increment_w_params_in_parametrize(n, expected):
    assert n + 1 == expected

@pytest.mark.xfail
def test_increment_by_2():
    assert increment_by_2(1) == 3

def test_increment_by_1_passes():
  assert increment_by_1(1) == 2

# checking whether an AssertionError is raised
def test_increment_by_1_fail():
    with pytest.raises(AssertionError):
        assert increment_by_1(1) == -1

# another test to check whether a ZeroDivisionError is raised
def test_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        1/0

@pytest.mark.skip
def test_skip():
    assert 1 ==1

@pytest.mark.skipif(sys.version_info >= (3, 0),
reason ="***needs to run on python2***")
def test_skipif():
    assert 1 == 1

# this is a custom marker
@pytest.mark.others
def test_others():
    print("***we can tun this specific test with a \"others\" marker***")
    assert not 0 == None

def test_my_name():
    print("***something bogus***")
    assert 0 == 0


# mocking tests with pytest-mock
def is_windows():
    time.sleep(2)
    return True

def get_operating_system():
    return "Windows" if is_windows() else "Linux"

@pytest.mark.application_tests
def test_get_operating_system():
    start_time = time.perf_counter()
    assert get_operating_system() == "Windows"
    print(f"total time(s): {time.perf_counter()-start_time}")

@pytest.mark.application_tests
def test_get_operating_system_mocked(mocker):
    # Mock the operatng system function and return True always
    mocker.patch('test_main.is_windows', return_value=True)
    start_time = time.perf_counter()
    assert get_operating_system() == 'Windows'
    print(f"total time(ms): {(time.perf_counter()-start_time)*1e3}")

@pytest.mark.application_tests
def test_operation_system_is_linux_mocked(mocker):
    # Mock the operatng system function and return False for testing Linux
    mocker.patch('test_main.is_windows', return_value=False) 
    start_time = time.perf_counter()
    assert get_operating_system() == 'Linux'
    print(f"total time(ms): {(time.perf_counter()-start_time)*1e3}")






