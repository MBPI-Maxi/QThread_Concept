import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def ChromeOptions(*chrome_options):
    def wrapper(fn):
        options = Options()

        for option in chrome_options:
            options.add_argument(option)
        
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        def _inner(*args, **kwargs):

            driver = webdriver.Chrome(options=options)
            wait = WebDriverWait(driver, timeout=20)

            return fn(driver, wait, *args, **kwargs)
        return _inner
    return wrapper


@ChromeOptions("--log-level=3")
def test_driver(driver, wait, url):
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(5)
    
    driver.quit()

test_driver("https://pypi.org/project/selenium/")