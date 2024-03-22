import os
import time
import logging
from abc import ABC
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from crowd_rpa.settings import cfg
from crowd_rpa.driver import WebDriver
from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.cyberbill.constant import cyber_bill_constant


class CyberBillRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal: str, lookup_code: str, storage_pth: str, filename: str):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory, more_option=more_option)()

    def get_name(self):
        return cyber_bill_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        portal_pth = os.path.join(storage_pth, cyber_bill_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth, True)
        # Maximize the browser window to full screen
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({cyber_bill_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(cyber_bill_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(portal)
        logging.info(f'{self.get_name()}: Open a website: {portal}')
        time.sleep(cyber_bill_constant.DELAY_TIME_LOAD_PAGE)
        # Enter lookup code
        logging.info(f'{self.get_name()}: Entenr lookup code')
        wait = WebDriverWait(browser, 15)  # Đợi 10 giây
        input_id = wait.until(ec.visibility_of_element_located((By.NAME, cyber_bill_constant.INPUT_ID_BY_NAME)))
        input_id.send_keys(lookup_code)
        # Enter captcha
        util_rpa.enter_captcha(self.get_name(), browser, By.XPATH, By.XPATH,
                               cyber_bill_constant.CAPTCHA_IMG_BY_XPATH,
                               cyber_bill_constant.CAPTCHA_INPUT_BY_XPATH, By.XPATH,
                               cyber_bill_constant.BUTTON_SEARCH_BY_XPATH, By.CLASS_NAME,
                               cyber_bill_constant.ERROR_ALERT_BY_CLASS, cyber_bill_constant.RETRY_MAX,
                               cyber_bill_constant.DELAY_TIME_SKIP, check_num=True,
                               callback=self.process_download_xml_pdf,
                               callback_args=[portal, lookup_code, storage_pth, filename])

        time.sleep(cyber_bill_constant.DELAY_TIME_SKIP)
        time.sleep(cyber_bill_constant.DELAY_TIME_SKIP)
        logging.info(f'{self.get_name()}: Download PDF')
        download_pdf = browser.find_element(By.XPATH, cyber_bill_constant.DOWNLOAD_PDF_XPATH)
        download_pdf.click()
        download_pdf.click()
        download_pdf.click()
        download_pdf.click()
        logging.info(f'{self.get_name()}: Please wait .. ({cyber_bill_constant.DELAY_TIME_SKIP}s)')
        time.sleep(cyber_bill_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        logging.info(f'{self.get_name()}: Download XML')
        download_xml = browser.find_element(By.XPATH, cyber_bill_constant.DOWNLOAD_XML_XPATH)
        download_xml.click()
        logging.info(f'{self.get_name()}: Please wait .. ({cyber_bill_constant.DELAY_TIME_SKIP}s)')

        time.sleep(cyber_bill_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return cyber_bill_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': cyber_bill_constant.LATEST_VERSION,
            'info': cyber_bill_constant.VERSIONS[cyber_bill_constant.LATEST_VERSION]
        }


cyber_bill_ins = CyberBillRpa(cyber_bill_constant.META_DATA)

if __name__ == '__main__':
    cyber_bill_ins.extract_data("https://tracuu.cyberbill.vn",
                                "2E2EYBV8S3AG",
                                cfg.TEST_ROOT_PTH,
                                "test")
    cyber_bill_ins.reset()
