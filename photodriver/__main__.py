"""
Download Google Photos from your browser using Selenium Webdriver.
"""
import sys
import argparse
from datetime import date
from dateutil.parser import parse

from . import photodriver


def main():
    photodriver.run(**parse_arguments())


def parse_arguments(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--start",
        default=None,
        help="Start downloading from this date (default: no limit)",
    )
    parser.add_argument(
        "--stop", default=None, help="Stop downloading at this date (default: no limit)"
    )

    options = parser.parse_args(args)

    current_year = date.today().year
    if options.start is not None:
        options.start = parse(options.start, default=date(current_year, 1, 1))
    if options.stop is not None:
        options.stop = parse(options.stop, default=date(current_year, 1, 1))

    return dict(start_date=options.start, stop_date=options.stop)


if __name__ == "__main__":
    main()
