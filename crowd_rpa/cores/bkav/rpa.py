import os
import time
import logging
from abc import ABC
from pathlib import Path

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from crowd_rpa.settings import cfg
from crowd_rpa.driver import WebDriver
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.bkav.constant import bkav_constant


class BkavRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory, more_option=more_option)()

    def get_name(self):
        return bkav_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        portal_pth = os.path.join(storage_pth, bkav_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth, True)
        # Maximize the browser window to full screen
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({bkav_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(bkav_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(portal)
        logging.info(f'{self.get_name()}: Open a website: {portal}')
        time.sleep(bkav_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({bkav_constant.DELAY_TIME_LOAD_PAGE}s)')
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
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return bkav_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': bkav_constant.LATEST_VERSION,
            'info': bkav_constant.VERSIONS[bkav_constant.LATEST_VERSION]
        }


bkav_ins = BkavRpa(bkav_constant.META_DATA)

if __name__ == '__main__':
    bkav_ins.extract_data("https://tracuu.ehoadon.vn",
                          "Y88TPVQF501",
                          cfg.TEST_ROOT_PTH,
                          "test")
    bkav_ins.reset()
