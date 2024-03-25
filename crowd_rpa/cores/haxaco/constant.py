class HaxacoConstant:
    FILE_PATH = './RPA_TEMP/haxaco.pdf'
    LATEST_VERSION = 'v1'
    RETRY_MAX = 8
    DELAY_OPEN_MAXIMUM_BROWSER = 3
    DELAY_TIME_LOAD_PAGE = 5
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 5
    DELAY_TIME_SKIP = 5
    URL_KEYWORD = 'Quý khách hàng vui lòng tra cứu hóa đơn điện tử tại website:'
    CODE_BILL_KEYWORD = 'Mã tra cứu:'
    LAST_KEYWORD = 'STT'

    FORM_BY_ID_TYPE = 'ASPxButton_search_CD'
    IMG_CAPTCHA_BY_XPATH = '//*[@id="CaptchaImage"]'
    BUTTON_SUBMIT_CAPCHA_BY_XPATH = '//*[@class="contentPage"]//button'
    TEXT_BOX_BY_CLASS_TYPE = 'form-control'
    TEXT_BOX_CAPTCHA_BY_ID = 'ASPxCaptcha_search_TB_I'

    TEXT_BOX_BY_ID = 'code'
    TEXT_BOX_CAPTCHA_BY_XPATH = '//*[@id="CaptchaInputText"]'
    BUTTON_FIND_BILL_XPATH = '//*[@id="ASPxCaptcha_search_TB_I"]'
    BUTTON_DOWNLOAD_BY_XPATH = '//*[@class="contentPage"]//td[9]/a'
    ERROR_ALERT_BY_XPATH = ''

    DOWNLOAD_PDF_BY_XPATH = '//*[@class="table"]/tbody/tr/td[11]/a/i'
    VIEW_BTN_BY_XPATH = '//*[@class="table"]/tbody/tr/td[10]/a'

    DOWNLOAD_ZIP_BTN_BY_NAME_TYPE = 'down'
    CORE_NAME = 'HAXACO'
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


haxaco_constant = HaxacoConstant()

