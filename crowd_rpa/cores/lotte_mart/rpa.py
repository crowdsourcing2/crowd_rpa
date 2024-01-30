import cv2
import time
import logging
import easyocr

import numpy as np
from abc import ABC
from PIL import Image
from io import BytesIO
from driver import WebDriver
from selenium.webdriver.common.by import By

from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.lotte_mart.constant import lottemart_constant


class LotteMartRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return lottemart_constant.META_DATA['RPA_NAME']

    def get_code_lookup(self):
        # TODO: you must be code here!
        return '01005_20231103_18'

    def bypass_captcha2(self, browser):
        retry = 0
        while retry < lottemart_constant.RETRY_MAX:
            logging.info(f'{self.get_name()}: Enter captcha')
            captcha_img = browser.find_element(By.CLASS_NAME, 'captcha_img')
            # Get the <img> tag's container
            img_location = captcha_img.location
            img_size = captcha_img.size
            # Get all photos of the website
            screenshot = browser.get_screenshot_as_png()
            # Use Pillow to crop and save the image according to the <img> tag's container
            image = Image.open(BytesIO(screenshot))
            cropped_image_captcha = image.crop((img_location['x'], img_location['y'], img_location['x'] + img_size['width'],
                                        img_location['y'] + img_size['height']))
            # Image to text
            captcha_text = ""
            try:
                cropped_image_captcha_np = np.array(cropped_image_captcha)
                gray_image = cv2.cvtColor(cropped_image_captcha_np, cv2.COLOR_BGR2GRAY)
                blurred_image = cv2.GaussianBlur(gray_image, (1, 1), 1)
                unsharp_mask = cv2.addWeighted(gray_image, 11, blurred_image, -10, 0)
                blurred_image = cv2.GaussianBlur(unsharp_mask, (5, 5), 0)
                reader = easyocr.Reader(['en'])
                results = reader.readtext(blurred_image)
                captcha_text = results[0][1]
            except Exception as e:
                logging.info(f'{self.get_name()}: {e}')
            text_box_captcha = browser.find_element(By.ID, lottemart_constant.TEXT_BOX_CAPTCHA_BY_ID)
            text_box_captcha.clear()
            text_box_captcha.send_keys(captcha_text)
            # Form submit
            logging.info(f'{self.get_name()}: Form submit')
            form = browser.find_element(By.ID, 'Searchform')
            form.submit()
            logging.info(f'{self.get_name()}: Please wait .. ({lottemart_constant.DELAY_TIME_SKIP}s)')
            time.sleep(lottemart_constant.DELAY_TIME_SKIP)
            # Check error captcha
            try:
                browser.find_element(By.XPATH, lottemart_constant.ERROR_ALERT_BY_XPATH)
                retry += 1
            except Exception as e:
                break

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({lottemart_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(lottemart_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        logging.info(f'{self.get_name()}: Open a website: {lottemart_constant.URL}')
        browser.get(lottemart_constant.META_DATA['URL'])
        logging.info(f'{self.get_name()}: Please wait .. ({lottemart_constant.DELAY_TIME_LOAD_PAGE}s)')
        time.sleep(lottemart_constant.DELAY_TIME_LOAD_PAGE)

        text_box = browser.find_element(By.CLASS_NAME, lottemart_constant.TEXT_BOX_BY_CLASS_TYPE)
        text_box.send_keys(self.get_code_lookup())
        logging.info(f'{self.get_name()}: Enter code lookup: {self.get_code_lookup()}')
        self.bypass_captcha2(browser)

        logging.info(f'{self.get_name()}: Download pdf')
        pdf_download = browser.find_element(By.XPATH, lottemart_constant.DOWNLOAD_PDF_BY_XPATH)
        pdf_download.click()
        logging.info(f'{self.get_name()}: Please wait .. ({lottemart_constant.DELAY_TIME_SKIP}s)')
        time.sleep(lottemart_constant.DELAY_TIME_SKIP)
        logging.info(f'{self.get_name()}: Open view detail')
        view_btn = browser.find_element(By.XPATH, lottemart_constant.VIEW_BTN_BY_XPATH)
        view_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({lottemart_constant.DELAY_TIME_SKIP}s)')
        time.sleep(lottemart_constant.DELAY_TIME_SKIP)

        logging.info(f'{self.get_name()}: Download file Zip xml')
        download_btn = browser.find_element(By.NAME, lottemart_constant.DOWNLOAD_ZIP_BTN_BY_NAME_TYPE)
        download_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({lottemart_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(lottemart_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return lottemart_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': lottemart_constant.LATEST_VERSION,
            'info': lottemart_constant.VERSIONS[lottemart_constant.LATEST_VERSION]
        }


if __name__ == '__main__':
    lotte_rpa_ins = LotteMartRpa(lottemart_constant.META_DATA)
    lotte_rpa_ins.extract_data()
    lotte_rpa_ins.reset()
