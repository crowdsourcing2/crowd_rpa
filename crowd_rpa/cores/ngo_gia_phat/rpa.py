import time
import logging
from abc import ABC

from crowd_rpa.driver import WebDriver
from selenium.webdriver.common.by import By

from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.ngo_gia_phat.constant import ngo_gia_phat_constant
from crowd_rpa.settings import cfg


class NgoGiaPhatRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory)()

    def get_name(self):
        return ngo_gia_phat_constant.META_DATA['RPA_NAME']


    def send_key_str(self, browser, lookup_code):
        text_box = browser.find_element(By.XPATH, ngo_gia_phat_constant.INPUT_BY_XPATH_ID)
        text_box.send_keys(lookup_code)
        logging.info(f'{self.get_name()}: Enter code lookup: {lookup_code}')

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')

        browser = self.get_driver()
        browser.maximize_window()

        logging.info(f'{self.get_name()}: Please wait .. ({ngo_gia_phat_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(ngo_gia_phat_constant.DELAY_OPEN_MAXIMUM_BROWSER)

        logging.info(f'{self.get_name()}: Open a website: {portal}')
        browser.get(portal)
        logging.info(f'{self.get_name()}: Please wait .. ({ngo_gia_phat_constant.DELAY_TIME_LOAD_PAGE}s)')
        time.sleep(ngo_gia_phat_constant.DELAY_TIME_LOAD_PAGE)

        self.send_key_str(browser, lookup_code)

        util_rpa.enter_captcha(self.get_name(), browser, By.XPATH, By.XPATH,
                               ngo_gia_phat_constant.IMG_CAPTCHA_BY_XPATH,
                               ngo_gia_phat_constant.BUTTON_FIND_BILL_XPATH,
                               By.ID, ngo_gia_phat_constant.FORM_BY_ID_TYPE, By.XPATH,
                               ngo_gia_phat_constant.ERROR_ALERT_BY_XPATH, ngo_gia_phat_constant.RETRY_MAX,
                               ngo_gia_phat_constant.DELAY_TIME_SKIP, check_num=True, callback=self.send_key_str,
                               callback_args=[browser])

        # find_bill_btn = browser.find_element(By.XPATH, ngo_gia_phat_constant.BUTTON_FIND_BILL_XPATH)
        # find_bill_btn.click()

        logging.info(f'{self.get_name()}: Please wait .. ({ngo_gia_phat_constant.DELAY_TIME_SKIP}s)')
        time.sleep(ngo_gia_phat_constant.DELAY_TIME_SKIP)
        logging.info(f'{self.get_name()}: Open view detail')

        logging.info(f'{self.get_name()}: Download file Zip xml')
        download_btn = browser.find_element(By.XPATH, ngo_gia_phat_constant.BUTTON_DOWNLOAD_BY_XPATH)
        download_btn.click()

        logging.info(f'{self.get_name()}: Please wait .. ({ngo_gia_phat_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(ngo_gia_phat_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        browser.quit()

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
    ngo_gia_phat_ins.extract_data("https://tracuuonline78.ngogiaphat.vn/Search",
                          "2747B58278DC46D9892D6FB3C0EFA81F",
                                  cfg.TEST_ROOT_PTH,
                          "test")

    ngo_gia_phat_ins.reset()
