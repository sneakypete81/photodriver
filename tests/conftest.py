from datetime import date, timedelta
import pytest
import random

from .test_images import photo_list


def pytest_addoption(parser):
    parser.addoption("--functional", action="store_true", help="run functional tests")
    parser.addoption("--seed", default=None, help="random seed for functional tests")
    parser.addoption(
        "--headless", action="store_true", help="Run functional tests in headless mode"
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
        ((None, date(2018, 1, 1)), []),
        ((None, date(2018, 1, 2)), photo_list.FILENAMES[0:2]),
        ((date(2018, 6, 1), None), []),
        ((date(2018, 5, 31), None), [photo_list.FILENAMES[-1]]),
    ]

    seed = metafunc.config.getoption("--seed")
    random_tests = create_random_functional_tests(seed)

    all_tests = fixed_tests + random_tests

    metafunc.parametrize(
        argnames=["date_range", "expected_filenames"],
        argvalues=all_tests,
        ids=[str(test[0]) for test in all_tests],
    )


def create_random_functional_tests(seed):
    if seed is None:
        seed = random.randint(0, 10000)

    print(f"Using --seed={seed}")
    random.seed(seed)

    return [create_random_functional_test() for i in range(10)]


def create_random_functional_test():
    start_date = get_random_photo_date()
    stop_date = get_random_photo_date()
    if start_date > stop_date:
        start_date, stop_date = stop_date, start_date

    date_range = (start_date, stop_date)

    expected_filenames = []
    for i, photo_date in enumerate(photo_list.DATES):
        if photo_date >= start_date and photo_date < stop_date:
            expected_filenames.append(photo_list.FILENAMES[i])

    return (date_range, expected_filenames)


def get_random_photo_date():
    index = random.randint(0, len(photo_list.DATES) - 1)
    date = photo_list.DATES[index]

    offset = random.randint(-1, 1)
    return date + timedelta(days=offset)
