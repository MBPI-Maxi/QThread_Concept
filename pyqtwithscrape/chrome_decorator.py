from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from functools import wraps
import os

# THIS IS FOR THE CLASS ONLY
def chrome_decorator(
        *chrome_options,
        timeout=20,
    ):
    def _wrapper(fn):
        options = Options()

        for option in chrome_options:
            options.add_argument(option)
        
        service = Service(log_output=os.devnull)

        @wraps(fn)
        def _inner(self, *args, **kwargs):
            driver = webdriver.Chrome(options=options, service=service)
            
            wait = WebDriverWait(driver, timeout=timeout)

            return fn(self, driver, wait, *args, **kwargs)
        return _inner
    return _wrapper
