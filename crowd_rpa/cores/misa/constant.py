class MisaConstant:
    FILE_PATH = './RPA_TEMP/misa.pdf'
    URL_KEYWORD = 'Tra cứu tại Website (Search on Website):'
    CODE_BILL_KEYWORD = 'Mã tra cứu hóa đơn (Invoice code):'
    LAST_KEYWORD = 'Mã CQT: '

    DOWNLOAD_BTN_BY_CLASS_TYPE = 'download-invoice'
    DOWNLOAD_PDF_XPATH = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div'
    DOWNLOAD_XML_XPATH = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div[2]'
    URL = None
    CORE_NAME = 'MISA'
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
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 5
    DELAY_TIME_SKIP = 5


misa_constant = MisaConstant()
