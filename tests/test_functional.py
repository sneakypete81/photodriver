from pathlib import Path

from hamcrest import assert_that, is_
import pytest

import photodriver
from photodriver.driver import Driver
from photodriver.photos import Photos
from .test_images import photo_list

TEST_COOKIE_FILE = ".test-cookies"

PASSWORD = (Path(__file__).parent / ".functional.password").read_text().strip()


@pytest.fixture(scope="module")
def logged_in_driver():
    """Create a single driver object to be used for all tests in the module."""
    driver = Driver()
    driver_close = driver.close
    driver.close = driver.clear_download_dir
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
@pytest.mark.parametrize(
    "date_range, expected_filenames", [((None, None), photo_list.FILENAMES)]
)
class TestFunctional:
    def test_download_all(
        self, tmp_path, patched_driver, date_range, expected_filenames
    ):
        photodriver.run(
            output_path=tmp_path,
            start_date=date_range[0],
            stop_date=date_range[1],
            cookie_file=TEST_COOKIE_FILE,
        )
        filenames = [f.name for f in tmp_path.iterdir()]

        assert_that(sorted(filenames), is_(expected_filenames))
