import os
import time
import logging
from abc import ABC
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from crowd_rpa.settings import cfg
from crowd_rpa.driver import WebDriver
from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.mobifone.constant import mobifone_constant


class MobiFoneRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename, company_code=None):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory,
                                more_option=more_option)()

    def get_name(self):
        return mobifone_constant.META_DATA['RPA_NAME']

    def enter_id(self, browser, lookup_code):
        id_input = browser.find_element(By.ID, mobifone_constant.ID_INPUT_BY_ID_TYPE)
        id_input.send_keys(lookup_code)
        logging.info(f'{self.get_name()}: Enter id')
        time.sleep(mobifone_constant.DELAY_TIME_LOAD_PAGE)

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        portal_pth = os.path.join(storage_pth, mobifone_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth, True)
        browser = self.get_driver(save_pth)
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({mobifone_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(mobifone_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(portal)
        logging.info(f'{self.get_name()}: Open a website: {portal}')
        time.sleep(mobifone_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({mobifone_constant.DELAY_TIME_LOAD_PAGE}s)')

        # reload page
        try:
            reload_btn = browser.find_element(By.ID, mobifone_constant.RELOAD_BTN_BY_ID_TYPE)
            reload_btn.click()
            time.sleep(mobifone_constant.DELAY_TIME_LOAD_PAGE)
            logging.info(f'{self.get_name()}: Please wait .. ({mobifone_constant.DELAY_TIME_LOAD_PAGE}s)')
        except Exception as e:
            pass

        # Enter id
        self.enter_id(browser, lookup_code)
        # Enter captcha
        util_rpa.enter_captcha(self.get_name(), browser, By.ID, By.ID,
                               mobifone_constant.CAPTCHA_IMG_BY_ID_TYPE,
                               mobifone_constant.CAPTCHA_INPUT_BY_ID_TYPE,
                               By.XPATH, mobifone_constant.FORM_BTN_BY_XPATH_TYPE, By.XPATH,
                               mobifone_constant.ERROR_ALERT_BY_XPATH, mobifone_constant.RETRY_MAX,
                               mobifone_constant.DELAY_TIME_SKIP, check_num=False, form_btn_handle="click",
                               callback=self.enter_id, callback_args=[browser, lookup_code])

        # Download file pdf and xml
        logging.info(f'{self.get_name()}: Download pdf and xml')
        download_btn = browser.find_element(By.XPATH, mobifone_constant.DOWNLOAD_BTN_BY_XPATH_TYPE)
        wait = WebDriverWait(browser, mobifone_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.XPATH, mobifone_constant.DOWNLOAD_BTN_BY_XPATH_TYPE)))
        download_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({mobifone_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(mobifone_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # extra zip
        directory_path = f"{storage_pth}/{self.get_name().lower()}/{filename}"
        util_rpa.extract_zip_files_and_keep_specific_files(directory_path)
        time.sleep(mobifone_constant.DELAY_TIME_SKIP)

        # Close rpa
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return mobifone_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': mobifone_constant.LATEST_VERSION,
            'info': mobifone_constant.VERSIONS[mobifone_constant.LATEST_VERSION]
        }


mobifone_ins = MobiFoneRpa(mobifone_constant.META_DATA)

if __name__ == '__main__':
    mobifone_ins.extract_data("http://invoice.mobifone.vn",
                              "41N4GCGP8",
                              cfg.TEST_ROOT_PTH,
                              "test")
    mobifone_ins.reset()
