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
from crowd_rpa.cores.hilo.constant import hilo_constant


class HiloRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename, company_code=None):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory,
                         more_option=more_option)()

    def get_name(self):
        return hilo_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        portal_pth = os.path.join(storage_pth, hilo_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth, True)
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({hilo_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(hilo_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        url = portal
        browser.get(url)
        logging.info(f'{self.get_name()}: Open a website: {portal}')
        time.sleep(hilo_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({hilo_constant.DELAY_TIME_LOAD_PAGE}s)')

        browser.find_element(By.XPATH, hilo_constant.SELECTOR_BY_XPATH).click()

        text_box = browser.find_element(By.XPATH, hilo_constant.TEXT_BOX_BY_XPATH)
        text_box.clear()
        text_box.send_keys(lookup_code)
        logging.info(f'{self.get_name()}: Enter code lookup: {lookup_code}')
        # Enter captcha
        util_rpa.enter_captcha_hilo(self.get_name(), browser, By.XPATH, By.XPATH,
                                    hilo_constant.CAPTCHA_IMG_BY_XPATH,
                                    hilo_constant.CAPTCHA_INPUT_BY_XPATH,
                                    By.XPATH, hilo_constant.BTN_CLICK_BY_XPATH, By.XPATH,
                                    hilo_constant.VIEW_BTN_BY_XPATH, hilo_constant.RETRY_MAX,
                                    hilo_constant.DELAY_TIME_SKIP, form_btn_handle='click')
        time.sleep(hilo_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        # view button to download
        logging.info(f'{self.get_name()}: Enter view button to download')
        btn_eye = browser.find_element(By.XPATH, hilo_constant.VIEW_BTN_BY_XPATH)
        btn_eye.click()
        logging.info(f'{self.get_name()}: Please wait .. ({hilo_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(hilo_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        # view button to download
        logging.info(f'{self.get_name()}: ENTER DOWLOAD XML')
        download_xml = browser.find_element(By.XPATH, hilo_constant.BTN_DOWNLOAD_XML_BY_XPATH)
        wait = WebDriverWait(browser, hilo_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.XPATH, hilo_constant.BTN_DOWNLOAD_XML_BY_XPATH)))
        download_xml.click()
        logging.info(f'{self.get_name()}: Please wait .. ({hilo_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(hilo_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        # Close rpa
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return hilo_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': hilo_constant.LATEST_VERSION,
            'info': hilo_constant.VERSIONS[hilo_constant.LATEST_VERSION]
        }


hilo_ins = HiloRpa(hilo_constant.META_DATA)

if __name__ == '__main__':
    hilo_ins.extract_data("https://evat.hilo.com.vn",
                          "68be6281-84d8-4a3c-9b3d-8863557105ab",
                          cfg.TEST_ROOT_PTH,
                          "test")
    hilo_ins.reset()