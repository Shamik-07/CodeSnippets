import pickle
from argparse import Namespace
from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def input_value():
    input = 39
    yield input
    print("***executing after yield statement as a tear down***")
    del input


@pytest.fixture(scope="session")
def generated_yyyy_mm_dd():
    yyyy, mm, dd = map(int, "1992/09/08".split("/"))
    yield yyyy, mm, dd
    print("***executing after yield statement as a tear down***")
    del yyyy, mm, dd


# The below fixture is required when a function needs argparse arguments
# this will automatically give these files by writing the content passed
# through @pytest.mark.parametrize, which is accepted by the below function's
# pytest.FixtureRequest and remove them after the test has been completed
# pytest.FixtureRequest allows to pass in data before running the tests through
# @pytest.mark.parametrize
@pytest.fixture(scope="function")
def setup_files(
    tmp_path: Path, request: pytest.FixtureRequest
) -> Generator[Namespace, None, None]:
    some_random_filepath = tmp_path / "some_random.pkl"
    another_random_filepath = tmp_path / "another_random.pkl"

    some_random_data = request.param.get("some_random_data", {})
    another_random_data = request.param.get("another_random_data", {})

    with open(file=some_random_filepath, mode="wb") as f:
        pickle.dump(obj=some_random_data, file=f)
    with open(file=another_random_filepath, mode="wb") as f:
        pickle.dump(obj=another_random_data, file=f)

    yield Namespace(
        some_random_filepath=some_random_filepath.as_posix(),
        another_random_filepath=another_random_filepath.as_posix(),
    )
