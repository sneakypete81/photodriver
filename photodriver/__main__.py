"""
Download Google Photos from your browser using Selenium Webdriver.
"""
import sys
import argparse
from datetime import date
from dateutil.parser import parse
from selenium import webdriver

from .photos import Photos

COOKIE_FILE = ".cookies"


def main():
    photodriver(**parse_arguments())


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


def photodriver(start_date, stop_date):
    photos = Photos()

    profile = webdriver.FirefoxProfile()
    for preference in photos.get_firefox_preferences():
        profile.set_preference(*preference)

    driver = webdriver.Firefox(profile)
    try:
        photos.set_driver(driver)
        photos.load_cookies(COOKIE_FILE)
        photos.login()
        photos.save_cookies(COOKIE_FILE)

        photos.select_all()
        print(photos.download_selected_photos())

    finally:
        driver.close()


if __name__ == "__main__":
    main()
