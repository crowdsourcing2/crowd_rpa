class LotteMartConstant:
    IMG_CAPTCHA_BY_CLASS_TYPE = "img_captcha"
    SEARCH_BNT_BY_CLASS_TYPE = 'icon-search'
    TEXT_BOX_BY_CLASS_TYPE = 'form-control'
    TEXT_BOX_CAPTCHA_BY_ID = 'captch'
    ERROR_ALERT_BY_XPATH = '//*[@id="messagewrapper"]/div'
    DOWNLOAD_PDF_BY_XPATH = '//*[@class="table"]/tbody/tr/td[11]/a/i'
    VIEW_BTN_BY_XPATH = '//*[@class="table"]/tbody/tr/td[10]/a'
    DOWNLOAD_ZIP_BTN_BY_NAME_TYPE = 'down'
    CORE_NAME = 'CORES.LOTTEMART.RPA'
    URL = 'https://lottemart-bdg-tt78.vnpt-invoice.com.vn/HomeNoLogin/SearchByFkey'
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
    DELAY_OPEN_MAXIMUM_BROWSER = 0.2
    DELAY_TIME_LOAD_PAGE = 3
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 2
    DELAY_TIME_SKIP = 1


lottemart_constant = LotteMartConstant()
