from datetime import date

# from hamcrest import assert_that, is_
import pytest
from unittest.mock import Mock, patch

from photodriver.checkbox import Checkbox
from photodriver.driver import Driver
from photodriver.photos import Photos


def CheckboxMock(date):
    return Mock(Checkbox, element=Mock(), label=f"checkbox {date}", date=date)


@pytest.fixture
def checkboxes():
    return [
        CheckboxMock(date(2019, 11, 5)),
        CheckboxMock(date(2019, 11, 4)),
        CheckboxMock(date(2019, 11, 3)),
        CheckboxMock(date(2019, 11, 2)),
        CheckboxMock(date(2019, 11, 1)),
    ]


@patch("photodriver.photos.PhotoScroller", autospec=True, spec_set=True)
class TestSelectRange:
    def test_all_photos_are_selected_if_dates_are_unspecified(
        self, PhotoScroller, checkboxes
    ):
        driver = Mock(Driver)
        PhotoScroller(driver).get_visible_checkboxes.return_value = checkboxes
        PhotoScroller(driver).to_top.return_value = checkboxes[0]
        PhotoScroller(driver).to_bottom.return_value = checkboxes[-1]

        photos = Photos(driver)
        photos.select_range(None, None)

        checkboxes[-1].click.assert_called()
        checkboxes[0].shift_click.assert_called()

    def test_photos_are_selected_between_two_dates(self, PhotoScroller, checkboxes):
        driver = Mock(Driver)
        PhotoScroller(driver).get_visible_checkboxes.return_value = checkboxes
        PhotoScroller(driver).to_top.return_value = checkboxes[0]
        PhotoScroller(driver).to_bottom.return_value = checkboxes[-1]

        def find_last_matching_checkbox(date):
            matches = [checkbox for checkbox in checkboxes if checkbox.date == date]
            return matches[-1]

        PhotoScroller(driver).up_to_checkbox.side_effect = find_last_matching_checkbox

        photos = Photos(driver)
        photos.select_range(date(2019, 11, 2), date(2019, 11, 4))

        checkboxes[3].click.assert_called()
        checkboxes[2].shift_click.assert_called()
