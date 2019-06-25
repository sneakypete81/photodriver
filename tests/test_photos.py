from datetime import date
# from hamcrest import assert_that, is_
import pytest
from unittest.mock import Mock, patch

from photodriver.checkbox import Checkbox
from photodriver.driver import Driver
from photodriver.photos import Photos


@pytest.fixture
def checkboxes():
    return [
        Mock(Checkbox, element=Mock(), label="checkbox1", date=date(2019, 11, 5)),
        Mock(Checkbox, element=Mock(), label="checkbox2", date=date(2019, 11, 4)),
        Mock(Checkbox, element=Mock(), label="checkbox3", date=date(2019, 11, 3)),
        Mock(Checkbox, element=Mock(), label="checkbox4", date=date(2019, 11, 2)),
        Mock(Checkbox, element=Mock(), label="checkbox5", date=date(2019, 11, 1)),
    ]


class TestSelectRange:
    @patch("photodriver.photos.PhotoScroller", autospec=True, spec_set=True)
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
