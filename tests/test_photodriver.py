from datetime import date
from hamcrest import assert_that, is_

from photodriver.__main__ import parse_arguments


class TestParseArguments:
    def test_dates_default_to_none(self):
        options = parse_arguments([])

        assert_that(options["start_date"], is_(None))
        assert_that(options["stop_date"], is_(None))

    def test_date_are_parsed_correctly(self):
        options = parse_arguments(
            ["--start", "23 jan 2016", "--stop", "19 December 2001"]
        )

        assert_that(options["start_date"], is_(date(2016, 1, 23)))
        assert_that(options["stop_date"], is_(date(2001, 12, 19)))

    def test_dates_use_first_of_month_when_not_specified(self):
        options = parse_arguments(
            ["--start", "January 2000", "--stop", "February 2011"]
        )

        assert_that(options["start_date"], is_(date(2000, 1, 1)))
        assert_that(options["stop_date"], is_(date(2011, 2, 1)))

    def test_dates_use_current_year_when_not_specified(self):
        current_year = date.today().year
        options = parse_arguments(["--start", "July", "--stop", "23 November"])

        assert_that(options["start_date"], is_(date(current_year, 7, 1)))
        assert_that(options["stop_date"], is_(date(current_year, 11, 23)))
