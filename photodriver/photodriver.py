from .driver import Driver
from .photos import Photos

COOKIE_FILE = ".cookies"


def photodriver(start_date, stop_date):
    driver = Driver()
    try:
        photos = Photos(driver)
        photos.load_cookies(COOKIE_FILE)
        photos.login()
        photos.save_cookies(COOKIE_FILE)

        count = photos.select_range(start_date, stop_date)
        print(f"Downloaded {count} photos.")
        print(photos.download_selected_photos())

    finally:
        driver.close()
