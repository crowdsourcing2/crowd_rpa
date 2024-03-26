class ExpressConstant:
    FILE_PATH = './RPA_TEMP/247express.pdf'
    URL_KEYWORD = 'Hóa Đơn Điện Tử tra cứu tại website :'
    CODE_BILL_KEYWORD = 'Mã nhận hóa đơn:'
    LAST_KEYWORD = 'Đơn vị cung cấp giải pháp hóa đơn điện tử:'

    TEXT_BOX_BY_XPATH = '//*[@id="search_LookupID"]'
    BTN_CLICK_BY_XPATH = '//*[@id="search"]/div[2]/div/div/div/button'
    BTN_DOWNLOAD_PDF_XML_BY_XPATH = '//*[@id="search"]/div[4]/div/div/div/button'
    BTN_ACCEPT_SUCCESS_BY_XPATH = '//*[@class="swal2-actions"]//button[1]'

    FORM_BY_ID_TYPE = 'Searchform'
    ID_INPUT_BY_ID_TYPE = 'ContentPlaceHolder1_txtCode'
    CAPTCHA_IMG_BY_XPATH = '//*[@id="ContentPlaceHolder1_Image1"]'
    CAPTCHA_INPUT_BY_XPATH = '//*[@id="ContentPlaceHolder1_txtCapcha"]'
    ERROR_ALERT_BY_XPATH = '//*[@id="tabError"]'
    VIEW_BTN_BY_XPATH = '//*[@class="table"]/tbody/tr/td[10]/a'
    DOWNLOAD_BTN_BY_NAME_TYPE = 'down'
    URL = None
    CORE_NAME = '247EXPRESS'
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
    DELAY_OPEN_MAXIMUM_BROWSER = 5
    DELAY_TIME_LOAD_PAGE = 5
    DELAY_TIME_SKIP = 8
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 8
    RETRY_MAX = 5


express_constant = ExpressConstant()
