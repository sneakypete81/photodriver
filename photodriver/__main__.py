from selenium import webdriver

from .photos import Photos

COOKIE_FILE = ".cookies"


def main():
    driver = webdriver.Firefox(firefox_profile="photodriver")

    try:
        photos = Photos(driver)

        photos.load_cookies(COOKIE_FILE)
        photos.login()
        photos.save_cookies(COOKIE_FILE)

    finally:
        driver.close()


if __name__ == "__main__":
    main()
