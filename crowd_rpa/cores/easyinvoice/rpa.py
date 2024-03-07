import time
import logging
from abc import ABC

from crowd_rpa.utils.rpa_util import util_rpa
from driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.easyinvoice.constant import easy_invoice_constant


class EasyInvoiceRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def get_portal(self):
        url = ""
        path = easy_invoice_constant.FILE_PATH
        if path.endswith(".pdf"):
            url = util_rpa.read_pdf(path, easy_invoice_constant.URL_KEYWORD,
                                    easy_invoice_constant.CODE_BILL_KEYWORD)
        elif path.endswith(".xml"):
            url = util_rpa.read_xml(path, easy_invoice_constant.URL_KEYWORD)

        return url

    def get_code_lookup(self):
        code_bill = ""
        path = easy_invoice_constant.FILE_PATH
        if path.endswith(".pdf"):
            code_bill = util_rpa.read_pdf(path, easy_invoice_constant.CODE_BILL_KEYWORD,
                                          easy_invoice_constant.LAST_KEYWORD)
        elif path.endswith(".xml"):
            code_bill = util_rpa.read_xml(path, easy_invoice_constant.CODE_BILL_KEYWORD)
        return code_bill

    def check_invoice(self):
        return None

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return easy_invoice_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        # Thực hiện các thay đổi sau khi đã tạo đối tượng WebDriver
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({easy_invoice_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(easy_invoice_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        logging.info(f'{self.get_name()}: Open a website: {self.get_portal()}')
        browser.get(self.get_portal())
        time.sleep(easy_invoice_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({easy_invoice_constant.DELAY_TIME_LOAD_PAGE}s)')
        # Enter id
        logging.info(f'{self.get_name()}: Enter id')
        id_input = browser.find_element(By.ID, easy_invoice_constant.ID_INPUT_BY_ID_TYPE)
        id_input.send_keys(self.get_code_lookup())
        # Enter captcha
        util_rpa.enter_captcha(self.get_name(), browser, By.ID, By.ID,
                               easy_invoice_constant.CAPTCHA_IMG_BY_ID_TYPE,
                               easy_invoice_constant.CAPTCHA_INPUT_BY_ID_TYPE,
                               By.ID, easy_invoice_constant.FORM_BY_ID_TYPE, By.CLASS_NAME,
                               easy_invoice_constant.ERROR_ALERT_BY_CLASS_TYPE, easy_invoice_constant.RETRY_MAX,
                               easy_invoice_constant.DELAY_TIME_SKIP, check_num=True)
        # Download file pdf
        logging.info(f'{self.get_name()}: Download pdf')
        download_pdf_btn = browser.find_element(By.XPATH, easy_invoice_constant.DOWNLOAD_PDF_XPATH)
        download_pdf_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({easy_invoice_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(easy_invoice_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # Download file xml
        logging.info(f'{self.get_name()}: Download xml')
        download_xml_btn = browser.find_element(By.XPATH, easy_invoice_constant.DOWNLOAD_XML_XPATH)
        download_xml_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({easy_invoice_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(easy_invoice_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # Close rpa
        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return easy_invoice_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': easy_invoice_constant.LATEST_VERSION,
            'info': easy_invoice_constant.VERSIONS[easy_invoice_constant.LATEST_VERSION]
        }


if __name__ == '__main__':
    easy_invoice_rpa_ins = EasyInvoiceRpa(easy_invoice_constant.META_DATA)
    easy_invoice_rpa_ins.extract_data()
    easy_invoice_rpa_ins.reset()
