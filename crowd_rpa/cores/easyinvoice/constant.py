from os.path import join

from settings import cfg


class EasyInvoiceConstant:
    FILE_PATH = './RPA_TEMP/easyinvoice.xml'
    URL_KEYWORD = 'PortalLink'  # tag name contains data
    # URL_KEYWORD = 'Trang tra cứu:'
    CODE_BILL_KEYWORD = 'Key'
    # CODE_BILL_KEYWORD = 'Mã tra cứu:'
    # LAST_KEYWORD = '(Cần kiểm tra, đối chiếu khi lập, giao, nhận hóa đơn)'

    FORM_BY_ID_TYPE = 'Search'
    ID_INPUT_BY_ID_TYPE = 'iFkey'
    CAPTCHA_IMG_BY_ID_TYPE = 'captcha'
    CAPTCHA_INPUT_BY_ID_TYPE = 'Capcha'
    ERROR_ALERT_BY_CLASS_TYPE = 'showSweetAlert'
    CONFIRM_BTN_BY_CLASS_TYPE = 'sa-confirm-button-container'
    DOWNLOAD_PDF_XPATH = '//*[@id="invoice-footer"]/div/button[2]'
    DOWNLOAD_XML_XPATH = '//*[@id="invoice-footer"]/div/button[5]'
    URL = None
    SETTING_SECURITY = 'chrome://settings/security'
    CORE_NAME = 'CORES.EASYINVOICE.RPA'
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
