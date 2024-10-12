import pytest
from dataclasses import dataclass
from calc import calc


@dataclass
class CalcCase:
    name: str
    a: int
    b: int
    result: int
    op: str = "+"




@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 3),
    (1, 2, 3),
    (2, 3, 5),
])

# by stacking the parametrize operation, we get all the combinations
@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("b", [3, 4])
def test_permutations(a, b):
    assert calc(a, b, "+") == a + b

def test_add(a, b, expected):
    assert calc(a, b, "+") == expected

@pytest.mark.parametrize(
    "op", ["+", "-", "*", "/", "**"])
def test_smoke(op):
    calc(1, 2, op)


@pytest.mark.parametrize(
    "a, b, op, expected", [
    pytest.param(
        2, 3, "**", 8,
        marks=pytest.mark.xfail(reason="..."),
    ),
    (1, 2, "+", 3),
    (3, 1, "-", 5),
])
def test_calc(a, b, op, expected):
    assert calc(a, b, op) == expected


@pytest.mark.parametrize("tc", [
CalcCase("add", a=1, b=2, result=3),
CalcCase("add-neg", a=-2, b=-3, result=-5),
CalcCase("sub", a=2, b=1, op="-", result=1),
], ids=lambda tc: tc.name)
def test_calc(tc):
    assert calc(tc.a, tc.b, tc.op) == tc.result