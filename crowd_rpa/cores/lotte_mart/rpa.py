import time
import logging
from abc import ABC
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

    def process_download_xml_pdf(self):
        logging.info(f'{self.get_name()}: Start process download xml & pdf')

        browser = self.get_driver()
        browser.maximize_window()

        time.sleep(lottemart_constant.DELAY_OPEN_MAXIMUM_BROWSER)
        browser.get(lottemart_constant.META_DATA['URL'])

        text_box = browser.find_element(By.CLASS_NAME, lottemart_constant.TEXT_BOX_BY_CLASS_TYPE)
        text_box.send_keys(self.get_code_lookup())
        text_box_captcha = browser.find_element(By.ID, lottemart_constant.TEXT_BOX_CAPTCHA_BY_ID)
        text_box_captcha.send_keys(self.get_code_lookup())

        # captcha_img = browser.find_element(By.CLASS_NAME, 'captcha_img')
        # screenshot_png = captcha_img.screenshot_as_png
        # with open("captcha.png", "wb") as f:
        #     f.write(screenshot_png)

        # search_btn = browser.find_element(By.CLASS_NAME, lottemart_constant.SEARCH_BNT_BY_CLASS_TYPE)
        # search_btn.click()


        time.sleep(99)


if __name__ == '__main__':
    lotte_rpa_ins = LotteMartRpa(lottemart_constant.META_DATA)
    lotte_rpa_ins.extract_data()
    lotte_rpa_ins.reset()
