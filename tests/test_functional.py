from pathlib import Path

from hamcrest import assert_that, only_contains, has_properties, has_length
import pytest

import photodriver
from photodriver.driver import Driver
from photodriver.photos import Photos

TEST_COOKIE_FILE = ".test-cookies"

PASSWORD = (Path(__file__).parent / ".functional.password").read_text().strip()


@pytest.fixture(scope="module")
def logged_in_driver():
    """Create a single driver object to be used for all tests in the module."""
    driver = Driver()
    driver_close = driver.close
    driver.close = lambda: None
    try:
        photos = Photos(driver)
        photos.login("photodriver.test@gmail.com", PASSWORD)
        yield driver
    finally:
        driver_close()


@pytest.fixture()
def patched_driver(logged_in_driver, monkeypatch):
    """Monkeypatch the Driver class to use our test driver."""
    monkeypatch.setattr(photodriver.photodriver, "Driver", lambda: logged_in_driver)


@pytest.mark.functional
class TestFunctional:
    def test_download_all(self, tmp_path, patched_driver):
        photodriver.run(
            output_path=tmp_path,
            start_date=None,
            stop_date=None,
            cookie_file=TEST_COOKIE_FILE,
        )
        files = list(tmp_path.iterdir())

        assert_that(files, has_length(37))
        assert_that(files, only_contains(has_properties(suffix=".jpg")))
