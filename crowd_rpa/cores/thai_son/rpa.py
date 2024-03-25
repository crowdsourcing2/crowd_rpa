import time
import logging
from abc import ABC

from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.thai_son.constant import thai_son_constant


class ThaiSonRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def get_portal(self):
        url = ""
        path = thai_son_constant.FILE_PATH
        if path.endswith(".pdf"):
            url = util_rpa.read_pdf(path, thai_son_constant.URL_KEYWORD,
                                    thai_son_constant.LAST_KEYWORD)
        elif path.endswith(".xml"):
            url = util_rpa.read_xml(path, thai_son_constant.URL_KEYWORD)
        return url

    def get_code_lookup(self):
        code_bill = ""
        path = thai_son_constant.FILE_PATH
        if path.endswith(".pdf"):
            code_bill = util_rpa.read_pdf(path, thai_son_constant.CODE_BILL_KEYWORD,
                                          thai_son_constant.URL_KEYWORD)
        elif path.endswith(".xml"):
            code_bill = util_rpa.read_xml(path, thai_son_constant.CODE_BILL_KEYWORD)
        return code_bill

    def check_invoice(self):
        return None

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return thai_son_constant.META_DATA['RPA_NAME']

    def enter_id(self, browser):
        logging.info(f'{self.get_name()}: Please wait .. ({thai_son_constant.DELAY_TIME_LOAD_PAGE}s)')
        mst_text = browser.find_element(By.XPATH, thai_son_constant.MA_NHAN_HOA_DON_XPATH)
        mst_text.send_keys(self.get_code_lookup())

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({thai_son_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(thai_son_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_portal())
        logging.info(f'{self.get_name()}: Open a website: {self.get_portal()}')
        time.sleep(thai_son_constant.DELAY_TIME_LOAD_PAGE)
        # Enter ID
        self.enter_id(browser)
        #ClearCaptCha
        util_rpa.enter_captcha(self.get_name(), browser, By.XPATH, By.XPATH,
                               thai_son_constant.CAPTCHA_IMG_XPATH,
                               thai_son_constant.CAPTCHA_TEXT_XPATH,
                               By.XPATH, thai_son_constant.BTN_FORM_BY_XPATH_TYPE, By.XPATH,
                               thai_son_constant.ERROR_XPATH, thai_son_constant.RETRY_MAX,
                               thai_son_constant.DELAY_TIME_SKIP, callback=self.enter_id, callback_args=[browser],
                               form_btn_handle="click")
        # Download file zip
        logging.info(f'{self.get_name()}: Download Zip')
        download_zip = browser.find_element(By.XPATH, thai_son_constant.DOWNLOAD_ZIP_XPATH)
        download_zip.click()
        logging.info(f'{self.get_name()}: Please wait .. ({thai_son_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(thai_son_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return thai_son_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': thai_son_constant.LATEST_VERSION,
            'info': thai_son_constant.VERSIONS[thai_son_constant.LATEST_VERSION]
        }


thai_son_ins = ThaiSonRpa(thai_son_constant.META_DATA)


if __name__ == '__main__':
    thai_son_ins.extract_data()
    thai_son_ins.reset()
