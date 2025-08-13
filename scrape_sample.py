import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.remote.webdriver import WebDriver

def ChromeOptions(*chrome_options):
    def wrapper(fn):
        options = Options()

        for option in chrome_options:
            options.add_argument(option)
        
        # to suppress the logs being generated automatically
        service = Service(log_output="")

        # for class instance
        def _inner(self, *args, **kwargs):

            driver = webdriver.Chrome(options=options, service=service)
            wait = WebDriverWait(driver, timeout=20)

            return fn(self, driver, wait, *args, **kwargs)
        return _inner
    return wrapper


class DriverInstance():
    @ChromeOptions()
    def test_driver(
        self, 
        driver: WebDriver, 
        wait: WebDriverWait,
        url: str
    ) -> None:
        driver.get(url)
        

        time.sleep(3)
        driver.quit()

instance = DriverInstance()
instance.test_driver("https://pypi.org/project/selenium/")
