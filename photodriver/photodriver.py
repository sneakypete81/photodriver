from .driver import Driver
from .photos import Photos

DEFAULT_COOKIE_FILE = ".cookies"


def run(start_date, stop_date, cookie_file=None):
    if cookie_file is None:
        cookie_file = DEFAULT_COOKIE_FILE

    driver = Driver()
    try:
        photos = Photos(driver)
        photos.load_cookies(cookie_file)
        photos.login()
        photos.save_cookies(cookie_file)

        count = photos.select_range(start_date, stop_date)
        print(f"Downloaded {count} photos.")
        print(photos.download_selected_photos())

    finally:
        driver.close()
