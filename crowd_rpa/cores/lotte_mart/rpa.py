import time
import logging
from abc import ABC

from driver import WebDriver
from selenium.webdriver.common.by import By

from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.lotte_mart.constant import lottemart_constant


class LotteMartRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def get_code_lookup(self):
        code_bill = ""
        path = lottemart_constant.FILE_PATH
        if path.endswith(".pdf"):
            code_bill = util_rpa.read_pdf(path, lottemart_constant.CODE_BILL_KEYWORD,
                                          lottemart_constant.LAST_KEYWORD)
        elif path.endswith(".xml"):
            code_bill = util_rpa.read_xml(path, lottemart_constant.CODE_BILL_KEYWORD)
        return code_bill

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return lottemart_constant.META_DATA['RPA_NAME']

    def enter_id(self, browser):
        text_box = browser.find_element(By.CLASS_NAME, lottemart_constant.TEXT_BOX_BY_CLASS_TYPE)
        text_box.send_keys(self.get_code_lookup())
        logging.info(f'{self.get_name()}: Enter code lookup: {self.get_code_lookup()}')

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({lottemart_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(lottemart_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        logging.info(f'{self.get_name()}: Open a website: {self.get_portal()}')
        browser.get(self.get_portal())
        logging.info(f'{self.get_name()}: Please wait .. ({lottemart_constant.DELAY_TIME_LOAD_PAGE}s)')
        time.sleep(lottemart_constant.DELAY_TIME_LOAD_PAGE)

        self.enter_id(browser)
        util_rpa.enter_captcha(self.get_name(), browser, By.CLASS_NAME, By.ID,
                               lottemart_constant.IMG_CAPTCHA_BY_CLASS_TYPE,
                               lottemart_constant.TEXT_BOX_CAPTCHA_BY_ID,
                               By.ID, lottemart_constant.FORM_BY_ID_TYPE, By.XPATH,
                               lottemart_constant.ERROR_ALERT_BY_XPATH, lottemart_constant.RETRY_MAX,
                               lottemart_constant.DELAY_TIME_SKIP, check_num=True, callback=self.enter_id,
                               callback_args=[browser])

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
        browser.quit()
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
    lotte_ins.extract_data()
    lotte_ins.reset()
