class BkavConstant:
    IFRAME_BY_ID = 'frameViewInvoice'
    PATH_PDF_FILE ='./RPA_TEMP/BKAV.pdf'
    INPUT_ID ='form-control'
    BUTTON_SEARCH_BY_ID = 'Button1'
    MENU_DOWNLOAD_BY_XPATH = '//*[@id="divDownloads"]/ul'
    DOWNLOAD_PDF_XPATH = '//*[@id="LinkDownPDF"]'
    DOWNLOAD_XML_XPATH = '//*[@id="LinkDownXML"]'
    URL = None
    CORE_NAME = 'BKAV'
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
    DELAY_OPEN_MAXIMUM_BROWSER = 2
    DELAY_TIME_LOAD_PAGE = 5
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 5
    DELAY_TIME_SKIP = 5


bkav_constant = BkavConstant()
