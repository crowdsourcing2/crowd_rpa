from os.path import join

from settings import cfg


class EasyInvoiceConstant:
    FORM_BY_ID_TYPE = 'Search'
    ID_INPUT_BY_ID_TYPE = 'iFkey'
    CAPTCHA_IMG_BY_ID_TYPE = 'captcha'
    CAPTCHA_INPUT_BY_ID_TYPE = 'Capcha'
    ERROR_ALERT_BY_CLASS_TYPE = 'showSweetAlert'
    CONFIRM_BTN_BY_CLASS_TYPE = 'sa-confirm-button-container'
    DOWNLOAD_PDF_XPATH = '//*[@id="invoice-footer"]/div/button[2]'
    DOWNLOAD_XML_XPATH = '//*[@id="invoice-footer"]/div/button[5]'
    URL = 'https://0401356807hd.easyinvoice.com.vn/'
    SETTING_SECURITY = 'chrome://settings/security'
    META_DATA = {
        'URL': URL,
        'RPA_NAME': 'CORES.EASYINVOICE.RPA',
        'DRIVER_NAME': 'chrome'
    }
    DELAY_OPEN_MAXIMUM_BROWSER = 0.2
    DELAY_TIME_LOAD_PAGE = 3
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 2
    DELAY_TIME_SKIP = 1
    RETRY_MAX = 5

easy_invoice_constant = EasyInvoiceConstant()
