import re
import cv2
import time
import easyocr
import logging
import numpy as np
from abc import ABC
from PIL import Image
from io import BytesIO
from driver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.cyberbill.constant import cyberbill_constant


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

    def enter_captcha(self, browser):
        retry = 0
        while retry < cyberbill_constant.RETRY_MAX:
            logging.info(f'{self.get_name()}: Enter captcha')
            captcha_img = browser.find_element(By.XPATH, cyberbill_constant.CAPTCHA_IMG_BY_XPATH)
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
                blurred_image = cv2.GaussianBlur(gray_image, (1, 1), 1)
                unsharp_mask = cv2.addWeighted(gray_image, 11, blurred_image, -10, 0)
                blurred_image = cv2.GaussianBlur(unsharp_mask, (5, 5), 0)
                # Read captcha
                reader = easyocr.Reader(['en'])
                results = reader.readtext(blurred_image)
                captcha_text = results[0][1]
                captcha_text = re.sub(r'[^0-9]', '', captcha_text)

            except Exception as e:
                logging.info(f'{self.get_name()}: {e}')
            captcha_input = browser.find_element(By.XPATH, cyberbill_constant.CAPTCHA_INPUT_BY_XPATH)
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)
            # Form submit
            logging.info(f'{self.get_name()}: Form submit')
            time.sleep(cyberbill_constant.DELAY_TIME_SKIP)
            btnSearch = browser.find_element(By.XPATH, cyberbill_constant.BUTTON_SEARCH_BY_XPATH)
            btnSearch.submit()
            logging.info(f'{self.get_name()}: Please wait .. ({cyberbill_constant.DELAY_TIME_SKIP}s)')
            time.sleep(cyberbill_constant.DELAY_TIME_SKIP)
            # Check error captcha
            try:
                browser.find_element(By.CLASS_NAME, cyberbill_constant.ERROR_ALERT_BY_CLASS)
                retry += 1
            except Exception as e:
                break

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
        #Enter lookup code
        logging.info(f'{self.get_name()}: Entenr lookup code')
        wait = WebDriverWait(browser, 15)  # Đợi 10 giây
        input_id = wait.until(EC.visibility_of_element_located((By.NAME, cyberbill_constant.INPUT_ID_BY_NAME)))
        input_id.send_keys("2E2EYBV8S3AG")
        # Enter captcha
        self.enter_captcha(browser)
        time.sleep(cyberbill_constant.DELAY_TIME_SKIP)
        logging.info(f'{self.get_name()}: Download XML')
        download_xml = browser.find_element(By.XPATH, cyberbill_constant.DOWNLOAD_XML_XPATH)
        download_xml.click()
        logging.info(f'{self.get_name()}: Please wait .. ({cyberbill_constant.DELAY_TIME_SKIP}s)')
        time.sleep(cyberbill_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        logging.info(f'{self.get_name()}: Download PDF')
        download_pdf = browser.find_element(By.XPATH, cyberbill_constant.DOWNLOAD_PDF_XPATH)
        download_pdf.click()
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

