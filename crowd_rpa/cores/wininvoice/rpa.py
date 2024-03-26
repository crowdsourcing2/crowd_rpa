import time
import logging

from abc import ABC
from selenium.webdriver.common.by import By

from crowd_rpa.driver import WebDriver
from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.wininvoice.constant import win_invoice_constant


class WininvoiceRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def get_portal(self):
        url = ""
        path = win_invoice_constant.FILE_PATH
        if path.endswith(".pdf"):
            url = util_rpa.read_pdf(path, win_invoice_constant.URL_KEYWORD,
                                    win_invoice_constant.CODE_BILL_KEYWORD)
        elif path.endswith(".xml"):
            url = util_rpa.read_xml(path, win_invoice_constant.URL_KEYWORD)

        return 'https://' + url

    def get_code_lookup(self):
        code_bill = ""
        path = win_invoice_constant.FILE_PATH
        if path.endswith(".pdf"):
            code_bill = util_rpa.read_pdf(path, win_invoice_constant.CODE_BILL_KEYWORD,
                                          win_invoice_constant.CITY_CODE_KEYWORD)
        elif path.endswith(".xml"):
            code_bill = util_rpa.read_xml(path, win_invoice_constant.CODE_BILL_KEYWORD)
        return code_bill

    def extract_data(self):
        self.process_download_xml_pdf()

    def check_invoice(self):
        code_city = ""
        path = win_invoice_constant.FILE_PATH
        if path.endswith(".pdf"):
            code_city = util_rpa.read_pdf(path, win_invoice_constant.CITY_CODE_KEYWORD,
                                          win_invoice_constant.LAST_KEYWORD)

        elif path.endswith(".xml"):
            code_city = util_rpa.read_xml(path, win_invoice_constant.CITY_CODE_KEYWORD)
        return code_city

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return win_invoice_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({win_invoice_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(win_invoice_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_portal())
        logging.info(f'{self.get_name()}: Open a website: {self.get_portal()}')
        time.sleep(win_invoice_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({win_invoice_constant.DELAY_TIME_LOAD_PAGE}s)')

        # Find and input data into the input field
        input_field = browser.find_element(By.NAME, "private_code")
        input_field.send_keys(self.get_code_lookup())
        logging.info(f'{self.get_name()}: Entered private code.')

        # Find and input data into the input field
        input_field = browser.find_element(By.NAME, "cmpn_key")
        input_field.send_keys(self.check_invoice())
        logging.info(f'{self.get_name()}: Entered company key.')
        view_button = browser.find_element(By.CSS_SELECTOR, ".btn.blue")
        view_button.click()
        logging.info(f'{self.get_name()}: Clicked the "Xem" button.')
        time.sleep(win_invoice_constant.DELAY_TIME_SKIP)
        link_element = browser.find_element(By.XPATH, "//a[contains(@title, 'Tải file hóa đơn')]")

        # Click on the link to trigger the download
        link_element.click()
        logging.info(f'{self.get_name()}: Clicked on the link to download the invoice file.')
        time.sleep(win_invoice_constant.DELAY_TIME_SKIP)
        view_button2 = browser.find_element(By.XPATH, '//*[@class="go-link btn btn-success btn-sm"]')
        # Remove the 'target' attribute
        browser.execute_script("arguments[0].removeAttribute('target')", view_button2)
        view_button2.click()
        logging.info(f'{self.get_name()}: Clicked the second "Xem" button.')
        # Give some time for the page to load after clicking the button
        time.sleep(win_invoice_constant.DELAY_TIME_SKIP)

        # Continue with the rest of your process
        download_btn = browser.find_element(By.XPATH, win_invoice_constant.DOWNLOAD_BTN_BY_CLASS_TYPE)
        download_btn.click()
        logging.info(f'{self.get_name()}: Clicked the "Download" button.')
        time.sleep(win_invoice_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return win_invoice_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': win_invoice_constant.LATEST_VERSION,
            'info': win_invoice_constant.VERSIONS[win_invoice_constant.LATEST_VERSION]
        }


win_invoice_ins = WininvoiceRpa(win_invoice_constant.META_DATA)

if __name__ == '__main__':
    win_invoice_ins.extract_data()
    win_invoice_ins.reset()
