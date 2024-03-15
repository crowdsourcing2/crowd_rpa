class EasyInvoiceConstant:
    FILE_PATH = './RPA_TEMP/easyinvoice.xml'
    URL_KEYWORD = 'PortalLink'  # tag name contains data
    CODE_BILL_KEYWORD = 'Key'

    FORM_BY_ID_TYPE = 'Search'
    ID_INPUT_BY_ID_TYPE = 'iFkey'
    CAPTCHA_IMG_BY_ID_TYPE = 'captcha'
    CAPTCHA_INPUT_BY_ID_TYPE = 'Capcha'
    ERROR_ALERT_BY_CLASS_TYPE = 'showSweetAlert'
    CONFIRM_BTN_BY_CLASS_TYPE = 'sa-confirm-button-container'
    DOWNLOAD_PDF_XPATH = '/html/body/div[2]/div/div/div[2]/div/button[2]'
    DOWNLOAD_XML_XPATH = '/html/body/div[2]/div/div/div[2]/div/button[5]'

    URL = None
    SETTING_SECURITY = 'chrome://settings/security'
    CORE_NAME = 'EASYINVOICE'
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
    DELAY_OPEN_MAXIMUM_BROWSER = 0.2
    DELAY_TIME_LOAD_PAGE = 3
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 2
    DELAY_TIME_SKIP = 1
    RETRY_MAX = 5


easy_invoice_constant = EasyInvoiceConstant()
