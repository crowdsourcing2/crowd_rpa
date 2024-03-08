import fitz
from io import BytesIO
import logging
import time
import re

import cv2
import easyocr
import numpy as np
from PIL import Image
import xml.etree.ElementTree as ET


class UtilRpa:
    @staticmethod
    def read_pdf(path, first_str, last_str):
        try:
            doc = fitz.open(path)
            for page in doc:  # iterate the document pages
                text = page.get_text()  # get plain text encoded as UTF-8
                if first_str in text:
                    first_split = text.split(first_str)[1]
                    result = first_split.split(last_str)[0]
                    return result.strip()

            raise ValueError('Keyword not found in any page of the PDF.')

        except Exception as e:
            raise ValueError(f'An unexpected error occurred: {e}')

    @staticmethod
    def read_xml(path, keyword):
        try:
            tree = ET.parse(path)
            root = tree.getroot()

            # Find the PortalLink and Key elements
            result = root.find('.//' + keyword).text
            if result:
                return result

            raise ValueError('Keyword not found in XML')

        except ET.ParseError as parse_error:
            raise ValueError(f"Error parsing XML: {parse_error}")
        except Exception as unexpected_error:
            raise ValueError(f"An unexpected error occurred: {unexpected_error}")

    @staticmethod
    def enter_captcha(name, browser, captcha_find_by, input_result_captcha_by, captcha_image, input_result_captcha,
                      submit_find_by, value_submit, result_captcha_by, value_result_captcha, retry_max, delay_time_skip,
                      check_num=False, callback=None, callback_args=None, form_btn_handle="submit"):
        retry = 0
        while retry < retry_max:
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
                if check_num:
                    captcha_text = re.sub(r'\D', '', captcha_text)
            except Exception as e:
                logging.info(f'{name}: {e}')
            captcha_input = browser.find_element(input_result_captcha_by, input_result_captcha)
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)
            # Form submit
            logging.info(f'{name}: Form submit')
            time.sleep(1)
            form_btn = browser.find_element(submit_find_by, value_submit)
            if form_btn_handle.lower() == "submit":
                form_btn.submit()
            elif form_btn_handle.lower() == "click":
                form_btn.click()

            logging.info(f'{name}: Please wait .. ({delay_time_skip}s)')
            time.sleep(delay_time_skip)
            # Check error captcha
            try:
                browser.find_element(result_captcha_by, value_result_captcha)
                retry += 1
                if callback is not None:
                    callback(*callback_args)
            except Exception as e:
                break


util_rpa = UtilRpa()
