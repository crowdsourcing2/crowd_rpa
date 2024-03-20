import logging
import time
from abc import ABC

from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.rosysoft.constant import rosysoft_constant


class RosySoftRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def get_portal(self):
        url = ""
        path = rosysoft_constant.FILE_PATH
        if path.endswith(".pdf"):
            url = util_rpa.read_pdf(path, rosysoft_constant.URL_KEYWORD,
                                    rosysoft_constant.CODE_BILL_KEYWORD)
        elif path.endswith(".xml"):
            url = util_rpa.read_xml(path, rosysoft_constant.URL_KEYWORD)
        print(url)
        return url

    def get_code_lookup(self):
        code_bill = ""
        path = rosysoft_constant.FILE_PATH
        if path.endswith(".pdf"):
            code_bill = util_rpa.read_pdf(path, rosysoft_constant.CODE_BILL_KEYWORD,
                                          rosysoft_constant.LAST_KEYWORD)
        elif path.endswith(".xml"):
            code_bill = util_rpa.read_xml(path, rosysoft_constant.CODE_BILL_KEYWORD)
        return code_bill

    def check_invoice(self):
        taxt_code = ""
        path = rosysoft_constant.FILE_PATH
        if path.endswith(".pdf"):
            taxt_code = util_rpa.read_pdf(path, rosysoft_constant.TAX_CODE_KEYWORD,
                                          rosysoft_constant.LAST_TAXT_KEYWORD)
        elif path.endswith(".xml"):
            taxt_code = util_rpa.read_xml(path, rosysoft_constant.TAX_CODE_KEYWORD)
        taxt_code = taxt_code.replace(' ', '')
        return taxt_code

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return rosysoft_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf.')

        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(rosysoft_constant.DELAY_OPEN_MAXIMUM_BROWSER)

        browser.get(self.get_portal())
        logging.info(f'{self.get_name()}: Open a website: {self.get_portal()}')
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_LOAD_PAGE}s)')
        time.sleep(rosysoft_constant.DELAY_TIME_LOAD_PAGE)

        tab2_button = browser.find_element(By.ID, rosysoft_constant.TAB2_BUTTON_BY_ID_TYPE)
        tab2_button.click()
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_SKIP}s)')
        time.sleep(rosysoft_constant.DELAY_TIME_SKIP)

        logging.info(f'{self.get_name()}: Enter data code lookup: {self.check_invoice()} into the from.')
        text_box_tax_code = browser.find_element(By.ID, rosysoft_constant.TEXT_TAXCODE_BY_ID_TYPE)
        text_box_tax_code.send_keys(self.check_invoice())
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_SKIP}s)')
        time.sleep(rosysoft_constant.DELAY_TIME_SKIP)

        text_box_search_code = browser.find_element(By.ID, rosysoft_constant.TEXT_SEARCH_CODE_BY_ID_TYPE)
        text_box_search_code.send_keys(self.get_code_lookup())
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_SKIP}s)')
        time.sleep(rosysoft_constant.DELAY_TIME_SKIP)

        logging.info(f'{self.get_name()}: Submit data code lookup.')
        submit_btn = browser.find_element(By.CSS_SELECTOR, rosysoft_constant.SUBMIT_BTN_BY_ID_TYPE)
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_SKIP}s)')
        submit_btn.click()
        time.sleep(rosysoft_constant.DELAY_TIME_SKIP)

        logging.info(f'{self.get_name()}: URL redirection: {rosysoft_constant.URL_N}.')
        browser.get(rosysoft_constant.URL_N)
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_LOAD_PAGE}s)')
        time.sleep(rosysoft_constant.DELAY_TIME_LOAD_PAGE)

        logging.info(f'{self.get_name()}: Download PDF')
        pdf_down = browser.find_element(By.XPATH, rosysoft_constant.DOWNLOAD_PDF_XPATH)
        pdf_down.click()
        logging.info(f'{self.get_name()}:Please wait .. ({rosysoft_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(rosysoft_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        logging.info(f'{self.get_name()}: Download XML')
        xml_down = browser.find_element(By.XPATH, rosysoft_constant.DOWNLOAD_XML_XPATH)
        xml_down.click()
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(rosysoft_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return rosysoft_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': rosysoft_constant.LATEST_VERSION,
            'info': rosysoft_constant.VERSIONS[rosysoft_constant.LATEST_VERSION]
        }


rosy_soft_ins = RosySoftRpa(rosysoft_constant.META_DATA)


if __name__ == '__main__':
    rosy_soft_ins.extract_data()
    rosy_soft_ins.reset()
