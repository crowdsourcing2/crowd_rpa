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
from crowd_rpa.cores.thai_son.constant import thai_son_constant


class ThaiSonRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename, company_code=None):
        self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory, more_option=more_option)()

    def get_name(self):
        return thai_son_constant.META_DATA['RPA_NAME']

    @staticmethod
    def check_extension(portal, group_portal_extension):
        for portal_extension in group_portal_extension:
            if portal_extension in portal:
                return True
        return False

    def enter_id(self, browser, lookup_code):
        logging.info(f'{self.get_name()}: Please wait .. ({thai_son_constant.DELAY_TIME_LOAD_PAGE}s)')
        mst_text = browser.find_element(By.ID, thai_son_constant.MA_NHAN_HOA_DON_ID)
        mst_text.clear()
        mst_text.send_keys(lookup_code)

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        portal_pth = os.path.join(storage_pth, thai_son_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth)
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({thai_son_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(thai_son_constant.DELAY_OPEN_MAXIMUM_BROWSER)

        if self.check_extension(portal=portal, group_portal_extension=thai_son_constant.GROUP_PORTAL_EXTENSIONS[0]):
            # Open a website
            browser.get(portal)
            logging.info(f'{self.get_name()}: Open a website: {portal}')
            time.sleep(thai_son_constant.DELAY_TIME_LOAD_PAGE)
            # Enter ID
            self.enter_id(browser, lookup_code)
            # ClearCaptCha
            util_rpa.enter_captcha(name=self.get_name(),
                                   browser=browser,
                                   captcha_find_by=By.ID,
                                   captcha_image=thai_son_constant.CAPTCHA_IMG_ID,
                                   input_result_captcha_by=By.ID,
                                   input_result_captcha=thai_son_constant.CAPTCHA_TEXT_ID,
                                   submit_find_by=By.ID,
                                   value_submit=thai_son_constant.FORM_BY_ID_TYPE,
                                   result_captcha_by=By.ID,
                                   value_result_captcha=thai_son_constant.ERROR_ID,
                                   retry_max=thai_son_constant.RETRY_MAX,
                                   delay_time_skip=thai_son_constant.DELAY_TIME_SKIP,
                                   callback=self.enter_id,
                                   callback_args=[browser, lookup_code],
                                   use_script=True)
            # Download file zip
            logging.info(f'{self.get_name()}: Download Zip')
            download_zip = browser.find_element(By.XPATH, thai_son_constant.DOWNLOAD_ZIP_XPATH)
            download_zip.click()
            logging.info(
                f'{self.get_name()}: Please wait .. ({thai_son_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
            time.sleep(thai_son_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

            # extra zip
            src_pth = os.path.join(storage_pth, thai_son_constant.CORE_NAME.lower())
            util_rpa.extract_zip_files_and_keep_specific_files(os.path.join(src_pth, filename))
            time.sleep(thai_son_constant.DELAY_TIME_SKIP)

        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return thai_son_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': thai_son_constant.LATEST_VERSION,
            'info': thai_son_constant.VERSIONS[thai_son_constant.LATEST_VERSION]
        }


thai_son_ins = ThaiSonRpa(thai_son_constant.META_DATA)

if __name__ == '__main__':
    thai_son_ins.extract_data("https://einvoice-fbvn.fujifilm.com/",
                              "LWT6XPFZ3",
                              cfg.TEST_ROOT_PTH,
                              'test')
    thai_son_ins.reset()
