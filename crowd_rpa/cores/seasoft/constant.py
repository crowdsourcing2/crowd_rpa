class SeaSoftConstant:
    FILE_PATH = './RPA_TEMP/Seasoft.pdf'
    URL_KEYWORD = 'Trang tra cứu:'
    CODE_BILL_KEYWORD = 'Mã tra cứu:'
    LAST_KEYWORD = 'Mã CQT: '
    INPUT_INVOICE_CODE_BY_ID = 'sohoadon'
    INPUT_LOOKUP_CODE_BY_ID = 'maxacnhan'
    INPUT_CAPTCHA_CODE_BY_ID = 'CaptchaInputText'
    CAPTCHA_IMG_BY_ID = 'CaptchaImage'
    BUTTON_SUBMIT_BY_XPATH = '//*[@id="page-content"]/div/div[1]/div/div/div/form/div/div/p/button'
    ERROR_ALERT_BY_XPATH ='//*[@id="page-content"]/div/div[1]/div/div/div/form/div/div/div[1]'
    ERROR_ALERT_BY_CLASS = 'alert-warning'
    DOWNLOAD_BTN_ZIP_BY_XPATH ='//*[@id="row_22370"]/td[14]/a/img'

    URL = None
    CORE_NAME = 'SeaSoft'
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
    DELAY_OPEN_MAXIMUM_BROWSER = 2
    DELAY_TIME_LOAD_PAGE = 5
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 5
    DELAY_TIME_SKIP = 5
    RETRY_MAX = 5


sea_soft_constant = SeaSoftConstant()
