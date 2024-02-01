import os
import pathlib
import time
import logging
from abc import ABC
from driver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from crowd_rpa.interfaces.rpa_interface import IRpa
from crowd_rpa.cores.Vnpt.constant import vnpt_constant
import easyocr
import cv2
import re
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WininvoiceRpa(IRpa, ABC):
    def __init__(self, meta_data):
        super().__init__(meta_data)

    def extract_data(self):
        logging.info(f'{self.get_name()}: Start extracting data')
        self.process_download_xml_pdf()

    def get_driver(self):
        return WebDriver(tag=self.driver_name)()

    def get_name(self):
        return vnpt_constant.META_DATA['RPA_NAME']

    def get_code_lookup(self):
        return vnpt_constant.META_DATA['URL']

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')

        # Function to handle captcha input
        def handle_captcha_input(browser):
            nhaplieu = browser.find_element(By.NAME, "strFkey")
            nhaplieu.send_keys("009FA9BFCB2380469487DB4D7A54EE51FB")
            time.sleep(vnpt_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
            # Capture screenshot of the captcha
            capcha = browser.find_element(By.NAME, "captch")
            time.sleep(1)
            browser.get_screenshot_as_file("captcha.png")
            imgCv2 = cv2.imread('captcha.png')
            # Apply image processing to enhance contrast and visibility
            img_gray = cv2.cvtColor(imgCv2, cv2.COLOR_BGR2GRAY)
            img_equ = cv2.equalizeHist(img_gray)

            # Áp dụng kỹ thuật ngưỡng để chuyển đổi ảnh thành ảnh nhị phân, giúp làm nổi bật các đặc trưng của ảnh.
            _, img_thresh = cv2.threshold(img_equ, 128, 255, cv2.THRESH_BINARY)
            imgCrop = imgCv2[365:395, 490:570]
            cropped_image_np = np.array(imgCrop)
            gray_image = cv2.cvtColor(cropped_image_np, cv2.COLOR_BGR2GRAY)
            blurred_image = cv2.GaussianBlur(gray_image, (1, 1), 1)
            unsharp_mask = cv2.addWeighted(gray_image, 11, blurred_image, -10, 0)
            blurred_image = cv2.GaussianBlur(unsharp_mask, (5, 5), 0)
            # Read captcha
            reader = easyocr.Reader(['en'])
            result = reader.readtext(blurred_image)

            if result:
                text = result[0][-2]
                # Extract only numbers from the detected text
                numbers_only = ''.join(filter(str.isdigit, text))
                # Ensure the extracted numbers contain exactly 4 digits
                if len(numbers_only) == 4:
                    capcha.send_keys(numbers_only)
                    time.sleep(vnpt_constant.DELAY_TIME_LOAD_CAPTCHA)
                    logging.info(f"{self.get_name()}: Detected captcha text: {numbers_only}")
                else:
                    logging.error(f"{self.get_name()}: Invalid captcha format.")
            else:
                logging.error(f"{self.get_name()}: No text detected in the captcha image.")

        # Maximize the browser window to full screen
        browser = self.get_driver()
        browser.maximize_window()
        logging.info(f'{self.get_name()}: Please wait .. ({vnpt_constant.DELAY_OPEN_MAXIMUM_BROWSER}s)')
        time.sleep(vnpt_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        # Open a website
        browser.get(self.get_code_lookup())
        logging.info(f'{self.get_name()}: Open a website: {self.get_code_lookup()}')
        time.sleep(vnpt_constant.DELAY_TIME_LOAD_PAGE)
        logging.info(f'{self.get_name()}: Please wait .. ({vnpt_constant.DELAY_TIME_LOAD_PAGE}s)')

        max_attempts = 5
        attempt_count = 0
        success = False  # Thêm một biến kiểm soát

        while attempt_count < max_attempts:
            # Process Captcha
            handle_captcha_input(browser)  # Pass the browser instance

            # Try to find and click the submit button
            form_submit = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "Searchform"))
            )
            form_submit.submit()

            try:
                link_element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@title, 'Tải file pdf')]"))
                )
                link_element.click()
                success = True
                break
            except Exception as e:
                attempt_count += 1
                logging.warning(f"{self.get_name()}: Attempt {attempt_count} failed. Retrying...")

        # Kiểm tra nếu thành công thì thực hiện các bước tiếp theo
        if success:
            link_element = browser.find_element(By.XPATH, "//a[contains(@title, 'Tải file pdf')]")
            link_element.click()
            time.sleep(vnpt_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
            logging.info(f"{self.get_name()}: Clicked on the 'Tải file pdf' link.")

            view_link = browser.find_element(By.XPATH, "//td[@class='text-center']/a[@title='Xem']")
            view_link.click()
            time.sleep(vnpt_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
            logging.info(f"{self.get_name()}: Clicked on the 'Xem' link.")

            download_button = browser.find_element(By.XPATH,"//button[@onclick=\"downloadZip('E11ix13GqCAToOpGHidEqI/OddSZrj5i6SlhH1+JY0s=');\"]")
            download_button.click()
            time.sleep(vnpt_constant.DELAY_CLICK_DOWNLOAD_EVERY_FILE)
            logging.info(f"{self.get_name()}: Clicked on the 'Tải hóa đơn Zip' button.")
            pass
        browser.quit()
        logging.info(f'{self.get_name()}: Process completed successfully.')

    def versions(self) -> dict:
        return vnpt_constant.VERSIONS

    def get_latest_version(self) -> dict:
        return {
            'version': vnpt_constant.LATEST_VERSION,
            'info': vnpt_constant.VERSIONS[vnpt_constant.LATEST_VERSION]
        }
if __name__ == '__main__':
    vnpt_rpa_ins = WininvoiceRpa(vnpt_constant.META_DATA)
    vnpt_rpa_ins.extract_data()
    vnpt_rpa_ins.reset()
