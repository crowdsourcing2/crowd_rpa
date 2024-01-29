import os
import pathlib
import time
import logging
from abc import ABC
from driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.Wininvoice.constant import wininvoice_constant


class WininvoiceRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return wininvoice_constant.META_DATA['RPA_NAME']

    def get_code_lookup(self):
        return wininvoice_constant.META_DATA['URL']

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({wininvoice_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(wininvoice_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_code_lookup())
        logging.info(f'{self.get_name()}: Open a website: {self.get_code_lookup()}')
        time.sleep(wininvoice_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({wininvoice_constant.DELAY_TIME_LOAD_PAGE}s)')

        # Find and input data into the input field
        input_field = browser.find_element(By.NAME, "private_code")
        input_field.send_keys("H64PXFK8JQ")
        # Find and input data into the input field
        input_field = browser.find_element(By.NAME, "cmpn_key")
        input_field.send_keys("0317572285")
        view_button = browser.find_element(By.CSS_SELECTOR, ".btn.blue")
        view_button.click()
        time.sleep(wininvoice_constant.DELAY_TIME_SKIP)
        link_element = browser.find_element(By.XPATH, "//a[contains(@title, 'Tải file hóa đơn')]")

        # Click on the link to trigger the download
        link_element.click()

        time.sleep(wininvoice_constant.DELAY_TIME_SKIP)
        view_button2 = browser.find_element(By.XPATH, '//*[@class="go-link btn btn-success btn-sm"]')
        # Remove the 'target' attribute
        browser.execute_script("arguments[0].removeAttribute('target')", view_button2)
        view_button2.click()
        # Give some time for the page to load after clicking the button
        time.sleep(wininvoice_constant.DELAY_TIME_SKIP)

        # Continue with the rest of your process
        download_btn = browser.find_element(By.XPATH, wininvoice_constant.DOWNLOAD_BTN_BY_CLASS_TYPE)
        download_btn.click()
        time.sleep(wininvoice_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

if __name__ == '__main__':
    wininvoice_rpa_ins = WininvoiceRpa(wininvoice_constant.META_DATA)
    wininvoice_rpa_ins.extract_data()
    wininvoice_rpa_ins.reset()
