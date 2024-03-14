from os.path import join

from settings import cfg


class WininvoiceConstant:
    #ADD
    FILE_PATH = './RPA_TEMP/Wininvoice.pdf'
    # URL_KEYWORD = 'PortalLink'  # tag name contains data
    URL_KEYWORD = 'tra cứu trực tuyến tại'
    # CODE_BILL_KEYWORD = 'Fkey'
    CODE_BILL_KEYWORD = ' , mã tra cứu: '
    CITY_CODE_KEYWORD = ' , mã công ty: '
    LAST_KEYWORD = '  )'

    DOWNLOAD_BTN_BY_CLASS_TYPE = "//body/div[1]/a[1]"
    DOWNLOAD_PDF_XPATH = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div'
    DOWNLOAD_XML_XPATH = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div[2]'
    URL = None
    CORE_NAME = 'WININVOICE'
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
    DELAY_TIME_SKIP = 3


wininvoice_constant = WininvoiceConstant()
