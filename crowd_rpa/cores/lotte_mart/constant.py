class LotteMartConstant:
    FILE_PATH = './RPA_TEMP/lottemart.pdf'
    # URL_KEYWORD = 'PortalLink'  # tag name contains data
    URL_KEYWORD = 'Quý khách hàng vui lòng tra cứu hóa đơn điện tử tại website:'
    # CODE_BILL_KEYWORD = 'Key'
    CODE_BILL_KEYWORD = 'Mã tra cứu:'
    LAST_KEYWORD = 'STT'

    FORM_BY_ID_TYPE = 'Searchform'
    IMG_CAPTCHA_BY_CLASS_TYPE = "captcha_img"
    TEXT_BOX_BY_CLASS_TYPE = 'form-control'
    TEXT_BOX_CAPTCHA_BY_ID = 'captch'
    ERROR_ALERT_BY_XPATH = '//*[@id="messagewrapper"]/div'
    DOWNLOAD_PDF_BY_XPATH = '//*[@class="table"]/tbody/tr/td[11]/a/i'
    VIEW_BTN_BY_XPATH = '//*[@class="table"]/tbody/tr/td[10]/a'
    DOWNLOAD_ZIP_BTN_BY_NAME_TYPE = 'down'
    CORE_NAME = 'LOTTEMART'
    URL = None
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
    RETRY_MAX = 8
    DELAY_OPEN_MAXIMUM_BROWSER = 2
    DELAY_TIME_LOAD_PAGE = 5
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 5
    DELAY_TIME_SKIP = 5


lottemart_constant = LotteMartConstant()
