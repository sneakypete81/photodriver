import pytest


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
