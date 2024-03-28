class HiloConstant:
    FILE_PATH = './RPA_TEMP/hilo.pdf'
    URL_KEYWORD = 'Hóa Đơn Điện Tử tra cứu tại website :'
    CODE_BILL_KEYWORD = 'Mã nhận hóa đơn:'
    LAST_KEYWORD = 'Đơn vị cung cấp giải pháp hóa đơn điện tử:'
    CIRCULARS_KEYWORD = 'Thông tư 32'

    BTN_EYE_BY_XPATH = '//*[@class="contentPage"]//td[8]//a'
    ELEMENT_EYE_BY_XPATH = '//*[@class="table-responsive"]//td[8]//a'

    TEXT_BOX_BY_XPATH = '//*[@id="key"]'
    SELECTOR_BY_XPATH = '//*[@id="TypeCirculars"]/option[2]'
    BTN_CLICK_BY_XPATH = '/html/body/div[2]/div[2]/div/div/div/form/div/div/div/div[4]/div/button'
    BTN_DOWNLOAD_XML_BY_XPATH = '//*[@id="invoice-footer"]/button[2]'
    BTN_DOWNLOAD_PDF_BY_XPATH = '//*[@id="ContentPlaceHolder1_viewReport"]/div[1]/div/div[1]/input[2]'
    TABLE_BY_XPATH = '//*[@class="table-responsive"]'
    BTN_ACCEPT_SUCCESS_BY_XPATH = '//*[@class="swal2-actions"]//button[1]'

    FORM_BY_ID_TYPE = 'Searchform'
    ID_INPUT_BY_ID_TYPE = 'ContentPlaceHolder1_txtCode'
    CAPTCHA_IMG_BY_XPATH = '//*[@id="CaptchaImage"]'
    CAPTCHA_INPUT_BY_XPATH = '//*[@id="CaptchaInputText"]'
    ERROR_ALERT_BY_XPATH = '//*[@class="table-responsive"]'
    VIEW_BTN_BY_XPATH = '/html/body/div[2]/div[2]/div/div/div/div/div/table/tbody/tr/td[8]/a/i'
    DOWNLOAD_BTN_BY_NAME_TYPE = 'down'
    URL_DOWNLOAD_PDF = 'https://evat.hilo.com.vn/Invoice/InvPreview/'
    URL = None
    CORE_NAME = 'HILO'
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
    RETRY_MAX = 8


hilo_constant = HiloConstant()