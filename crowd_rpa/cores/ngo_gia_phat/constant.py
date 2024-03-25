class NgoGiaPhatConstant:
    FILE_PATH = './RPA_TEMP/ngo_gia_phat.pdf'
    LATEST_VERSION = 'v1'
    RETRY_MAX = 8
    DELAY_OPEN_MAXIMUM_BROWSER = 0.2
    DELAY_TIME_LOAD_PAGE = 3
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 2
    DELAY_TIME_SKIP = 1
    URL_KEYWORD = 'Quý khách hàng vui lòng tra cứu hóa đơn điện tử tại website:'
    CODE_BILL_KEYWORD = 'Mã tra cứu:'
    LAST_KEYWORD = 'STT'

    FORM_BY_ID_TYPE = 'ASPxButton_search_CD'
    IMG_CAPTCHA_BY_XPATH = '//*[@id="ASPxCaptcha_search_IMG"]'
    INPUT_SUBMIT_BY_XPATH = '//*[@id="ASPxButton_search_I"]'
    TEXT_BOX_BY_CLASS_TYPE = 'form-control'
    TEXT_BOX_CAPTCHA_BY_ID = 'ASPxCaptcha_search_TB_I'

    TEXT_BOX_BY_XPATH = '//*[@id="ASPxTextBox_search"]//input'
    TEXT_BOX_CAPTCHA_BY_XPATH = '//*[@id="ASPxCaptcha_search_TB_I"]'
    BUTTON_FIND_BILL_XPATH = '//*[@id="ASPxCaptcha_search_TB_I"]'
    BUTTON_DOWNLOAD_BY_XPATH = '//*[@id="ASPxPageControlSearch_ASPxFormLayoutListGTGT_ASPxButton_Download_CD"]'
    ERROR_ALERT_BY_XPATH = '/html/body/div[2]'

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


ngo_gia_phat_constant = NgoGiaPhatConstant()

