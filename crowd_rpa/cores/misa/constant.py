from os.path import join

from settings import cfg


class MisaConstant:

    DOWNLOAD_BTN_BY_CLASS_TYPE = 'download-invoice'
    DOWNLOAD_PDF_XPATH = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div'
    DOWNLOAD_XML_XPATH = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div[2]'
    URL = 'https://www.meinvoice.vn/tra-cuu/?sc='
    META_DATA = {
        'URL': URL,
        'RPA_NAME': 'CORES.MISA.RPA',
        'DRIVER_NAME': 'chrome'

    }
    DELAY_OPEN_MAXIMUM_BROWSER = 0.2
    DELAY_TIME_LOAD_PAGE = 3
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 2
    DELAY_TIME_SKIP = 1


misa_constant = MisaConstant()
