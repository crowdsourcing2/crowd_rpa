import time
import logging
from abc import ABC
from driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.Wininvoice.constant import wininvoice_constant
from crowd_rpa.utils.rpa_util import util_rpa

class WininvoiceRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)
    def get_portal(self):
        url = ""
        path = wininvoice_constant.FILE_PATH
        if path.endswith(".pdf"):
            url = util_rpa.read_pdf(path, wininvoice_constant.URL_KEYWORD,
                                    wininvoice_constant.CODE_BILL_KEYWORD)
        elif path.endswith(".xml"):
            url = util_rpa.read_xml(path, wininvoice_constant.URL_KEYWORD)

        return 'https://' + url
    def get_code_lookup(self):
        code_bill = ""
        path = wininvoice_constant.FILE_PATH
        if path.endswith(".pdf"):
            code_bill = util_rpa.read_pdf(path, wininvoice_constant.CODE_BILL_KEYWORD,
                                          wininvoice_constant.CITY_CODE_KEYWORD)
        elif path.endswith(".xml"):
            code_bill = util_rpa.read_xml(path, wininvoice_constant.CODE_BILL_KEYWORD)
        return code_bill
    def extract_data(self):
        self.process_download_xml_pdf()

    def check_invoice(self):
        code_city = ""
        path = wininvoice_constant.FILE_PATH
        if path.endswith(".pdf"):
            code_city = util_rpa.read_pdf(path,wininvoice_constant.CITY_CODE_KEYWORD,wininvoice_constant.LAST_KEYWORD)

        elif path.endswith(".xml"):
            code_city = util_rpa.read_xml(path,wininvoice_constant.CITY_CODE_KEYWORD)
        return code_city

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return wininvoice_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({wininvoice_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(wininvoice_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_portal())
        logging.info(f'{self.get_name()}: Open a website: {self.get_portal()}')
        time.sleep(wininvoice_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({wininvoice_constant.DELAY_TIME_LOAD_PAGE}s)')

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
        time.sleep(wininvoice_constant.DELAY_TIME_SKIP)
        link_element = browser.find_element(By.XPATH, "//a[contains(@title, 'Tải file hóa đơn')]")

        # Click on the link to trigger the download
        link_element.click()
        logging.info(f'{self.get_name()}: Clicked on the link to download the invoice file.')
        time.sleep(wininvoice_constant.DELAY_TIME_SKIP)
        view_button2 = browser.find_element(By.XPATH, '//*[@class="go-link btn btn-success btn-sm"]')
        # Remove the 'target' attribute
        browser.execute_script("arguments[0].removeAttribute('target')", view_button2)
        view_button2.click()
        logging.info(f'{self.get_name()}: Clicked the second "Xem" button.')
        # Give some time for the page to load after clicking the button
        time.sleep(wininvoice_constant.DELAY_TIME_SKIP)

        # Continue with the rest of your process
        download_btn = browser.find_element(By.XPATH, wininvoice_constant.DOWNLOAD_BTN_BY_CLASS_TYPE)
        download_btn.click()
        logging.info(f'{self.get_name()}: Clicked the "Download" button.')
        time.sleep(wininvoice_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return wininvoice_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': wininvoice_constant.LATEST_VERSION,
            'info': wininvoice_constant.VERSIONS[wininvoice_constant.LATEST_VERSION]
        }


if __name__ == '__main__':
    wininvoice_rpa_ins = WininvoiceRpa(wininvoice_constant.META_DATA)
    wininvoice_rpa_ins.extract_data()
    wininvoice_rpa_ins.reset()
