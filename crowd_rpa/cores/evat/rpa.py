import time
import logging
from abc import ABC
from driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.evat.constant import evat_constant
from crowd_rpa.utils.rpa_util import util_rpa


class EvatRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def get_portal(self):
        url = ""
        path = evat_constant.FILE_PATH
        if path.endswith(".pdf"):
            url = util_rpa.read_pdf(path, evat_constant.URL_KEYWORD,
                                    evat_constant.LOOKUP_KEYWORD)
        elif path.endswith(".xml"):
            url = util_rpa.read_xml(path, evat_constant.URL_KEYWORD)

        return url

    def get_code_lookup(self):
        lookup_code = ""
        path = evat_constant.FILE_PATH
        if path.endswith(".pdf"):
            lookup_code = util_rpa.read_pdf(path, evat_constant.LOOKUP_KEYWORD,
                                            evat_constant.COMPANY_KEYWORD)
        elif path.endswith(".xml"):
            lookup_code = util_rpa.read_xml(path, evat_constant.LOOKUP_KEYWORD)
        return lookup_code

    def extract_data(self):
        self.process_download_xml_pdf()

    def check_invoice(self):
        company_code = ""
        path = evat_constant.FILE_PATH
        if path.endswith(".pdf"):
            company_code = util_rpa.read_pdf(path, evat_constant.COMPANY_KEYWORD,
                                             evat_constant.LAST_KEYWORD)
        elif path.endswith(".xml"):
            company_code = util_rpa.read_xml(path, evat_constant.COMPANY_KEYWORD)
        return company_code

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return evat_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        browser = self.get_driver()

        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({evat_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(evat_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_portal())
        logging.info(f'{self.get_name()}: Open a website: {self.get_portal()}')
        time.sleep(evat_constant.DELAY_TIME_LOAD_PAGE)

        lookupcode = browser.find_element(By.CSS_SELECTOR, ".login-form > div:nth-child(2) > input")
        lookupcode.send_keys(self.get_code_lookup())

        companycode = browser.find_element(By.CSS_SELECTOR, ".login-form > div:nth-child(3) > input")
        companycode.send_keys(self.check_invoice())

        view_button = browser.find_element(By.CSS_SELECTOR, ".btn.blue")
        view_button.click()

        # _aflist > tr > td.td-actions.text-center.w220 > a.go-link.btn.btn-info.btn-sm

        link_element = browser.find_element(By.XPATH, "//a[contains(@title, 'Tải file hóa đơn')]")
        link_element.click()
        view_button2 = browser.find_element(By.XPATH, '//*[@class="go-link btn btn-success btn-sm"]')
        browser.execute_script("arguments[0].removeAttribute('target')", view_button2)
        view_button2.click()

        time.sleep(evat_constant.DELAY_TIME_SKIP)

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
    evat_ins.extract_data()
    evat_ins.reset()
