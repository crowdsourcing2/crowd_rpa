import os
import time
import logging
from abc import ABC
from pathlib import Path

from crowd_rpa.driver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from crowd_rpa.settings import cfg
from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.yamaha.constant import yamaha_constant


class YamahaRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename, company_code=None):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory,
                         more_option=more_option)()

    def get_name(self):
        return yamaha_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        portal_pth = os.path.join(storage_pth, yamaha_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth, True)
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({yamaha_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(yamaha_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        url = portal + "/YamahaSearchInvByCode/Index/"
        browser.get(url)
        logging.info(f'{self.get_name()}: Open a website: {url}')
        time.sleep(yamaha_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({yamaha_constant.DELAY_TIME_LOAD_PAGE}s)')
        # Enter id
        id_input = browser.find_element(By.ID, yamaha_constant.ID_INPUT_BY_ID_TYPE)
        id_input.send_keys(lookup_code)
        logging.info(f'{self.get_name()}: Enter id')
        # Enter captcha
        util_rpa.enter_captcha(self.get_name(), browser, By.CLASS_NAME, By.ID,
                               yamaha_constant.CAPTCHA_IMG_BY_CLASS_TYPE,
                               yamaha_constant.CAPTCHA_INPUT_BY_ID_TYPE,
                               By.ID, yamaha_constant.FORM_BY_ID_TYPE, By.XPATH,
                               yamaha_constant.ERROR_ALERT_BY_XPATH, yamaha_constant.RETRY_MAX,
                               yamaha_constant.DELAY_TIME_SKIP, check_num=True)

        # Download file pdf
        logging.info(f'{self.get_name()}: Download pdf')
        download_pdf_btn = browser.find_element(By.XPATH, yamaha_constant.DOWNLOAD_PDF_BTN_BY_XPATH)
        wait = WebDriverWait(browser, yamaha_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.XPATH, yamaha_constant.DOWNLOAD_PDF_BTN_BY_XPATH)))
        download_pdf_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({yamaha_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(yamaha_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # Open view detail
        logging.info(f'{self.get_name()}: Open view detail')
        view_btn = browser.find_element(By.XPATH, yamaha_constant.VIEW_BTN_BY_XPATH)
        wait = WebDriverWait(browser, yamaha_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.XPATH, yamaha_constant.VIEW_BTN_BY_XPATH)))
        view_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({yamaha_constant.DELAY_TIME_SKIP}s)')
        time.sleep(yamaha_constant.DELAY_TIME_SKIP)
        # Download file xml
        logging.info(f'{self.get_name()}: Download xml')
        download_xml_btn = browser.find_element(By.XPATH, yamaha_constant.DOWNLOAD_XML_BTN_BY_XPATH)
        wait = WebDriverWait(browser, yamaha_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.XPATH, yamaha_constant.DOWNLOAD_XML_BTN_BY_XPATH)))
        download_xml_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({yamaha_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(yamaha_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # extra zip
        directory_path = f"{storage_pth}/{self.get_name().lower()}/{filename}"
        util_rpa.extract_zip_files_and_keep_specific_files(directory_path)
        time.sleep(yamaha_constant.DELAY_TIME_SKIP)

        # Close rpa
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return yamaha_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': yamaha_constant.LATEST_VERSION,
            'info': yamaha_constant.VERSIONS[yamaha_constant.LATEST_VERSION]
        }


yamaha_ins = YamahaRpa(yamaha_constant.META_DATA)

if __name__ == '__main__':
    yamaha_ins.extract_data("https://einvoice78.yamaha-motor.com.vn",
                            "EINV21142346",
                            cfg.TEST_ROOT_PTH,
                            "test")
    yamaha_ins.reset()
