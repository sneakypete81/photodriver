from datetime import date
import pytest

from .test_images import photo_list


def pytest_addoption(parser):
    parser.addoption(
        "--functional", action="store_true", default=False, help="run functional tests"
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "functional: only run test when --functional is specified"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--functional"):
        return

    skip = pytest.mark.skip(
        reason="only run functional tests when --functional is specified"
    )
    for item in items:
        if "functional" in item.keywords:
            item.add_marker(skip)


def pytest_generate_tests(metafunc):
    has_date_range = "date_range" in metafunc.fixturenames
    has_expected_filenames = "expected_filenames" in metafunc.fixturenames
    if has_date_range and has_expected_filenames:
        generate_functional_tests(metafunc)


def generate_functional_tests(metafunc):
    fixed_tests = [
        ((None, None), photo_list.FILENAMES),
        ((date(1990, 1, 1), date(2050, 1, 1)), photo_list.FILENAMES),
        ((None, date(2018, 1, 1)), []),
        ((None, date(2018, 1, 2)), photo_list.FILENAMES[0:2]),
    ]

    random_tests = create_random_functional_tests()

    all_tests = fixed_tests + random_tests

    metafunc.parametrize(
        argnames=["date_range", "expected_filenames"],
        argvalues=all_tests,
        ids=[str(test[0]) for test in all_tests],
    )


def create_random_functional_tests():
    return []
