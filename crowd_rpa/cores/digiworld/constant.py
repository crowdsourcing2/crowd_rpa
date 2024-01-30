from os.path import join

from settings import cfg


class DigiWorldConstant:
    FORM_BY_ID_TYPE = 'Searchform'
    ID_INPUT_BY_ID_TYPE = 'strFkey'
    CAPTCHA_IMG_BY_CLASS_TYPE = 'captcha_img'
    CAPTCHA_INPUT_BY_ID_TYPE = 'captch'
    ERROR_ALERT_BY_XPATH = '//*[@id="messagewrapper"]/div'
    VIEW_BTN_BY_XPATH = '//*[@class="table"]/tbody/tr/td[10]/a'
    DOWNLOAD_BTN_BY_NAME_TYPE = 'down'
    URL = 'https://hddt78.digiworld.com.vn'
    ID = '13231232184PD2B'
    CORE_NAME = 'CORES.DIGIWORLD.RPA'
    META_DATA = {
        'URL': URL,
        'RPA_NAME': CORE_NAME,
        'DRIVER_NAME': 'chrome'
    }
    VERSIONS = {
        'v1': {
            'URL': URL,
            'RPA_NAME': CORE_NAME,
        }
    }
    LATEST_VERSION = 'v1'
    DELAY_OPEN_MAXIMUM_BROWSER = 0.2
    DELAY_TIME_LOAD_PAGE = 3
    DELAY_TIME_SKIP = 1
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 2
    RETRY_MAX = 5

digi_world_constant = DigiWorldConstant()
