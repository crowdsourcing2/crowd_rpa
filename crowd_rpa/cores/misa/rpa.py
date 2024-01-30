import time
import logging
from abc import ABC
from driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.misa.constant import misa_constant


class MisaRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return misa_constant.META_DATA['RPA_NAME']

    def get_code_lookup(self):
        # TODO: you must be code here!
        return misa_constant.META_DATA['URL'] + 'W8T2F353A8D'

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({misa_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(misa_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_code_lookup())
        logging.info(f'{self.get_name()}: Open a website: {self.get_code_lookup()}')
        time.sleep(misa_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({misa_constant.DELAY_TIME_LOAD_PAGE}s)')
        download_btn = browser.find_element(By.CLASS_NAME, misa_constant.DOWNLOAD_BTN_BY_CLASS_TYPE)
        download_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({misa_constant.DELAY_TIME_SKIP}s)')
        time.sleep(misa_constant.DELAY_TIME_SKIP)
        logging.info(f'{self.get_name()}: Download pdf')
        download_pdf = browser.find_element(By.XPATH, misa_constant.DOWNLOAD_PDF_XPATH)
        download_pdf.click()
        logging.info(f'{self.get_name()}: Please wait .. ({misa_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(misa_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        download_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({misa_constant.DELAY_TIME_SKIP}s)')
        time.sleep(misa_constant.DELAY_TIME_SKIP)
        logging.info(f'{self.get_name()}: Download XML')
        download_xml = browser.find_element(By.XPATH, misa_constant.DOWNLOAD_XML_XPATH)
        download_xml.click()
        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return misa_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': misa_constant.LATEST_VERSION,
            'info': misa_constant.VERSIONS[misa_constant.LATEST_VERSION]
        }


if __name__ == '__main__':
    misa_rpa_ins = MisaRpa(misa_constant.META_DATA)
    misa_rpa_ins.extract_data()
    misa_rpa_ins.reset()
