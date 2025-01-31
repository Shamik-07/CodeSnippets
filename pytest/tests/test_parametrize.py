from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path

from calc import calc, read_pickle_data

import pytest


@dataclass
class CalcCase:
    name: str
    a: int
    b: int
    result: int
    op: str = "+"


# by stacking the parametrize operation, we get all the combinations
@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("b", [3, 4])
def test_permutations(a, b):
    assert calc(a, b, "+") == a + b


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 1, 2),
        (1, 2, 3),
        (2, 3, 5),
    ],
)
def test_add(a, b, expected):
    assert calc(a, b, "+") == expected

@pytest.mark.parametrize("op", ["+", "-", "*", "/", "**"])
def test_smoke(op):
    if op == "**":
        pytest.xfail(reason="Invalid operator")
    calc(1, 2, op)


@pytest.mark.parametrize(
    "a, b, op, expected",
    [
        pytest.param(
            2,
            3,
            "**",
            8,
            marks=pytest.mark.xfail(reason="..."),
        ),
        (1, 2, "+", 3),
        (3, 1, "-", 5),
    ],
)
def test_calc(a, b, op, expected):
    assert calc(a, b, op) == expected


@pytest.mark.parametrize(
    "tc",
    [
        CalcCase("add", a=1, b=2, result=3),
        CalcCase("add-neg", a=-2, b=-3, result=-5),
        CalcCase("sub", a=2, b=1, op="-", result=1),
    ],
    ids=lambda tc: tc.name,
)
def test_calc(tc):
    assert calc(tc.a, tc.b, tc.op) == tc.result


# The indirect=true passes the data to the setup_files function
# instead of the test_read_pickle_data function directly
@pytest.mark.parametrize(
    "setup_files",
    [
        {
            "some_random_filepath": {
                "google": "Google",
                "apple": "Apple",
                "samsung": "Samsung",
            },
            "another_random_filepath": {
                "google": ["google"],
                "apple": ["apple inc.", "apple"],
                "microsoft": ["microsoft"],
                "samsung": ["samsung"],
            },
        },
    ],
    indirect=True,
)
def test_read_pickle_data(setup_files: Namespace) -> None:
    args = setup_files
    read_pickle_data(args=args)
    assert (
        Path(args.some_random_filepath).exists()
        or Path(args.another_random_filepath).exists()
    )
