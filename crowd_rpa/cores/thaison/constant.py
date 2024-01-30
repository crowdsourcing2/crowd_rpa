from os.path import join

from settings import cfg


class ThaiSonConstant:
    MA_NHAN_HOA_DON_XPATH = '//*[@id="MA_NHAN_HOA_DON"]'
    CAPTCHA_TEXT_XPATH = '//*[@id="CaptchaInputText"]'
    CAPTCHA_IMG_XPATH = '//*[@id="CaptchaImage"]'
    ERROR_XPATH = '//*[@id="listresult"]'
    FIND_BTN_XPATH = '//*[@id="formgr"]/div/div[1]/div[1]/div/div/div/div[4]/div[2]/button'
    DOWNLOAD_ZIP_XPATH = '//*[@id="formgr"]/div/div/div[1]/div[1]/div/button[2]'
    URL = 'https://einvoice-fbvn.fujifilm.com'
    CORE_NAME = 'CORES.THAI_SON.RPA'
    MA_NHAN_HOA_DON = 'LWT6XPFZ3'
    META_DATA = {
        'URL': URL,
        'RPA_NAME': CORE_NAME,
        'DRIVER_NAME': 'chrome',
    }
    VERSIONS = {
        'v1': {
            'URL': URL,
            'RPA_NAME': CORE_NAME
        }
    }
    LATEST_VERSION = 'v1'
    DELAY_OPEN_MAXIMUM_BROWSER = 0.2
    DELAY_TIME_LOAD_PAGE = 3
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 2
    DELAY_TIME_SKIP = 1
    DELAY_TIME_CAPTCHA = 5
    RETRY_MAX = 8


thai_son_constant = ThaiSonConstant()
