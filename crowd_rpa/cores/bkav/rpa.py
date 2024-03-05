
import time
import logging
from abc import ABC
from driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.bkav.constant import bkav_constant
from selenium.common.exceptions import TimeoutException


class BkavRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return bkav_constant.META_DATA['RPA_NAME']

    def get_code_lookup(self):
        # TODO: you must be code here!
        return bkav_constant.META_DATA['URL']

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({bkav_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(bkav_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_code_lookup())
        logging.info(f'{self.get_name()}: Open a website: {self.get_code_lookup()}')
        time.sleep(bkav_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({bkav_constant.DELAY_TIME_LOAD_PAGE}s)')
        #Enter lookup code
        logging.info(f'{self.get_name()}: Enter lookup code')
        input_id = browser.find_element(By.CLASS_NAME, bkav_constant.INPUT_ID)
        input_id.send_keys("Y88TPVQF501")
        btnSearch = browser.find_element(By.ID, bkav_constant.BUTTON_SEARCH_BY_ID)
        btnSearch.click()
        time.sleep(bkav_constant.DELAY_TIME_LOAD_PAGE)
        try:
            iframe = browser.find_element(By.ID, bkav_constant.IFRAME_BY_ID)
            browser.get(iframe.get_attribute('src'))
            time.sleep(bkav_constant.DELAY_TIME_LOAD_PAGE)
            logging.info(f'{self.get_name()}: Please wait .. ({bkav_constant.DELAY_TIME_LOAD_PAGE}s)')
            # Chờ đến khi nút download hiển thị và có thể được click
            menu_download = browser.find_element(By.XPATH, bkav_constant.MENU_DOWNLOAD_BY_XPATH)
            browser.execute_script('arguments[0].style.setProperty("display", "block", "important")', menu_download)
            # Show menu
        except TimeoutException:
            logging.error("TimeoutException: Cannot find the download button within the specified time.")
        # Download PDF
        logging.info(f'{self.get_name()}: Download pdf')
        download_pdf = browser.find_element(By.XPATH, bkav_constant.DOWNLOAD_PDF_XPATH)
        download_pdf.click()
        logging.info(f'{self.get_name()}: Please wait .. ({bkav_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(bkav_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # Download XML
        logging.info(f'{self.get_name()}: Download XML')
        download_xml = browser.find_element(By.XPATH, bkav_constant.DOWNLOAD_XML_XPATH)
        download_xml.click()
        time.sleep(bkav_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return bkav_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': bkav_constant.LATEST_VERSION,
            'info': bkav_constant.VERSIONS[bkav_constant.LATEST_VERSION]
        }


if __name__ == '__main__':
    bkav_rpa_ins = BkavRpa(bkav_constant.META_DATA)
    bkav_rpa_ins.extract_data()
    bkav_rpa_ins.reset()




