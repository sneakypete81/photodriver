from selenium import webdriver

from .photos import Photos

COOKIE_FILE = ".cookies"


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
