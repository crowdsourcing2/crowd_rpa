import os
import time
import logging
from abc import ABC
from pathlib import Path

from crowd_rpa.driver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from crowd_rpa.settings import cfg
from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.express.constant import express_constant


class ExpressRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def get_code_lookup(self):
        code_bill = ""
        path = express_constant.FILE_PATH
        if path.endswith(".pdf"):
            code_bill = util_rpa.read_pdf(path, express_constant.CODE_BILL_KEYWORD,
                                          express_constant.LAST_KEYWORD)
        elif path.endswith(".xml"):
            code_bill = util_rpa.read_xml(path, express_constant.CODE_BILL_KEYWORD)
        return code_bill

    def extract_data(self, portal, lookup_code, storage_pth, filename):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory,
                         more_option=more_option)()

    def get_name(self):
        return express_constant.META_DATA['RPA_NAME']

    def enter_id(self, browser, lookup_code):
        text_box = browser.find_element(By.XPATH, express_constant.TEXT_BOX_BY_XPATH)
        text_box.send_keys(lookup_code)
        logging.info(f'{self.get_name()}: Enter code lookup: {lookup_code}')

    def download_file(self, file_type, browser, btn_download_find_by, value_btn_download):
        logging.info(f'{self.get_name()}: Download {file_type.upper()}')
        download_btn = browser.find_element(btn_download_find_by, value_btn_download)

        wait = WebDriverWait(browser, express_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((btn_download_find_by, value_btn_download)))

        download_btn.click()

        logging.info(f'{self.get_name()}: Please wait .. ({express_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(express_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')

        # Maximize the browser window to full screen
        portal_pth = os.path.join(storage_pth, express_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)

        browser = self.get_driver(save_pth, True)
        browser.maximize_window()

        logging.info(f'{self.get_name()}: Please wait .. ({express_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(express_constant.DELAY_OPEN_MAXIMUM_BROWSER)

        # Open a website
        browser.get(portal)
        logging.info(f'{self.get_name()}: Open a website: {portal}')
        time.sleep(express_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({express_constant.DELAY_TIME_LOAD_PAGE}s)')

        # Enter id
        self.enter_id(browser, lookup_code)

        # Click Download
        time.sleep(express_constant.DELAY_TIME_SKIP)
        logging.info(f'{self.get_name()}: Please wait .. ({express_constant.DELAY_TIME_SKIP}s)')
        self.download_file('PDF XML', browser, By.XPATH, express_constant.BTN_DOWNLOAD_PDF_XML_BY_XPATH)

        time.sleep(express_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        # extra zip
        directory_path = f"{storage_pth}/{self.get_name().lower()}/test"
        os.makedirs(directory_path, exist_ok=True)
        util_rpa.extract_zip_files_and_keep_specific_files(directory_path)
        time.sleep(express_constant.DELAY_TIME_SKIP)

        # Close rpa
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')
        return save_pth

    def versions(self) -> dict:
        return express_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': express_constant.LATEST_VERSION,
            'info': express_constant.VERSIONS[express_constant.LATEST_VERSION]
        }


express_ins = ExpressRpa(express_constant.META_DATA)

if __name__ == '__main__':
    express_ins.extract_data("https://hoadon.247express.vn",
                             "NDYH34145ZUUX7OUTV1CMS2Z",
                             cfg.TEST_ROOT_PTH,
                             "test")
    express_ins.reset()
