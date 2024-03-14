from os.path import join

from settings import cfg


class VnptConstant:
    FILE_PATH = './RPA_TEMP/VNPT.pdf'
    # URL_KEYWORD = 'PortalLink'  # tag name contains data
    URL_KEYWORD = 'Tra cứ u hóa đơn tại website:'
    # CODE_BILL_KEYWORD = 'Fkey'
    CODE_BILL_KEYWORD = 'Mã tra cứu:'
    LAST_KEYWORD = 'Phí'

    FORM_BY_ID_TYPE = 'Searchform'
    ID_INPUT_BY_ID_TYPE = 'strFkey'
    CAPTCHA_IMG_BY_CLASS_TYPE = 'captcha_img'
    CAPTCHA_INPUT_BY_ID_TYPE = 'captch'
    ERROR_ALERT_BY_XPATH = '//*[@id="messagewrapper"]/div'
    VIEW_BTN_BY_XPATH = '//*[@class="table"]/tbody/tr/td[10]/a'
    DOWNLOAD_BTN_BY_NAME_TYPE = 'down'
    URL = None
    CORE_NAME = 'VNPT'
    META_DATA = {
        'URL': URL,
        'RPA_NAME': CORE_NAME,
        'DRIVER_NAME': 'chrome'

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
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 3
    DELAY_TIME_SKIP = 1
    RETRY_MAX = 5

vnpt_constant = VnptConstant()
