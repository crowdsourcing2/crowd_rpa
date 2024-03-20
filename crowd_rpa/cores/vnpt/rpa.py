import time
import logging
from abc import ABC
from crowd_rpa.driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.vnpt.constant import vnpt_constant
from crowd_rpa.utils.rpa_util import util_rpa


class VnptRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def get_portal(self):
        url = ""
        path = vnpt_constant.FILE_PATH
        if path.endswith(".pdf"):
            url = util_rpa.read_pdf(path, vnpt_constant.URL_KEYWORD,
                                    vnpt_constant.CODE_BILL_KEYWORD)
        elif path.endswith(".xml"):
            url = util_rpa.read_xml(path, vnpt_constant.URL_KEYWORD)

        return url
    def get_code_lookup(self):
        code_bill = ""
        path = vnpt_constant.FILE_PATH
        if path.endswith(".pdf"):
            code_bill = util_rpa.read_pdf(path, vnpt_constant.CODE_BILL_KEYWORD,
                                          vnpt_constant.LAST_KEYWORD)
        elif path.endswith(".xml"):
            code_bill = util_rpa.read_xml(path, vnpt_constant.CODE_BILL_KEYWORD)
        return code_bill

    def extract_data(self):
        logging.info(f'{self.get_name()}: Start extracting data')
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return vnpt_constant.META_DATA['RPA_NAME']

    def enter_id(self,browser):
        id_input = browser.find_element(By.NAME, "strFkey")
        id_input.send_keys(self.get_code_lookup())
        logging.info(f'{self.get_name()}: Enter id')

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({vnpt_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(vnpt_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_portal())
        logging.info(f'{self.get_name()}: Open a website: {self.get_portal()}')
        time.sleep(vnpt_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({vnpt_constant.DELAY_TIME_LOAD_PAGE}s)')
        # Enter id
        self.enter_id(browser)
        # Enter captcha
        util_rpa.enter_captcha(self.get_name(), browser, By.CLASS_NAME, By.ID,
                               vnpt_constant.CAPTCHA_IMG_BY_CLASS_TYPE,
                               vnpt_constant.CAPTCHA_INPUT_BY_ID_TYPE,
                               By.ID, vnpt_constant.FORM_BY_ID_TYPE, By.XPATH,
                               vnpt_constant.ERROR_ALERT_BY_XPATH, vnpt_constant.RETRY_MAX,
                               vnpt_constant.DELAY_TIME_SKIP, check_num=True, callback=self.enter_id,
                               callback_args=[browser])
        # Open view detail
        logging.info(f'{self.get_name()}: Open view detail')
        view_btn = browser.find_element(By.XPATH, vnpt_constant.VIEW_BTN_BY_XPATH)
        view_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({vnpt_constant.DELAY_TIME_SKIP}s)')
        time.sleep(vnpt_constant.DELAY_TIME_SKIP)
        # Download file pdf and xml
        logging.info(f'{self.get_name()}: Download pdf and xml')
        download_btn = browser.find_element(By.NAME, vnpt_constant.DOWNLOAD_BTN_BY_NAME_TYPE)
        download_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({vnpt_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(vnpt_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # Close rpa
        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return vnpt_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': vnpt_constant.LATEST_VERSION,
            'info': vnpt_constant.VERSIONS[vnpt_constant.LATEST_VERSION]
        }


vnpt_ins = VnptRpa(vnpt_constant.META_DATA)


if __name__ == '__main__':
    vnpt_ins.extract_data()
    vnpt_ins.reset()
