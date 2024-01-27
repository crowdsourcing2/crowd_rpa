class LotteMartConstant:
    IMG_CAPTCHA_BY_CLASS_TYPE = "img_captcha"
    SEARCH_BNT_BY_CLASS_TYPE = 'icon-search'
    TEXT_BOX_BY_CLASS_TYPE = 'form-control'
    TEXT_BOX_CAPTCHA_BY_ID = 'captch'
    DOWNLOAD_PDF_BTN_BY_CLASS_TYPE = 'icon-download-alt'

    URL = 'https://lottemart-bdg-tt78.vnpt-invoice.com.vn/HomeNoLogin/SearchByFkey'
    META_DATA = {
        'URL': URL,
        'RPA_NAME': 'CORES.LOTTEMART.RPA',
        'DRIVER_NAME': 'chrome'
    }
    DELAY_OPEN_MAXIMUM_BROWSER = 0.2
    DELAY_TIME_LOAD_PAGE = 3
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 2
    DELAY_TIME_SKIP = 1


lottemart_constant = LotteMartConstant()
