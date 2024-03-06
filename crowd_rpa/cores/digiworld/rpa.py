import logging
import re
import time
from abc import ABC
from io import BytesIO

import cv2
import easyocr
import numpy as np
from PIL import Image
from selenium.webdriver.common.by import By

from crowd_rpa.cores.digiworld.constant import digi_world_constant
from crowd_rpa.interfaces.rpa_interface import IRpa
from driver import WebDriver


class DigiWorldRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self):
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return digi_world_constant.META_DATA['RPA_NAME']

    def get_code_lookup(self):
        # TODO: you must be code here!
        return digi_world_constant.META_DATA['URL']

    @staticmethod
    def enter_captcha(name, browser, captcha_find_by, input_result_captcha_by, captcha_image, input_result_captcha,
                      submit_find_by, value_submit, result_captcha_by, value_result_captcha):
        retry = 0
        while retry < digi_world_constant.RETRY_MAX:
            logging.info(f'{name}: Enter captcha')
            captcha_img = browser.find_element(captcha_find_by, captcha_image)
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
                logging.info(f'{name}: {e}')
            captcha_input = browser.find_element(input_result_captcha_by, input_result_captcha)
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)
            # Form submit
            logging.info(f'{name}: Form submit')
            time.sleep(1)
            form = browser.find_element(submit_find_by, value_submit)
            form.submit()
            logging.info(f'{name}: Please wait .. ({digi_world_constant.DELAY_TIME_SKIP}s)')
            time.sleep(digi_world_constant.DELAY_TIME_SKIP)
            # Check error captcha
            try:
                browser.find_element(result_captcha_by, value_result_captcha)
                retry += 1
            except Exception as e:
                break

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')
        # Maximize the browser window to full screen
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({digi_world_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(digi_world_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_code_lookup())
        logging.info(f'{self.get_name()}: Open a website: {self.get_code_lookup()}')
        time.sleep(digi_world_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({digi_world_constant.DELAY_TIME_LOAD_PAGE}s)')
        # Enter id
        id_input = browser.find_element(By.ID, digi_world_constant.ID_INPUT_BY_ID_TYPE)
        id_input.send_keys(digi_world_constant.ID)
        logging.info(f'{self.get_name()}: Enter id')
        # Enter captcha
        self.enter_captcha(self.get_name(), browser, By.CLASS_NAME, By.ID,
                           digi_world_constant.CAPTCHA_IMG_BY_CLASS_TYPE, digi_world_constant.CAPTCHA_INPUT_BY_ID_TYPE,
                           By.ID, digi_world_constant.FORM_BY_ID_TYPE, By.XPATH,
                           digi_world_constant.ERROR_ALERT_BY_XPATH)
        # Open view detail
        logging.info(f'{self.get_name()}: Open view detail')
        view_btn = browser.find_element(By.XPATH, digi_world_constant.VIEW_BTN_BY_XPATH)
        view_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({digi_world_constant.DELAY_TIME_SKIP}s)')
        time.sleep(digi_world_constant.DELAY_TIME_SKIP)
        # Download file pdf and xml
        logging.info(f'{self.get_name()}: Download pdf and xml')
        download_btn = browser.find_element(By.NAME, digi_world_constant.DOWNLOAD_BTN_BY_NAME_TYPE)
        download_btn.click()
        logging.info(f'{self.get_name()}: Please wait .. ({digi_world_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE}s)')
        time.sleep(digi_world_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
        # Close rpa
        browser.quit()
        logging.info(f'{self.get_name()}: Finished process download xml & pdf')

    def versions(self) -> dict:
        return digi_world_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': digi_world_constant.LATEST_VERSION,
            'info': digi_world_constant.VERSIONS[digi_world_constant.LATEST_VERSION]
        }


if __name__ == '__main__':
    digi_world_rpa_ins = DigiWorldRpa(digi_world_constant.META_DATA)
    digi_world_rpa_ins.extract_data()
    digi_world_rpa_ins.reset()