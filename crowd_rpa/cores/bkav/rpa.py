
import time
import logging
from abc import ABC

import PyPDF2
import re
from driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.bkav.constant import bkav_constant
from selenium.common.exceptions import TimeoutException


class BkavRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return bkav_constant.META_DATA['RPA_NAME']

    def get_portal(self):
        urls = self.read_pdf()
        if urls:
            return urls[0]
        else:
            print("Khoong tim thay duong dan")
            return ""

    def get_code_lookup(self):
        code = self.read_look_code()
        return code

    def read_look_code(self):
        codes = []
        try:
            with open(bkav_constant.PATH_PDF_FILE, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    text = pdf_reader.pages[page_num].extract_text()
                    start_index = text.find("Mã tra cứu HĐĐT này:")
                    if start_index != -1:
                        # Cắt văn bản từ vị trí "Mã tra cứu HĐĐT này:" đến hết văn bản
                        relevant_text = text[start_index + len("Mã tra cứu HĐĐT này:"):].strip()
                        code_matches = re.findall(r'[A-Za-z0-9]+', relevant_text)
                        if code_matches:
                            last_code = code_matches[0]
                            if last_code.endswith('M'):
                                last_code = last_code[:-1]
                            codes.append(last_code)

        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy tệp - {bkav_constant.PATH_PDF_FILE}")
        except Exception as e:
            print(f"Có lỗi xảy ra: {e}")
        return codes

    def read_pdf(self):
        links = []
        try:
            with open(bkav_constant.PATH_PDF_FILE, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                for page_num in range(len(pdf_reader.pages)):
                    text = pdf_reader.pages[page_num].extract_text()
                    # Tìm vị trí của chuỗi "Hóa đơn Điện tử (HĐĐT)"
                    start_index = text.find("Hóa đơn Điện tử (HĐĐT)")

                    if start_index != -1:
                        # Cắt văn bản từ vị trí "Hóa đơn Điện tử (HĐĐT)" đến hết văn bản
                        relevant_text = text[start_index:]

                        # Sử dụng biểu thức chính quy để tìm các đường link
                        link_matches = re.findall(
                            r'https?://(?:[a-zA-Z]|\d|[$-_@.&+]|[!*\\(),]|%[0-9a-fA-F][0-9a-fA-F])+',
                            relevant_text)
                        cleaned_links = [link.rstrip('.') for link in link_matches]
                        links.extend(cleaned_links)

        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy tệp - {bkav_constant.PATH_PDF_FILE}")
        except Exception as e:
            print(f"Có lỗi xảy ra: {e}")
        return links

    def process_download_xml_pdf(self):

        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({bkav_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(bkav_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_portal())
        logging.info(f'{self.get_name()}: Open a website: {self.get_portal()}')
        time.sleep(bkav_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({bkav_constant.DELAY_TIME_LOAD_PAGE}s)')
        #Enter lookup code
        logging.info(f'{self.get_name()}: Enter lookup code')
        input_id = browser.find_element(By.CLASS_NAME, bkav_constant.INPUT_ID)
        input_id.send_keys(self.get_code_lookup())
        btn_search = browser.find_element(By.ID, bkav_constant.BUTTON_SEARCH_BY_ID)
        btn_search.click()
        time.sleep(bkav_constant.DELAY_TIME_LOAD_PAGE)
        try:
            iframe = browser.find_element(By.ID, bkav_constant.IFRAME_BY_ID)
            browser.get(iframe.get_attribute('src'))
            time.sleep(bkav_constant.DELAY_TIME_LOAD_PAGE)
            logging.info(f'{self.get_name()}: Please wait .. ({bkav_constant.DELAY_TIME_LOAD_PAGE}s)')
            # Chờ đến khi nút download hiển thị và có thể được click
            menu_download = browser.find_element(By.XPATH, bkav_constant.MENU_DOWNLOAD_BY_XPATH)
            browser.execute_script('arguments[0].style.setProperty("display", "block", "important")', menu_download)
            # Show menu
        except TimeoutException:
            logging.error("TimeoutException: Cannot find the download button within the specified time.")
        # Download PDF
        logging.info(f'{self.get_name()}: Download pdf')
        download_pdf = browser.find_element(By.XPATH, bkav_constant.DOWNLOAD_PDF_XPATH)
        download_pdf.click()
        logging.info(f'{self.get_name()}: Please wait .. ({bkav_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(bkav_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # Download XML
        logging.info(f'{self.get_name()}: Download XML')
        download_xml = browser.find_element(By.XPATH, bkav_constant.DOWNLOAD_XML_XPATH)
        download_xml.click()
        time.sleep(bkav_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return bkav_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': bkav_constant.LATEST_VERSION,
            'info': bkav_constant.VERSIONS[bkav_constant.LATEST_VERSION]
        }


if __name__ == '__main__':
    bkav_rpa_ins = BkavRpa(bkav_constant.META_DATA)
    bkav_rpa_ins.extract_data()
    bkav_rpa_ins.reset()




