import os
import time
import logging
from abc import ABC
from pathlib import Path

from driver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.digiworld.constant import digi_world_constant


class DigiWorldRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory,
                         more_option=more_option)()

    def get_name(self):
        return digi_world_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        portal_pth = os.path.join(storage_pth, digi_world_constant.CORE_NAME)
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth, True)
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({digi_world_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(digi_world_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(portal)
        logging.info(f'{self.get_name()}: Open a website: {portal}')
        time.sleep(digi_world_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({digi_world_constant.DELAY_TIME_LOAD_PAGE}s)')
        # Enter id
        id_input = browser.find_element(By.ID, digi_world_constant.ID_INPUT_BY_ID_TYPE)
        id_input.send_keys(lookup_code)
        logging.info(f'{self.get_name()}: Enter id')
        # Enter captcha
        util_rpa.enter_captcha(self.get_name(), browser, By.CLASS_NAME, By.ID,
                               digi_world_constant.CAPTCHA_IMG_BY_CLASS_TYPE,
                               digi_world_constant.CAPTCHA_INPUT_BY_ID_TYPE,
                               By.ID, digi_world_constant.FORM_BY_ID_TYPE, By.XPATH,
                               digi_world_constant.ERROR_ALERT_BY_XPATH, digi_world_constant.RETRY_MAX,
                               digi_world_constant.DELAY_TIME_SKIP, check_num=True)
        # Open view detail
        logging.info(f'{self.get_name()}: Open view detail')
        view_btn = browser.find_element(By.XPATH, digi_world_constant.VIEW_BTN_BY_XPATH)
        wait = WebDriverWait(browser, digi_world_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.XPATH, digi_world_constant.VIEW_BTN_BY_XPATH)))
        view_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({digi_world_constant.DELAY_TIME_SKIP}s)')
        time.sleep(digi_world_constant.DELAY_TIME_SKIP)
        # Download file pdf and xml
        logging.info(f'{self.get_name()}: Download pdf and xml')
        download_btn = browser.find_element(By.NAME, digi_world_constant.DOWNLOAD_BTN_BY_NAME_TYPE)
        wait = WebDriverWait(browser, digi_world_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.NAME, digi_world_constant.DOWNLOAD_BTN_BY_NAME_TYPE)))
        download_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({digi_world_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(digi_world_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # extra zip
        directory_path = f"{storage_pth}/{self.get_name()}/{self.get_name().lower()}"
        util_rpa.extract_zip_files_and_keep_specific_files(directory_path)
        time.sleep(digi_world_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        # Close rpa
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return digi_world_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': digi_world_constant.LATEST_VERSION,
            'info': digi_world_constant.VERSIONS[digi_world_constant.LATEST_VERSION]
        }


digi_world_ins = DigiWorldRpa(digi_world_constant.META_DATA)

if __name__ == '__main__':
    digi_world_ins.extract_data("https://hddt78.digiworld.com.vn",
                                "13231232184PD2B",
                                r"D:\RainScales\crowd_rpa\tests\output",
                                "test")

    digi_world_ins.reset()
