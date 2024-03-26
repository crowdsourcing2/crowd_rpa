import os
import time
import logging

from abc import ABC
from os.path import join
from pathlib import Path

from crowd_rpa.settings import cfg
from crowd_rpa.driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.evat.constant import evat_constant


class EvatRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def get_code_lookup(self):
        lookup_code = ""
        path = evat_constant.FILE_PATH
        if path.endswith(".pdf"):
            lookup_code = util_rpa.read_pdf(path, evat_constant.LOOKUP_KEYWORD,
                                            evat_constant.COMPANY_KEYWORD)
        elif path.endswith(".xml"):
            lookup_code = util_rpa.read_xml(path, evat_constant.LOOKUP_KEYWORD)
        return lookup_code

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory, more_option=more_option)()

    def get_name(self):
        return evat_constant.META_DATA['RPA_NAME']

    def extract_data(self, portal, lookup_code, storage_pth, filename, company_code=None):
        self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename, company_code)

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename, company_code):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        portal_pth = os.path.join(storage_pth, evat_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth)
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({evat_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(evat_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(portal)
        logging.info(f'{self.get_name()}: Open a website: {portal}')
        time.sleep(evat_constant.DELAY_TIME_LOAD_PAGE)
        code = browser.find_element(By.CSS_SELECTOR, ".login-form > div:nth-child(2) > input")
        code.send_keys(lookup_code)
        company = browser.find_element(By.CSS_SELECTOR, ".login-form > div:nth-child(3) > input")
        company.send_keys(company_code)

        view_button = browser.find_element(By.CSS_SELECTOR, ".btn.blue")
        view_button.click()

        # _aflist > tr > td.td-actions.text-center.w220 > a.go-link.btn.btn-info.btn-sm

        link_element = browser.find_element(By.XPATH, "//a[contains(@title, 'Tải file hóa đơn')]")
        link_element.click()
        view_button2 = browser.find_element(By.XPATH, '//*[@class="go-link btn btn-success btn-sm"]')
        browser.execute_script("arguments[0].removeAttribute('target')", view_button2)
        view_button2.click()
        time.sleep(evat_constant.DELAY_TIME_SKIP)
        src_pth = join(storage_pth, evat_constant.CORE_NAME.lower())
        util_rpa.extract_zip_files_and_keep_specific_files(join(src_pth, filename))
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return evat_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': evat_constant.LATEST_VERSION,
            'info': evat_constant.VERSIONS[evat_constant.LATEST_VERSION]
        }


evat_ins = EvatRpa(evat_constant.META_DATA)

if __name__ == '__main__':
    evat_ins.extract_data("http://tracuu.evat.vn",
                          "XYKZZCQQAL",
                          cfg.TEST_ROOT_PTH,
                          'test',
                          company_code='0313123200')

    evat_ins.reset()
