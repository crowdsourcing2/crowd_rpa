import os
import time
import logging

from abc import ABC
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from crowd_rpa.settings import cfg
from crowd_rpa.driver import WebDriver
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.rosysoft.constant import rosysoft_constant


class RosySoftRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename, company_code=None):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename, company_code)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory, more_option=more_option)()

    def get_name(self):
        return rosysoft_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename, company_code):
        logging.info(f'{self.get_name()}: Start process download xml & pdf.')

        portal_pth = os.path.join(storage_pth, rosysoft_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth, True)
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(rosysoft_constant.DELAY_OPEN_MAXIMUM_BROWSER)

        browser.get(portal)
        logging.info(f'{self.get_name()}: Open a website: {portal}')
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_LOAD_PAGE}s)')
        time.sleep(rosysoft_constant.DELAY_TIME_LOAD_PAGE)

        tab2_button = browser.find_element(By.ID, rosysoft_constant.TAB2_BUTTON_BY_ID_TYPE)
        tab2_button.click()
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_SKIP}s)')
        time.sleep(rosysoft_constant.DELAY_TIME_SKIP)

        logging.info(f'{self.get_name()}: Enter data code lookup: {company_code} into the form.')
        text_box_tax_code = browser.find_element(By.ID, rosysoft_constant.TEXT_TAXCODE_BY_ID_TYPE)
        text_box_tax_code.send_keys(company_code)
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_SKIP}s)')
        time.sleep(rosysoft_constant.DELAY_TIME_SKIP)

        text_box_search_code = browser.find_element(By.ID, rosysoft_constant.TEXT_SEARCH_CODE_BY_ID_TYPE)
        text_box_search_code.send_keys(lookup_code)
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_SKIP}s)')
        time.sleep(rosysoft_constant.DELAY_TIME_SKIP)

        logging.info(f'{self.get_name()}: Submit data code lookup.')
        submit_btn = browser.find_element(By.CSS_SELECTOR, rosysoft_constant.SUBMIT_BTN_BY_ID_TYPE)
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_SKIP}s)')
        submit_btn.click()
        time.sleep(rosysoft_constant.DELAY_TIME_SKIP)

        windows = browser.window_handles
        logging.info(f'{self.get_name()}: Switch to new tab: {windows[-1]}.')
        browser.switch_to.window(windows[-1])
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_TIME_LOAD_PAGE}s)')
        time.sleep(rosysoft_constant.DELAY_TIME_LOAD_PAGE)

        logging.info(f'{self.get_name()}: Download PDF')
        pdf_down = browser.find_element(By.XPATH, rosysoft_constant.DOWNLOAD_PDF_XPATH)
        wait = WebDriverWait(browser, rosysoft_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.XPATH, rosysoft_constant.DOWNLOAD_PDF_XPATH)))
        browser.execute_script("arguments[0].click();", pdf_down)
        logging.info(f'{self.get_name()}:Please wait .. ({rosysoft_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(rosysoft_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        logging.info(f'{self.get_name()}: Download XML')
        xml_down = browser.find_element(By.XPATH, rosysoft_constant.DOWNLOAD_XML_XPATH)
        wait = WebDriverWait(browser, rosysoft_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        wait.until(ec.presence_of_element_located((By.XPATH, rosysoft_constant.DOWNLOAD_XML_XPATH)))
        browser.execute_script("arguments[0].click();", xml_down)
        logging.info(f'{self.get_name()}: Please wait .. ({rosysoft_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(rosysoft_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        browser.close()
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
    rosy_soft_ins.extract_data("https://eInv.rosySoft.vn:8386",
                               "A01TXL000630801",
                               cfg.TEST_ROOT_PTH,
                               'test',
                               company_code='0302035520')
    rosy_soft_ins.reset()
