class Gas_PetrolimexConstant:
    FORM_BTN_BY_XPATH_TYPE = '//*[@id="btnTracuu"]'
    ID_INPUT_BY_ID_TYPE = 'tracuuID'
    CAPTCHA_LABEL_BY_ID_TYPE = 'mainCaptcha'
    CAPTCHA_INPUT_BY_ID_TYPE = 'txtInput'
    DOWNLOAD_BTN_BY_XPATH = '//*[@id="mainButton_wrapper"]/a[2]'
    DOWNLOAD_ZIP_BTN_BY_ID = 'btnDownload'
    URL = None
    CORE_NAME = 'GAS_PETROLIMEX'
    META_DATA = {
        'URL': URL,
        'RPA_NAME': CORE_NAME,
        'DRIVER_NAME': 'chrome'
    }
    VERSIONS = {
        'v1': {
            'URL': URL,
            'RPA_NAME': CORE_NAME,
        }
    }
    LATEST_VERSION = 'v1'
    DELAY_OPEN_MAXIMUM_BROWSER = 2
    DELAY_TIME_LOAD_PAGE = 5
    DELAY_TIME_SKIP = 5
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 5
    RETRY_MAX = 5


gas_petrolimex_constant = Gas_PetrolimexConstant()
