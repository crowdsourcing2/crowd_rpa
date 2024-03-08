import logging
import time
from abc import ABC

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from crowd_rpa.cores.cyberbill.constant import cyberbill_constant
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.utils.rpa_util import util_rpa
from driver import WebDriver


class CyberbillRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return cyberbill_constant.META_DATA['RPA_NAME']

    def get_code_lookup(self):
        # TODO: you must be code here!
        return cyberbill_constant.META_DATA['URL']

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({cyberbill_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(cyberbill_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_code_lookup())
        logging.info(f'{self.get_name()}: Open a website: {self.get_code_lookup()}')
        time.sleep(cyberbill_constant.DELAY_TIME_LOAD_PAGE)
        # Enter lookup code
        logging.info(f'{self.get_name()}: Entenr lookup code')
        wait = WebDriverWait(browser, 15)  # Đợi 10 giây
        input_id = wait.until(EC.visibility_of_element_located((By.NAME, cyberbill_constant.INPUT_ID_BY_NAME)))
        input_id.send_keys("2E2EYBV8S3AG")
        # Enter captcha
        util_rpa.enter_captcha(self.get_name(), browser, By.XPATH, By.XPATH,
                                   cyberbill_constant.CAPTCHA_IMG_BY_XPATH,
                                   cyberbill_constant.CAPTCHA_INPUT_BY_XPATH, By.XPATH,
                                   cyberbill_constant.BUTTON_SEARCH_BY_XPATH, By.CLASS_NAME,
                                   cyberbill_constant.ERROR_ALERT_BY_CLASS, cyberbill_constant.RETRY_MAX, cyberbill_constant.DELAY_TIME_SKIP, check_num=True)
        time.sleep(cyberbill_constant.DELAY_TIME_SKIP)
        logging.info(f'{self.get_name()}: Download PDF')
        download_pdf = browser.find_element(By.XPATH, cyberbill_constant.DOWNLOAD_PDF_XPATH)
        download_pdf.click()
        download_pdf.click()
        download_pdf.click()
        download_pdf.click()
        logging.info(f'{self.get_name()}: Please wait .. ({cyberbill_constant.DELAY_TIME_SKIP}s)')
        time.sleep(cyberbill_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        logging.info(f'{self.get_name()}: Download XML')
        download_xml = browser.find_element(By.XPATH, cyberbill_constant.DOWNLOAD_XML_XPATH)
        download_xml.click()
        logging.info(f'{self.get_name()}: Please wait .. ({cyberbill_constant.DELAY_TIME_SKIP}s)')

        time.sleep(cyberbill_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return cyberbill_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': cyberbill_constant.LATEST_VERSION,
            'info': cyberbill_constant.VERSIONS[cyberbill_constant.LATEST_VERSION]
        }


if __name__ == '__main__':
    cyberbill_rpa_ins = CyberbillRpa(cyberbill_constant.META_DATA)
    cyberbill_rpa_ins.extract_data()
    cyberbill_rpa_ins.reset()