import os
import time
import logging
from abc import ABC
from pathlib import Path

from selenium.webdriver.common.by import By

from crowd_rpa.settings import cfg
from crowd_rpa.driver import WebDriver
from crowd_rpa.utils.rpa_util import util_rpa
from crowd_rpa.interfaces.rpa_interface import IRpa

from crowd_rpa.cores.easyinvoice.constant import easy_invoice_constant


class EasyInvoiceRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self, portal, lookup_code, storage_pth, filename):
        return self.process_download_xml_pdf(portal, lookup_code, storage_pth, filename)

    def get_driver(self, download_directory=None, more_option=False):
        return WebDriver(tag=self.driver_name, download_directory=download_directory,
                         more_option=more_option)()

    def get_name(self):
        return easy_invoice_constant.META_DATA['RPA_NAME']

    def process_download_xml_pdf(self, portal, lookup_code, storage_pth, filename):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        portal_pth = os.path.join(storage_pth, easy_invoice_constant.CORE_NAME.lower())
        if not Path(portal_pth).is_dir():
            os.mkdir(portal_pth)
        save_pth = os.path.join(portal_pth, filename)
        if not Path(save_pth):
            os.mkdir(save_pth)
        browser = self.get_driver(save_pth, True)
        # Thực hiện các thay đổi sau khi đã tạo đối tượng WebDriver
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({easy_invoice_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(easy_invoice_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        logging.info(f'{self.get_name()}: Open a website: {portal}')
        browser.get(portal)
        time.sleep(easy_invoice_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({easy_invoice_constant.DELAY_TIME_LOAD_PAGE}s)')
        # Enter id
        logging.info(f'{self.get_name()}: Enter id')
        id_input = browser.find_element(By.ID, easy_invoice_constant.ID_INPUT_BY_ID_TYPE)
        id_input.send_keys(lookup_code)
        # Enter captcha
        util_rpa.enter_captcha(self.get_name(), browser, By.ID, By.ID,
                               easy_invoice_constant.CAPTCHA_IMG_BY_ID_TYPE,
                               easy_invoice_constant.CAPTCHA_INPUT_BY_ID_TYPE,
                               By.ID, easy_invoice_constant.FORM_BY_ID_TYPE, By.CLASS_NAME,
                               easy_invoice_constant.ERROR_ALERT_BY_CLASS_TYPE, easy_invoice_constant.RETRY_MAX,
                               easy_invoice_constant.DELAY_TIME_SKIP, check_num=True,
                               callback=self.process_download_xml_pdf,
                               callback_args=[portal, lookup_code, storage_pth, filename])
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
        # extra zip
        directory_path = f"{storage_pth}/{self.get_name()}/{self.get_name().lower()}"
        util_rpa.extract_zip_files_and_keep_specific_files(directory_path)
        time.sleep(easy_invoice_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)

        # Close rpa
        browser.close()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return easy_invoice_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': easy_invoice_constant.LATEST_VERSION,
            'info': easy_invoice_constant.VERSIONS[easy_invoice_constant.LATEST_VERSION]
        }


easy_invoice_ins = EasyInvoiceRpa(easy_invoice_constant.META_DATA)

if __name__ == '__main__':
    easy_invoice_ins.extract_data("https://0401356807hd.easyinvoice.com.vn",
                                  "V6B3X7S70412674213298690",
                                  cfg.TEST_ROOT_PTH,
                                  "test")
    easy_invoice_ins.reset()
