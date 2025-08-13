import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

def ChromeOptions(*chrome_options):
    def wrapper(fn):
        options = Options()
        for option in chrome_options:
            options.add_argument(option)

        # Suppress ChromeDriver logs
        service = Service(log_output="")

        def _inner(self, *args, **kwargs):
            driver = webdriver.Chrome(options=options, service=service)
            wait = WebDriverWait(driver, timeout=20)
            return fn(self, driver, wait, *args, **kwargs)

        return _inner
    return wrapper


class DriverInstance:
    @ChromeOptions("--log-level=3")
    def test_driver(self, driver, wait, url):
        driver.get(url)
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    # Read URL from command line argument or use default
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "https://pypi.org/project/selenium/"

    instance = DriverInstance()
    instance.test_driver(url)

# .bat example
# @echo off
# python scrape.py https://www.example.com
# pause

# pyqt6 process
# import subprocess
# from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QLineEdit

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Scraper Launcher")

#         layout = QVBoxLayout(self)
#         self.url_input = QLineEdit()
#         self.url_input.setPlaceholderText("Enter URL to scrape")
#         layout.addWidget(self.url_input)

#         btn = QPushButton("Run Scraper")
#         btn.clicked.connect(self.run_scraper)
#         layout.addWidget(btn)

#     def run_scraper(self):
#         url = self.url_input.text().strip()
#         if url:
#             subprocess.Popen(["python", "scrape.py", url])
#         else:
#             subprocess.Popen(["python", "scrape.py"])  # default URL

# if __name__ == "__main__":
#     app = QApplication([])
#     win = MainWindow()
#     win.show()
#     app.exec()
