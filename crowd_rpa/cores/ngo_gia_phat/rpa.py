import os
import time
import logging
from abc import ABC
from pathlib import Path

from crowd_rpa.driver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from crowd_rpa.settings import cfg
from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.ngo_gia_phat.constant import ngo_gia_phat_constant


class NgoGiaPhatRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename, company_code=None):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory)()

    def get_name(self):
        return ngo_gia_phat_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')

        portal_pth = os.path.join(storage_pth, ngo_gia_phat_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth)
        browser.maximize_window()

        logging.info(f'{self.get_name()}: Please wait .. ({ngo_gia_phat_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(ngo_gia_phat_constant.DELAY_OPEN_MAXIMUM_BROWSER)

        logging.info(f'{self.get_name()}: Open a website: {portal}')
        browser.get(portal)
        logging.info(f'{self.get_name()}: Please wait .. ({ngo_gia_phat_constant.DELAY_TIME_LOAD_PAGE}s)')
        time.sleep(ngo_gia_phat_constant.DELAY_TIME_LOAD_PAGE)

        text_box = browser.find_element(By.XPATH, ngo_gia_phat_constant.INPUT_BY_XPATH_ID)
        text_box.send_keys(lookup_code)
        logging.info(f'{self.get_name()}: Enter code lookup: {lookup_code}')

        util_rpa.enter_captcha(self.get_name(), browser, By.XPATH, By.XPATH,
                               ngo_gia_phat_constant.IMG_CAPTCHA_BY_XPATH,
                               ngo_gia_phat_constant.INPUT_CAPTCHA_BY_XPATH,
                               By.XPATH, ngo_gia_phat_constant.FORM_ENTER_BY_XPATH, By.XPATH,
                               ngo_gia_phat_constant.ERROR_ALERT_BY_XPATH, ngo_gia_phat_constant.RETRY_MAX,
                               ngo_gia_phat_constant.DELAY_TIME_SKIP, check_num=False, form_btn_handle="click")

        logging.info(f'{self.get_name()}: Download pdf and xml')
        download_btn = browser.find_element(By.XPATH, ngo_gia_phat_constant.BUTTON_DOWNLOAD_BY_XPATH)
        wait = WebDriverWait(browser, ngo_gia_phat_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.XPATH, ngo_gia_phat_constant.BUTTON_DOWNLOAD_BY_XPATH)))
        download_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({ngo_gia_phat_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(ngo_gia_phat_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # extra zip
        directory_path = f"{storage_pth}/{self.get_name().lower()}/{filename}"
        util_rpa.extract_zip_files_and_keep_specific_files(directory_path)
        time.sleep(ngo_gia_phat_constant.DELAY_TIME_SKIP)

        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return ngo_gia_phat_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': ngo_gia_phat_constant.LATEST_VERSION,
            'info': ngo_gia_phat_constant.VERSIONS[ngo_gia_phat_constant.LATEST_VERSION]
        }


ngo_gia_phat_ins = NgoGiaPhatRpa(ngo_gia_phat_constant.META_DATA)

if __name__ == '__main__':
    ngo_gia_phat_ins.extract_data("https://tracuuonline78.ngogiaphat.vn",
                                  "2747B58278DC46D9892D6FB3C0EFA81F",
                                  cfg.TEST_ROOT_PTH,
                                  "test")

    ngo_gia_phat_ins.reset()
