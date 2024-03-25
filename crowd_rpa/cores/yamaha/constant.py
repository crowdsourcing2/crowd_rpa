class YamahaConstant:
    FORM_BY_ID_TYPE = 'Searchform'
    ID_INPUT_BY_ID_TYPE = 'strFkey'
    CAPTCHA_IMG_BY_CLASS_TYPE = 'captcha_img'
    CAPTCHA_INPUT_BY_ID_TYPE = 'captch'
    ERROR_ALERT_BY_XPATH = '//*[@id="messagewrapper"]/div'
    VIEW_BTN_BY_XPATH = '//*[@id="MainContent_tableView"]/div[2]/table/tbody/tr/td[9]/a'
    DOWNLOAD_PDF_BTN_BY_XPATH = '//*[@id="MainContent_tableView"]/div[2]/table/tbody/tr/td[10]/a'
    DOWNLOAD_XML_BTN_BY_XPATH =  '//*[@id="inbt"]/button[3]'
    URL = None
    CORE_NAME = 'YAMAHA'
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
    DELAY_OPEN_MAXIMUM_BROWSER = 1
    DELAY_TIME_LOAD_PAGE = 5
    DELAY_TIME_SKIP = 5
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 5
    RETRY_MAX = 5


yamaha_constant = YamahaConstant()
