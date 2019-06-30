import pytest

from photodriver import photodriver

TEST_COOKIE_FILE = ".test-cookies"


@pytest.mark.functional
class TestFunctional:
    def test_download_all(self):
        photodriver(start_date=None, stop_date=None, cookie_file=TEST_COOKIE_FILE)
