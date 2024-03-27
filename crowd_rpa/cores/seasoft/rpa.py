import os
import time
import logging
from abc import ABC
from pathlib import Path
from crowd_rpa.utils.rpa_util import util_rpa

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from crowd_rpa.settings import cfg
from crowd_rpa.driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.seasoft.constant import sea_soft_constant


class SeaSoftRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename, company_code=None):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename, company_code)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory, more_option=more_option)()

    def get_name(self):
        return sea_soft_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename, company_code=None):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        portal_pth = os.path.join(storage_pth, sea_soft_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth)
        # Maximize the browser window to full screen
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({sea_soft_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(sea_soft_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        browser.get(portal)
        logging.info(f'{self.get_name()}: Open a website: {portal}')
        time.sleep(sea_soft_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({sea_soft_constant.DELAY_TIME_LOAD_PAGE}s)')
        # Enter invoice code
        logging.info(f'{self.get_name()}: Enter invoice code')
        time.sleep(sea_soft_constant.DELAY_TIME_SKIP)
        invoice_code = browser.find_element(By.ID, sea_soft_constant.INPUT_INVOICE_CODE_BY_ID)
        invoice_code.send_keys(company_code)
        time.sleep(sea_soft_constant.DELAY_TIME_SKIP)
        # Enter lookup code
        logging.info(f'{self.get_name()}: Enter lookup code')
        time.sleep(sea_soft_constant.DELAY_TIME_SKIP)
        input_lookup_code = browser.find_element(By.ID, sea_soft_constant.INPUT_LOOKUP_CODE_BY_ID)
        input_lookup_code.send_keys(lookup_code)
        time.sleep(sea_soft_constant.DELAY_TIME_SKIP)
        # Enter captcha
        util_rpa.enter_captcha(self.get_name(), browser, By.ID, By.ID,
                               sea_soft_constant.CAPTCHA_IMG_BY_ID,
                               sea_soft_constant.INPUT_CAPTCHA_CODE_BY_ID, By.XPATH,
                               sea_soft_constant.BUTTON_SUBMIT_BY_XPATH, By.CLASS_NAME,
                               sea_soft_constant.ERROR_ALERT_BY_CLASS,
                               sea_soft_constant.RETRY_MAX,
                               sea_soft_constant.DELAY_TIME_SKIP, check_num=False)
        time.sleep(sea_soft_constant.DELAY_TIME_SKIP)
        time.sleep(sea_soft_constant.DELAY_TIME_SKIP)
        # Download file zip
        logging.info(f'{self.get_name()}: Download file zip pdf & xml')
        download_zip = browser.find_element(By.XPATH, sea_soft_constant.DOWNLOAD_BTN_ZIP_BY_XPATH)
        wait = WebDriverWait(browser, sea_soft_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(EC.presence_of_element_located((By.XPATH, sea_soft_constant.DOWNLOAD_BTN_ZIP_BY_XPATH)))
        download_zip.click()
        time.sleep(sea_soft_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # Extract file zip
        logging.info(f'{self.get_name()}: Extract zip file pdf & xml')
        directory_path = f'{storage_pth}/{self.get_name().lower()}/test'
        util_rpa.extract_zip_files_and_keep_specific_files(directory_path)
        time.sleep(sea_soft_constant.DELAY_TIME_SKIP)
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return sea_soft_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': sea_soft_constant.LATEST_VERSION,
            'info': sea_soft_constant.VERSIONS[sea_soft_constant.LATEST_VERSION]
        }


sea_soft_ins = SeaSoftRpa(sea_soft_constant.META_DATA)

if __name__ == '__main__':
    sea_soft_ins.extract_data("http://hoadon.hiephungnhatrang.com",
                              "GDMIIM",
                              cfg.TEST_ROOT_PTH,
                              "test", "0001244")

    sea_soft_ins.reset()
