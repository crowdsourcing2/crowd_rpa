import os
import pathlib
import time
import logging
from abc import ABC
from io import BytesIO

import re
import easyocr
import cv2
import numpy as np
from PIL import Image

from driver import WebDriver
from selenium.webdriver.common.by import By
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.thaison.constant import thai_son_constant


class ThaiSonRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return thai_son_constant.META_DATA['RPA_NAME']

    def get_code_lookup(self):
        # TODO: you must be code here!
        return thai_son_constant.META_DATA['URL']

    def enter_captcha(self, browser):
        retry = 0
        while retry < thai_son_constant.RETRY_MAX:
            logging.info(f'{self.get_name()}: Please wait .. ({thai_son_constant.DELAY_TIME_LOAD_PAGE}s)')
            mst_text = browser.find_element(By.XPATH, thai_son_constant.MA_NHAN_HOA_DON_XPATH)
            mst_text.send_keys(thai_son_constant.MA_NHAN_HOA_DON)
            logging.info(f'{self.get_name()}: Enter captcha')
            captcha_img = browser.find_element(By.XPATH, thai_son_constant.CAPTCHA_IMG_XPATH)
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
                # Read captcha
                reader = easyocr.Reader(['en'])
                cropped_image_np = np.array(gray_image)
                results = reader.readtext(cropped_image_np)
                captcha_text = results[0][1]
            except Exception as e:
                logging.info(f'{self.get_name()}: {e}')
            captcha_input = browser.find_element(By.XPATH, thai_son_constant.CAPTCHA_TEXT_XPATH)
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)
            # Click FIND
            logging.info(f'{self.get_name()}: Click Find')
            browser.find_element(By.XPATH, thai_son_constant.FIND_BTN_XPATH).click()
            logging.info(f'{self.get_name()}: Please wait .. ({thai_son_constant.DELAY_TIME_SKIP}s)')
            time.sleep(thai_son_constant.DELAY_TIME_SKIP)
            # Check error captcha
            try:
                browser.find_element(By.XPATH, thai_son_constant.ERROR_XPATH)
                retry += 1
            except Exception as e:
                break

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({thai_son_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(thai_son_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_code_lookup())
        logging.info(f'{self.get_name()}: Open a website: {self.get_code_lookup()}')
        time.sleep(thai_son_constant.DELAY_TIME_LOAD_PAGE)
        #ClearCaptCha
        self.enter_captcha(browser)
        # Download file zip
        logging.info(f'{self.get_name()}: Download Zip')
        download_zip = browser.find_element(By.XPATH, thai_son_constant.DOWNLOAD_ZIP_XPATH)
        download_zip.click()
        logging.info(f'{self.get_name()}: Please wait .. ({thai_son_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(thai_son_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return thai_son_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': thai_son_constant.LATEST_VERSION,
            'info': thai_son_constant.VERSIONS[thai_son_constant.LATEST_VERSION]
        }


if __name__ == '__main__':
    misa_rpa_ins = ThaiSonRpa(thai_son_constant.META_DATA)
    misa_rpa_ins.extract_data()
    misa_rpa_ins.reset()
