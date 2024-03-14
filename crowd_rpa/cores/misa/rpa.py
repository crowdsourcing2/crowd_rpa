import os
import time
import logging
from abc import ABC
from pathlib import Path

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.misa.constant import misa_constant


class MisaRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None):
        return WebDriver(tag=self.driver_name, download_directory=download_directory)()

    def get_name(self):
        return misa_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        portal_pth = os.path.join(storage_pth, misa_constant.CORE_NAME)
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth)
        # Maximize the browser window to full screen
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({misa_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(misa_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        domain_lookup_code = '?sc=' + lookup_code
        url = portal
        if not portal.endswith(domain_lookup_code):
            url += domain_lookup_code
        browser.get(url)
        logging.info(f'{self.get_name()}: Open a website: {url}')
        time.sleep(misa_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({misa_constant.DELAY_TIME_LOAD_PAGE}s)')
        download_btn = browser.find_element(By.CLASS_NAME, misa_constant.DOWNLOAD_BTN_BY_CLASS_TYPE)
        wait = WebDriverWait(browser, misa_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.XPATH, misa_constant.DOWNLOAD_PDF_XPATH)))
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
        wait = WebDriverWait(browser, misa_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.XPATH, misa_constant.DOWNLOAD_XML_XPATH)))
        download_xml.click()
        time.sleep(misa_constant.DELAY_TIME_SKIP)
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return misa_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': misa_constant.LATEST_VERSION,
            'info': misa_constant.VERSIONS[misa_constant.LATEST_VERSION]
        }


misa_ins = MisaRpa(misa_constant.META_DATA)


if __name__ == '__main__':
    misa_ins.extract_data("https://www.meinvoice.vn/tra-cuu/",
                          "W8T2F353A8D",
                          r"C:\Users\phduo\PycharmProjects\master_tools\velociti-be\crowd_rpa\tests\output",
                          "test")

    misa_ins.reset()
