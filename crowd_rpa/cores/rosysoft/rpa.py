import logging
import time
from abc import ABC
from driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.rosysoft.constant import rosysoft_constant


class RosySoftRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return rosysoft_constant.META_DATA['RPA_NAME']

    def get_code_lookup(self):
        # TODO: you must be code here!
        return {'tax_code': '0302035520', 'lookup_code': 'A01TXL000630801'}

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf.')

        browser = self.get_driver()
        browser.maximize_window()
        browser.get(rosysoft_constant.META_DATA['URL'])
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(rosysoft_constant.DELAY_OPEN_MAXIMUM_BROWSER)

        logging.info(f'{self.get_name()}: Open a website: {rosysoft_constant.URL}')
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_LOAD_PAGE}s)')
        time.sleep(rosysoft_constant.DELAY_TIME_LOAD_PAGE)

        tab2_button = browser.find_element(By.ID, rosysoft_constant.TAB2_BUTTON_BY_CLASS_TYPE)
        tab2_button.click()
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_SKIP}s)')
        time.sleep(rosysoft_constant.DELAY_TIME_SKIP)

        logging.info(f'{self.get_name()}: Enter data code lookup: {self.get_code_lookup()} into the from.')
        text_box_tax_code = browser.find_element(By.ID, rosysoft_constant.TEXT_TAXCODE_BY_ID_TYPE)
        text_box_tax_code.send_keys(self.get_code_lookup()['tax_code'])
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_SKIP}s)')
        time.sleep(rosysoft_constant.DELAY_TIME_SKIP)

        text_box_search_code = browser.find_element(By.ID, rosysoft_constant.TEXT_SEARCH_CODE_BY_ID_TYPE)
        text_box_search_code.send_keys(self.get_code_lookup()['lookup_code'])
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


if __name__ == '__main__':
    rosy_rpa_ins = RosySoftRpa(rosysoft_constant.META_DATA)
    rosy_rpa_ins.extract_data()
    rosy_rpa_ins.reset()
