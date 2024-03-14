import os
import pathlib

import undetected_chromedriver as uc

from selenium import webdriver
from selenium_stealth import stealth
from urllib3.util import url
from webdriver_manager.firefox import GeckoDriverManager

from settings import cfg

try:
    gecko_pth = "./geckodriver"
except Exception as e:
    gecko_pth = GeckoDriverManager().install()
    print(e)


class WebDriver:
    def __init__(self, tag: str = "firefox", download_directory=None):
        if tag == "firefox":
            self._driver = self.fire_fox()
        elif tag == "chrome":
            self._driver = self.make_stealth(self.google_chrome(download_directory))
        elif tag == "undetected_chrome":
            self._driver = self.make_stealth(self.undetected_chrome())
        elif tag == "browser_stack":
            self._driver = self.browser_stack()

    def __call__(self, *args, **kwargs):
        return self._driver

    @staticmethod
    def make_stealth(driver: webdriver):
        stealth(driver,
                languages=["es"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        driver.implicitly_wait(2)
        return driver

    @staticmethod
    def undetected_chrome():
        options = uc.ChromeOptions()
        # options.headless = True
        # options.add_argument('--headless')
        options.arguments.extend(["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"])  # << this

        chrome = uc.Chrome(options=options)
        return chrome

    @staticmethod
    def google_chrome(download_directory=None):
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("start-maximized")
        chrome_options.page_load_strategy = "normal"
        prefs = {"download.default_directory": download_directory}
        chrome_options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=chrome_options)
        return driver

    @staticmethod
    def fire_fox():
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

        # Create a Firefox profile
        profile = FirefoxProfile()

        # Set the default language to Japanese
        profile.set_preference("intl.accept_languages", "ja")

        options = Options()
        options.add_argument("--headless")
        # options.add_argument('--no-sandbox')
        options.add_argument('--lang=es')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.set_preference("layout.css.devPixelsPerPx", "1.0")  # Thiết lập pixel_ratio

        options.profile = profile
        options.headless = True
        driver = webdriver.Firefox(options=options)
        return driver

    @staticmethod
    def browser_stack():
        from selenium.webdriver.firefox.options import Options

        options = Options()

        desired_cap = {
            'browser': 'Chrome',
            'browser_version': '88.0',
            'os': 'Windows',
            'os_version': '10',
            'name': 'BStack-[Python] Sample Test',  # test name
            'build': 'BStack Build Number 1'  # CI/CD job or build name
        }
        options.set_capability('bstack:options', desired_cap)
        driver = webdriver.Remote(
            command_executor='https://hub-cloud.browserstack.com/wd/hub',
            options=options)

        return driver






    

    


