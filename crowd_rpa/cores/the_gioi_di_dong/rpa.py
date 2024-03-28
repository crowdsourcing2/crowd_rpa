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
from crowd_rpa.cores.the_gioi_di_dong.constant import the_gioi_di_dong_constant


class TheGioiDiDongRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename, company_code=None):
        self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename, company_code)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory, more_option=more_option)()

    def get_name(self):
        return the_gioi_di_dong_constant.META_DATA['RPA_NAME']

    @staticmethod
    def check_extension(portal, group_portal_extension):
        for portal_extension in group_portal_extension:
            if portal_extension in portal:
                return True
        return False

    def enter_code(self, browser, lookup_code, company_code):
        logging.info(f'{self.get_name()}: Enter phone')
        company_input = browser.find_element(By.ID, the_gioi_di_dong_constant.COMPANY_INPUT_BY_ID)
        company_input.clear()
        company_input.send_keys(company_code)

        logging.info(f'{self.get_name()}: Enter ID')
        id_input = browser.find_element(By.ID, the_gioi_di_dong_constant.ID_INPUT_BY_ID)
        id_input.clear()
        id_input.send_keys(lookup_code)
        time.sleep(the_gioi_di_dong_constant.DELAY_TIME_SKIP)

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename, company_code):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        portal_pth = os.path.join(storage_pth, the_gioi_di_dong_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth)
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({the_gioi_di_dong_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(the_gioi_di_dong_constant.DELAY_OPEN_MAXIMUM_BROWSER)

        if self.check_extension(portal=portal,
                                group_portal_extension=the_gioi_di_dong_constant.GROUP_PORTAL_EXTENSIONS[0]):
            # Open a website
            browser.get(portal)
            logging.info(f'{self.get_name()}: Open a website: {portal}')
            time.sleep(the_gioi_di_dong_constant.DELAY_TIME_LOAD_PAGE)
            logging.info(f'{self.get_name()}: Please wait .. ({the_gioi_di_dong_constant.DELAY_TIME_LOAD_PAGE}s)')

            # Enter code
            self.enter_code(browser, lookup_code, company_code)

            # ClearCaptCha
            util_rpa.enter_captcha(name=self.get_name(),
                                   browser=browser,
                                   captcha_find_by=By.XPATH,
                                   captcha_image=the_gioi_di_dong_constant.CAPTCHA_IMG_BY_XPATH,
                                   input_result_captcha_by=By.ID,
                                   input_result_captcha=the_gioi_di_dong_constant.CAPTCHA_INPUT_BY_ID,
                                   submit_find_by=By.ID,
                                   value_submit=the_gioi_di_dong_constant.FORM_BY_ID_TYPE,
                                   result_captcha_by=By.XPATH,
                                   value_result_captcha=the_gioi_di_dong_constant.ERROR_BY_XPATH,
                                   retry_max=the_gioi_di_dong_constant.RETRY_MAX,
                                   delay_time_skip=the_gioi_di_dong_constant.DELAY_TIME_SKIP,
                                   not_errol_captcha=True,
                                   reload_portal=True,
                                   callback=self.enter_code,
                                   callback_args=[browser, lookup_code, company_code]
                                   )
            # Download file xml
            logging.info(f'{self.get_name()}: Download Xml')
            download_btn = browser.find_element(By.XPATH, the_gioi_di_dong_constant.DOWNLOAD_XML_XPATH)
            download_btn.click()
            logging.info(
                f'{self.get_name()}: Please wait .. ({the_gioi_di_dong_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
            time.sleep(the_gioi_di_dong_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return the_gioi_di_dong_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': the_gioi_di_dong_constant.LATEST_VERSION,
            'info': the_gioi_di_dong_constant.VERSIONS[the_gioi_di_dong_constant.LATEST_VERSION]
        }


the_gioi_di_dong_ins = TheGioiDiDongRpa(the_gioi_di_dong_constant.META_DATA)

if __name__ == '__main__':
    the_gioi_di_dong_ins.extract_data("https://hddt.tantamphucvu.vn",
                                      "200400",
                                      cfg.TEST_ROOT_PTH,
                                      'test',
                                      "0387814090")
    the_gioi_di_dong_ins.reset()
