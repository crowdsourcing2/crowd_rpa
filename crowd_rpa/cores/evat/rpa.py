import os
import time
import logging
from abc import ABC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.evat.constant import evat_constant
from driver import WebDriver

class EvatRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return evat_constant.META_DATA['RPA_NAME']

    def get_code_lookup(self):
        return evat_constant.META_DATA['URL']

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        browser = self.get_driver()

        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({evat_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(evat_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(evat_constant.URL)
        logging.info(f'{self.get_name()}: Open a website: {self.get_code_lookup()}')
        time.sleep(evat_constant.DELAY_TIME_LOAD_PAGE)

        lookupcode = browser.find_element(By.CSS_SELECTOR, ".login-form > div:nth-child(2) > input")
        lookupcode.send_keys("XYKZZCQQAL")

        companycode = browser.find_element(By.CSS_SELECTOR, ".login-form > div:nth-child(3) > input")
        companycode.send_keys("0313123200")

        view_button = browser.find_element(By.CSS_SELECTOR, ".btn.blue")
        view_button.click()

        # _aflist > tr > td.td-actions.text-center.w220 > a.go-link.btn.btn-info.btn-sm

        link_element = browser.find_element(By.XPATH, "//a[contains(@title, 'Tải file hóa đơn')]")
        link_element.click()
        view_button2 = browser.find_element(By.XPATH, '//*[@class="go-link btn btn-success btn-sm"]')
        browser.execute_script("arguments[0].removeAttribute('target')", view_button2)
        view_button2.click()

        time.sleep(evat_constant.DELAY_TIME_SKIP)

        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

if __name__ == '__main__':
    evat_rpa_ins = EvatRpa(evat_constant.META_DATA)
    evat_rpa_ins.extract_data()
    evat_rpa_ins.reset()