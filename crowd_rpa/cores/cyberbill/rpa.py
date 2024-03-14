import logging
import time
from abc import ABC

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from crowd_rpa.cores.cyberbill.constant import cyber_bill_constant
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
        return cyber_bill_constant.META_DATA['RPA_NAME']

    def check_invoice(self):
        return None

    def get_portal(self):
        urls = self.read_pdf()
        if urls:
            return urls[0]
        else:
            print("Khong tim thay duong dan")
            return ""

    def get_code_lookup(self):
        code = self.read_look_code()
        return code

    def read_look_code(self):
        codes = []
        try:
            with open(cyber_bill_constant.PATH_PDF_FILE, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    text = pdf_reader.pages[page_num].extract_text()
                    start_index = text.find("Mã số tra cứu:")
                    if start_index != -1:
                        relevant_text = text[start_index + len("Mã số tra cứu"):].strip()
                        code_matches = re.findall(r'[A-Za-z0-9]+', relevant_text)
                        if code_matches:
                            last_code = code_matches[0]
                            if last_code.endswith('M'):
                                last_code = last_code[:-1]
                            codes.append(last_code)
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy tệp - {cyber_bill_constant.PATH_PDF_FILE}")
        except Exception as e:
            print(f"Có lỗi xảy ra: {e}")
        return codes

    def read_pdf(self):
        links = []
        try:
            with open(cyber_bill_constant.PATH_PDF_FILE, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    text = pdf_reader.pages[page_num].extract_text()
                    start_index = text.find("Tra cứu hóa đơn điện tử tại trang web:")
                    if start_index != -1:
                        relevant_text = text[start_index:]
                        link_matches = re.findall(
                            r'https?://(?:[a-zA-Z]|\d|[$-_@.&+]|[!*\\(),]|%[0-9a-fA-F][0-9a-fA-F])+', relevant_text)
                        links.extend(link_matches)
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy tệp - {cyber_bill_constant.PATH_PDF_FILE}")
        except Exception as e:
            print(f"Có lỗi xảy ra: {e}")
        return links


    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({cyber_bill_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(cyber_bill_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_portal())
        logging.info(f'{self.get_name()}: Open a website: {self.get_portal()}')
        time.sleep(cyber_bill_constant.DELAY_TIME_LOAD_PAGE)
        # Enter lookup code
        logging.info(f'{self.get_name()}: Entenr lookup code')
        wait = WebDriverWait(browser, 15)  # Đợi 10 giây
        input_id = wait.until(EC.visibility_of_element_located((By.NAME, cyber_bill_constant.INPUT_ID_BY_NAME)))
        input_id.send_keys(self.get_code_lookup())
        # Enter captcha
        util_rpa.enter_captcha(self.get_name(), browser, By.XPATH, By.XPATH,
                               cyber_bill_constant.CAPTCHA_IMG_BY_XPATH,
                               cyber_bill_constant.CAPTCHA_INPUT_BY_XPATH, By.XPATH,
                               cyber_bill_constant.BUTTON_SEARCH_BY_XPATH, By.CLASS_NAME,
                               cyber_bill_constant.ERROR_ALERT_BY_CLASS, cyber_bill_constant.RETRY_MAX,
                               cyber_bill_constant.DELAY_TIME_SKIP, check_num=True)
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
        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return cyber_bill_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': cyber_bill_constant.LATEST_VERSION,
            'info': cyber_bill_constant.VERSIONS[cyber_bill_constant.LATEST_VERSION]
        }


cyberbill_ins = CyberbillRpa(cyber_bill_constant.META_DATA)


if __name__ == '__main__':
    cyberbill_ins.extract_data()
    cyberbill_ins.reset()
