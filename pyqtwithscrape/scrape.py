from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from pyqtwithscrape.chrome_decorator import chrome_decorator as CDecorator
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

class Scraper(): 
    @CDecorator("--headless")
    def init_scrape(
        self,
        driver: WebDriver,
        wait: WebDriverWait,
        url: str
    ):
        # element string to send keys
        element_string_to_send = "Tangina mo francis"

        driver.get(url)
        tuple_element = (By.CSS_SELECTOR, ".gLFyf")
        input_element_find = wait.until(
            EC.visibility_of_element_located(tuple_element)
        )

        for char in element_string_to_send:
            input_element_find.send_keys(char)
            time.sleep(0.03)
        
        time.sleep(3)
        driver.quit()

instance = Scraper()
instance.init_scrape(url="https://www.google.com/")