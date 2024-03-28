class TheGioiDiDongConstant:
    ID_INPUT_BY_ID = 'billNum'
    COMPANY_INPUT_BY_ID = 'phone'
    CAPTCHA_INPUT_BY_ID = 'Captcha'
    CAPTCHA_IMG_BY_XPATH = '//*[@id="frmSearchInvoice"]/div[1]/div[3]/div/div/div[2]/img'
    ERROR_BY_XPATH = '/html/body/section/aside/div[2]/table/tbody/tr[2]/td[7]/a[3]'
    FORM_BY_ID_TYPE = 'frmSearchInvoice'
    RELOAD_CAPTCHA_BY_XPATH = '//*[@id="frmSearchInvoice"]/div[1]/div[3]/div/div/div[1]/a'
    DOWNLOAD_XML_XPATH = '/html/body/section/aside/div[2]/table/tbody/tr[2]/td[7]/a[3]'

    URL = None
    CORE_NAME = 'THE_GIOI_DI_DONG'
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
    DELAY_OPEN_MAXIMUM_BROWSER = 2
    DELAY_TIME_LOAD_PAGE = 5
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 5
    DELAY_TIME_SKIP = 5
    RETRY_MAX = 8
    GROUP_PORTAL_EXTENSIONS = [["hddt.tantamphucvu.vn", ".nhathuocankhang.com"]]


the_gioi_di_dong_constant = TheGioiDiDongConstant()
