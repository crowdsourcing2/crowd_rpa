from os.path import join

from settings import cfg

class EvatConstant:
    FILE_PATH =  './RPA_TEMP/evat.pdf'
    URL_KEYWORD = 'tra cứu trực tuyến tại '
    LOOKUP_KEYWORD = ' , mã tra cứu: '
    COMPANY_KEYWORD = ' , mã công ty: '
    LAST_KEYWORD = '  )'

    DOWNLOAD_BTN_BY_CLASS_TYPE = "//body/div[1]/a[1]"
    DOWNLOAD_PDF_XPATH = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div'
    DOWNLOAD_XML_XPATH = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div[2]'
    URL = None
    CORE_NAME = 'CORES.EVAT.RPA'
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

evat_constant = EvatConstant()