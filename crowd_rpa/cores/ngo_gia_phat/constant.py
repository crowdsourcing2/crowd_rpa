class NgoGiaPhatConstant:
    FILE_PATH = './RPA_TEMP/ngo_gia_phat.pdf'
    URL_KEYWORD = 'Quý khách hàng vui lòng tra cứu hóa đơn điện tử tại website:'
    CODE_BILL_KEYWORD = 'Mã tra cứu:'
    LAST_KEYWORD = 'STT'

    FORM_ENTER_BY_XPATH = '//*[@id="ASPxButton_search"]'
    IMG_CAPTCHA_BY_XPATH = '//*[@id="ASPxCaptcha_search_IMG"]'

    TEXT_BOX_BY_CLASS_TYPE = 'form-control'
    TEXT_BOX_CAPTCHA_BY_ID = 'ASPxCaptcha_search_TB_I'

    INPUT_BY_XPATH_ID = '//*[@id="ASPxTextBox_search"]//input'
    INPUT_CAPTCHA_BY_XPATH = '//*[@id="ASPxCaptcha_search_TB_I"]'
    TEXT_BOX_CAPTCHA_BY_XPATH = '//*[@id="ASPxCaptcha_search_TB_I"]'
    BUTTON_DOWNLOAD_BY_XPATH = '//*[@id="ASPxPageControlSearch_ASPxFormLayoutListGTGT_ASPxButton_Download_CD"]//span'
    ERROR_ALERT_BY_XPATH = '/html/body/div[2]/button'
    DOWNLOAD_PDF_BY_XPATH = '//*[@class="table"]/tbody/tr/td[11]/a/i'
    VIEW_BTN_BY_XPATH = '//*[@class="table"]/tbody/tr/td[10]/a'

    DOWNLOAD_ZIP_BTN_BY_NAME_TYPE = 'down'
    CORE_NAME = 'NGOGIAPHAT'
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


ngo_gia_phat_constant = NgoGiaPhatConstant()

