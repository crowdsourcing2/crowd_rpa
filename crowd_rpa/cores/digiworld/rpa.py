import logging
import time
from abc import ABC
from selenium.webdriver.common.by import By

from crowd_rpa.cores.digiworld.constant import digi_world_constant
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.utils.rpa_util import util_rpa
from driver import WebDriver


class DigiWorldRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def get_portal(self):
        url = ""
        path = digi_world_constant.FILE_PATH
        if path.endswith(".pdf"):
            url = util_rpa.read_pdf(path, digi_world_constant.URL_KEYWORD,
                                    digi_world_constant.CODE_BILL_KEYWORD)
        elif path.endswith(".xml"):
            url = util_rpa.read_xml(path, digi_world_constant.URL_KEYWORD)

        return url

    def get_code_lookup(self):
        code_bill = ""
        path = digi_world_constant.FILE_PATH
        if path.endswith(".pdf"):
            code_bill = util_rpa.read_pdf(path, digi_world_constant.CODE_BILL_KEYWORD,
                                          digi_world_constant.LAST_KEYWORD)
        elif path.endswith(".xml"):
            code_bill = util_rpa.read_xml(path, digi_world_constant.CODE_BILL_KEYWORD)
        return code_bill

    def check_invoice(self):
        return None

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return digi_world_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({digi_world_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(digi_world_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_portal())
        logging.info(f'{self.get_name()}: Open a website: {self.get_portal()}')
        time.sleep(digi_world_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({digi_world_constant.DELAY_TIME_LOAD_PAGE}s)')
        # Enter id
        id_input = browser.find_element(By.ID, digi_world_constant.ID_INPUT_BY_ID_TYPE)
        id_input.send_keys(self.get_code_lookup())
        logging.info(f'{self.get_name()}: Enter id')
        # Enter captcha
        util_rpa.enter_captcha(self.get_name(), browser, By.CLASS_NAME, By.ID,
                               digi_world_constant.CAPTCHA_IMG_BY_CLASS_TYPE,
                               digi_world_constant.CAPTCHA_INPUT_BY_ID_TYPE,
                               By.ID, digi_world_constant.FORM_BY_ID_TYPE, By.XPATH,
                               digi_world_constant.ERROR_ALERT_BY_XPATH, digi_world_constant.RETRY_MAX,
                               digi_world_constant.DELAY_TIME_SKIP, check_num=True)
        # Open view detail
        logging.info(f'{self.get_name()}: Open view detail')
        view_btn = browser.find_element(By.XPATH, digi_world_constant.VIEW_BTN_BY_XPATH)
        view_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({digi_world_constant.DELAY_TIME_SKIP}s)')
        time.sleep(digi_world_constant.DELAY_TIME_SKIP)
        # Download file pdf and xml
        logging.info(f'{self.get_name()}: Download pdf and xml')
        download_btn = browser.find_element(By.NAME, digi_world_constant.DOWNLOAD_BTN_BY_NAME_TYPE)
        download_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({digi_world_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(digi_world_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # Close rpa
        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return digi_world_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': digi_world_constant.LATEST_VERSION,
            'info': digi_world_constant.VERSIONS[digi_world_constant.LATEST_VERSION]
        }


digi_world_ins = DigiWorldRpa(digi_world_constant.META_DATA)


if __name__ == '__main__':
    digi_world_ins.extract_data()
    digi_world_ins.reset()
