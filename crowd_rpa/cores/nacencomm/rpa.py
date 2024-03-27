import os
import time
import logging

from abc import ABC
from pathlib import Path
from selenium.webdriver.common.by import By

from crowd_rpa.settings import cfg
from crowd_rpa.driver import WebDriver
from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.nacencomm.constant import nacencomm_constant


class NacencommRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename, company_code=None):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory, more_option=more_option)()

    def get_name(self):
        return nacencomm_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        portal_pth = os.path.join(storage_pth, nacencomm_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth, True)
        # Maximize the browser window to full screen
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({nacencomm_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(nacencomm_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(portal)
        logging.info(f'{self.get_name()}: Open a website: {portal}')
        time.sleep(nacencomm_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({nacencomm_constant.DELAY_TIME_LOAD_PAGE}s)')

        # Click search
        logging.info(f'{self.get_name()}: Redirect search page')
        search_btn = browser.find_element(By.XPATH, nacencomm_constant.SEARCH_BTN_BY_XPATH)
        search_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({nacencomm_constant.DELAY_TIME_SKIP}s)')
        time.sleep(nacencomm_constant.DELAY_TIME_SKIP)

        # Click radio
        logging.info(f'{self.get_name()}: Choice type')
        choice_radio = browser.find_element(By.XPATH, nacencomm_constant.CHOICE_RADIO_BY_XPATH)
        choice_radio.click()

        # Enter ID
        logging.info(f'{self.get_name()}: Enter ID')
        id_input = browser.find_element(By.ID, nacencomm_constant.ID_INPUT_BY_ID)
        id_input.send_keys(lookup_code)

        # Submit form
        logging.info(f'{self.get_name()}: Submit Form')
        submit_btn = browser.find_element(By.ID, nacencomm_constant.SUBMIT_BTN_BY_ID)
        submit_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({nacencomm_constant.DELAY_TIME_SKIP}s)')
        time.sleep(nacencomm_constant.DELAY_TIME_SKIP)

        # Download zip
        logging.info(f'{self.get_name()}: Download zip')
        download_zip = browser.find_element(By.ID, nacencomm_constant.DOWNLOAD_ZIP_BY_ID)
        browser.implicitly_wait(nacencomm_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        download_zip.click()
        logging.info(f'{self.get_name()}: Please wait .. ({nacencomm_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(nacencomm_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        # Extra zip
        src_pth = os.path.join(storage_pth, nacencomm_constant.CORE_NAME.lower())
        save_pth = os.path.join(src_pth, filename)
        util_rpa.extract_zip_files_and_keep_specific_files(save_pth)
        time.sleep(nacencomm_constant.DELAY_TIME_SKIP)

        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return nacencomm_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': nacencomm_constant.LATEST_VERSION,
            'info': nacencomm_constant.VERSIONS[nacencomm_constant.LATEST_VERSION]
        }


nacencomm_ins = NacencommRpa(nacencomm_constant.META_DATA)

if __name__ == '__main__':
    nacencomm_ins.extract_data("https://hoadon78.nacencomm.vn",
                               "YwU4Fa5x0s1XYmoTk5+wEZykGTuEihY7QI4NznsLo90=",
                               cfg.TEST_ROOT_PTH,
                               "test")

    nacencomm_ins.reset()
