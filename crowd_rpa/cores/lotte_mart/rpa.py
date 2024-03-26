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
from crowd_rpa.cores.lotte_mart.constant import lottemart_constant


class LotteMartRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename, company_code=None):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory,
                         more_option=more_option)()

    def get_name(self):
        return lottemart_constant.META_DATA['RPA_NAME']

    def enter_id(self, browser, lookup_code):
        text_box = browser.find_element(By.CLASS_NAME, lottemart_constant.TEXT_BOX_BY_CLASS_TYPE)
        text_box.send_keys(lookup_code)
        logging.info(f'{self.get_name()}: Enter code lookup: {lookup_code}')

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        portal_pth = os.path.join(storage_pth, lottemart_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth)
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({lottemart_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(lottemart_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        logging.info(f'{self.get_name()}: Open a website: {portal}')
        browser.get(portal)
        logging.info(f'{self.get_name()}: Please wait .. ({lottemart_constant.DELAY_TIME_LOAD_PAGE}s)')
        time.sleep(lottemart_constant.DELAY_TIME_LOAD_PAGE)

        self.enter_id(browser, lookup_code)
        util_rpa.enter_captcha(self.get_name(), browser, By.CLASS_NAME, By.ID,
                               lottemart_constant.IMG_CAPTCHA_BY_CLASS_TYPE,
                               lottemart_constant.TEXT_BOX_CAPTCHA_BY_ID,
                               By.ID, lottemart_constant.FORM_BY_ID_TYPE, By.XPATH,
                               lottemart_constant.ERROR_ALERT_BY_XPATH, lottemart_constant.RETRY_MAX,
                               lottemart_constant.DELAY_TIME_SKIP, check_num=True, callback=self.enter_id,
                               callback_args=[browser, lookup_code])

        logging.info(f'{self.get_name()}: Download pdf')
        pdf_download = browser.find_element(By.XPATH, lottemart_constant.DOWNLOAD_PDF_BY_XPATH)
        pdf_download.click()
        logging.info(f'{self.get_name()}: Please wait .. ({lottemart_constant.DELAY_TIME_SKIP}s)')
        time.sleep(lottemart_constant.DELAY_TIME_SKIP)
        logging.info(f'{self.get_name()}: Open view detail')
        view_btn = browser.find_element(By.XPATH, lottemart_constant.VIEW_BTN_BY_XPATH)
        view_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({lottemart_constant.DELAY_TIME_SKIP}s)')
        time.sleep(lottemart_constant.DELAY_TIME_SKIP)

        logging.info(f'{self.get_name()}: Download file Zip xml')
        download_btn = browser.find_element(By.NAME, lottemart_constant.DOWNLOAD_ZIP_BTN_BY_NAME_TYPE)
        download_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({lottemart_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(lottemart_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # extra zip
        directory_path = f"{storage_pth}/{self.get_name().lower()}/{filename}"
        util_rpa.extract_zip_files_and_keep_specific_files(directory_path)
        time.sleep(lottemart_constant.DELAY_TIME_SKIP)
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return lottemart_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': lottemart_constant.LATEST_VERSION,
            'info': lottemart_constant.VERSIONS[lottemart_constant.LATEST_VERSION]
        }


lotte_ins = LotteMartRpa(lottemart_constant.META_DATA)


if __name__ == '__main__':
    lotte_ins.extract_data("https://lottemart-bdg-tt78.vnpt-invoice.com.vn",
                           "01005_20231103_18",
                           cfg.TEST_ROOT_PTH,
                           "test")
    lotte_ins.reset()
