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
from crowd_rpa.cores.haxaco.constant import haxaco_constant


class HaxacoRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename, company_code=None):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory)()

    def get_name(self):
        return haxaco_constant.META_DATA['RPA_NAME']

    def enter_id(self, browser, input_find_by_hd, element_find_by, lookup_code):
        text_box = browser.find_element(input_find_by_hd, element_find_by)
        text_box.send_keys(lookup_code)
        logging.info(f'{self.get_name()}: Enter code lookup: {lookup_code}')

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')

        # check tree folder
        portal_pth = os.path.join(storage_pth, haxaco_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)

        # Open and Maximize the browser
        browser = self.get_driver(save_pth, True)
        browser.maximize_window()

        logging.info(f'{self.get_name()}: Please wait .. ({haxaco_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(haxaco_constant.DELAY_OPEN_MAXIMUM_BROWSER)

        # Get a website
        logging.info(f'{self.get_name()}: Get a website: {portal}')
        browser.get(portal)
        logging.info(f'{self.get_name()}: Please wait .. ({haxaco_constant.DELAY_TIME_LOAD_PAGE}s)')
        time.sleep(haxaco_constant.DELAY_TIME_LOAD_PAGE)

        # Enter id
        self.enter_id(browser, By.ID, haxaco_constant.TEXT_BOX_BY_ID, lookup_code)

        # Enter captcha
        util_rpa.enter_captcha(self.get_name(), browser, By.XPATH, By.XPATH,
                               haxaco_constant.IMG_CAPTCHA_BY_XPATH,
                               haxaco_constant.TEXT_BOX_CAPTCHA_BY_XPATH,
                               By.XPATH, haxaco_constant.BUTTON_SUBMIT_CAPCHA_BY_XPATH, By.XPATH,
                               haxaco_constant.ERROR_ALERT_BY_XPATH, haxaco_constant.RETRY_MAX,
                               haxaco_constant.DELAY_TIME_SKIP, check_num=True, callback=self.enter_id,
                               callback_args=[browser, By.ID, haxaco_constant.TEXT_BOX_BY_ID, lookup_code])

        logging.info(f'{self.get_name()}: Please wait .. ({haxaco_constant.DELAY_TIME_LOAD_PAGE}s)')
        time.sleep(haxaco_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Open view detail')

        # Download file pdf and xml
        logging.info(f'{self.get_name()}: Download file Zip xml')
        download_btn = browser.find_element(By.XPATH, haxaco_constant.BUTTON_DOWNLOAD_BY_XPATH)
        browser.execute_script("arguments[0].click()", download_btn)

        logging.info(f'{self.get_name()}: Please wait .. ({haxaco_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(haxaco_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        # extra zip
        directory_path = f"{storage_pth}/{self.get_name().lower()}/test"
        util_rpa.extract_zip_files_and_keep_specific_files(directory_path)
        time.sleep(haxaco_constant.DELAY_TIME_SKIP)

        # Close rpa
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return haxaco_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': haxaco_constant.LATEST_VERSION,
            'info': haxaco_constant.VERSIONS[haxaco_constant.LATEST_VERSION]
        }


haxaco_ins = HaxacoRpa(haxaco_constant.META_DATA)

if __name__ == '__main__':
    haxaco_ins.extract_data("http://hddt.haxaco.com.vn",
                            "br0B26382897661459518447854",
                            cfg.TEST_ROOT_PTH,
                            "test")

    haxaco_ins.reset()
