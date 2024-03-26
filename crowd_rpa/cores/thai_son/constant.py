class ThaiSonConstant:
    FILE_PATH = './RPA_TEMP/thaison.pdf'
    # URL_KEYWORD = 'PortalLink'  # tag name contains data
    URL_KEYWORD = 'Trang tra cứu (Website):'
    # CODE_BILL_KEYWORD = 'Key'
    CODE_BILL_KEYWORD = 'Mã tra cứu (Code):'
    LAST_KEYWORD = '(Cần kiểm tra, đối chiếu khi lập, giao nhận hóa đơn)'

    MA_NHAN_HOA_DON_ID = 'MA_NHAN_HOA_DON'
    CAPTCHA_TEXT_ID = 'CaptchaInputText'
    CAPTCHA_IMG_ID = 'CaptchaImage'
    ERROR_ID = 'listresult'
    FORM_BY_ID_TYPE = 'formgr'
    DOWNLOAD_ZIP_XPATH = '//*[@id="formgr"]/div/div/div[1]/div[1]/div/button[2]'
    URL = None
    CORE_NAME = 'THAI_SON'
    META_DATA = {
        'URL': URL,
        'RPA_NAME': CORE_NAME,
        'DRIVER_NAME': 'chrome',
    }
    VERSIONS = {
        'v1': {
            'URL': URL,
            'RPA_NAME': CORE_NAME
        }
    }
    LATEST_VERSION = 'v1'
    DELAY_OPEN_MAXIMUM_BROWSER = 1
    DELAY_TIME_LOAD_PAGE = 5
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 5
    DELAY_TIME_SKIP = 5
    RETRY_MAX = 8
    GROUP_PORTAL_EXTENSIONS = [[".thaison.vn", "einvoice-fbvn.fujifilm.com"]]


thai_son_constant = ThaiSonConstant()
