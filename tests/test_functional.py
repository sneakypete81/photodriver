import pytest

import photodriver

TEST_COOKIE_FILE = ".test-cookies"


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
