import re
import time
import cv2
import logging
import easyocr
import numpy as np
from abc import ABC
from PIL import Image
from io import BytesIO
from driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.easyinvoice.constant import easy_invoice_constant

class EasyInvoiceRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return easy_invoice_constant.META_DATA['RPA_NAME']

    def get_code_lookup(self):
        # TODO: you must be code here!
        return easy_invoice_constant.META_DATA['URL']

    def enter_captcha(self, browser):
        retry = 0
        while retry < easy_invoice_constant.RETRY_MAX:
            logging.info(f'{self.get_name()}: Enter captcha')
            captcha_img = browser.find_element(By.ID, easy_invoice_constant.CAPTCHA_IMG_BY_ID_TYPE)
            # Get the <img> tag's container
            img_location = captcha_img.location
            img_size = captcha_img.size
            # Get all photos of the website
            screenshot = browser.get_screenshot_as_png()
            # Use Pillow to crop and save the image according to the <img> tag's container
            image = Image.open(BytesIO(screenshot))
            cropped_image = image.crop((img_location['x'], img_location['y'], img_location['x'] + img_size['width'],
                                        img_location['y'] + img_size['height']))
            # Image to text
            captcha_text = ""
            try:
                # Blur captcha
                cropped_image_np = np.array(cropped_image)
                gray_image = cv2.cvtColor(cropped_image_np, cv2.COLOR_BGR2GRAY)
                blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
                # Read captcha
                reader = easyocr.Reader(['en'])
                cropped_image_np = np.array(blurred_image)
                results = reader.readtext(cropped_image_np)
                captcha_text = results[0][1]
                captcha_text = re.sub(r'[^0-9]', '', captcha_text)
            except Exception as e:
                logging.info(f'{self.get_name()}: {e}')
            captcha_input = browser.find_element(By.ID, easy_invoice_constant.CAPTCHA_INPUT_BY_ID_TYPE)
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)
            # Form submit
            logging.info(f'{self.get_name()}: Form submit')
            form = browser.find_element(By.ID, easy_invoice_constant.FORM_BY_ID_TYPE)
            form.submit()
            logging.info(f'{self.get_name()}: Please wait .. ({easy_invoice_constant.DELAY_TIME_SKIP}s)')
            time.sleep(easy_invoice_constant.DELAY_TIME_SKIP)
            # Check error captcha
            try:
                browser.find_element(By.CLASS_NAME, easy_invoice_constant.ERROR_ALERT_BY_CLASS_TYPE)
                confirm_btn = browser.find_element(By.CLASS_NAME, easy_invoice_constant.CONFIRM_BTN_BY_CLASS_TYPE)
                confirm_btn.click()
                retry += 1
            except Exception as e:
                break

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        # Thực hiện các thay đổi sau khi đã tạo đối tượng WebDriver
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({easy_invoice_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(easy_invoice_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        logging.info(f'{self.get_name()}: Open a website: {self.get_code_lookup()}')
        browser.get(self.get_code_lookup())
        time.sleep(easy_invoice_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({easy_invoice_constant.DELAY_TIME_LOAD_PAGE}s)')
        # Enter id
        logging.info(f'{self.get_name()}: Enter id')
        id_input = browser.find_element(By.ID, easy_invoice_constant.ID_INPUT_BY_ID_TYPE)
        id_input.send_keys(easy_invoice_constant.ID)
        # Enter captcha
        self.enter_captcha(browser)
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
