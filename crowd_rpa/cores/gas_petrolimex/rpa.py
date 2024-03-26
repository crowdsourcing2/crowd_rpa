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
from crowd_rpa.cores.gas_petrolimex.constant import gas_petrolimex_constant


class Gas_PetrolimexRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename, company_code=None):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory,
                         more_option=more_option)()

    def get_name(self):
        return gas_petrolimex_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        portal_pth = os.path.join(storage_pth, gas_petrolimex_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth, True)
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({gas_petrolimex_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(gas_petrolimex_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        url = portal
        browser.get(url)
        logging.info(f'{self.get_name()}: Open a website: {portal}')
        time.sleep(gas_petrolimex_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({gas_petrolimex_constant.DELAY_TIME_LOAD_PAGE}s)')
        # Enter id
        logging.info(f'{self.get_name()}: Enter id')
        id_input = browser.find_element(By.ID, gas_petrolimex_constant.ID_INPUT_BY_ID_TYPE)
        id_input.send_keys(lookup_code)
        time.sleep(gas_petrolimex_constant.DELAY_TIME_SKIP)
        # Enter captcha
        logging.info(f'{self.get_name()}: Enter captcha')
        label_captcha = browser.find_element(By.ID, gas_petrolimex_constant.CAPTCHA_LABEL_BY_ID_TYPE)
        captcha_text = label_captcha.text.replace(" ", "")
        captcha_input = browser.find_element(By.ID, gas_petrolimex_constant.CAPTCHA_INPUT_BY_ID_TYPE)
        captcha_input.send_keys(captcha_text)
        time.sleep(gas_petrolimex_constant.DELAY_TIME_SKIP)
        # Form submit
        logging.info(f'{self.get_name()}: Submit form')
        form_btn = browser.find_element(By.XPATH, gas_petrolimex_constant.FORM_BTN_BY_XPATH_TYPE)
        form_btn.click()
        time.sleep(gas_petrolimex_constant.DELAY_TIME_SKIP)

        # Download file zip
        logging.info(f'{self.get_name()}: Download zip')
        download_btn = browser.find_element(By.XPATH, gas_petrolimex_constant.DOWNLOAD_BTN_BY_XPATH)
        wait = WebDriverWait(browser, gas_petrolimex_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.XPATH, gas_petrolimex_constant.DOWNLOAD_BTN_BY_XPATH)))
        download_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({gas_petrolimex_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(gas_petrolimex_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        download_zip_btn = browser.find_element(By.ID, gas_petrolimex_constant.DOWNLOAD_ZIP_BTN_BY_ID)
        wait = WebDriverWait(browser, gas_petrolimex_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.ID, gas_petrolimex_constant.DOWNLOAD_ZIP_BTN_BY_ID)))
        download_zip_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({gas_petrolimex_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(gas_petrolimex_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # extra zip
        directory_path = f"{storage_pth}/{self.get_name().lower()}/{filename}"
        util_rpa.extract_zip_files_and_keep_specific_files(directory_path)
        time.sleep(gas_petrolimex_constant.DELAY_TIME_SKIP)

        # Close rpa
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return gas_petrolimex_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': gas_petrolimex_constant.LATEST_VERSION,
            'info': gas_petrolimex_constant.VERSIONS[gas_petrolimex_constant.LATEST_VERSION]
        }


gas_petrolimex_ins = Gas_PetrolimexRpa(gas_petrolimex_constant.META_DATA)

if __name__ == '__main__':
    gas_petrolimex_ins.extract_data("https://hoadon.pgas.vn/",
                                    "5YFV27XQAG",
                                    cfg.TEST_ROOT_PTH,
                                    "test")
    gas_petrolimex_ins.reset()
