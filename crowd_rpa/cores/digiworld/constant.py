class DigiWorldConstant:
    FILE_PATH = './RPA_TEMP/digiworld.pdf'
    URL_KEYWORD = 'Hóa Đơn Điện Tử tra cứu tại website :'
    CODE_BILL_KEYWORD = '- Mã nhận hóa đơn :'
    LAST_KEYWORD = 'Đơn vị cung cấp giải pháp hóa đơn điện tử:'

    FORM_BY_ID_TYPE = 'Searchform'
    ID_INPUT_BY_ID_TYPE = 'strFkey'
    CAPTCHA_IMG_BY_CLASS_TYPE = 'captcha_img'
    CAPTCHA_INPUT_BY_ID_TYPE = 'captch'
    ERROR_ALERT_BY_XPATH = '//*[@id="messagewrapper"]/div'
    VIEW_BTN_BY_XPATH = '//*[@class="table"]/tbody/tr/td[10]/a'
    DOWNLOAD_BTN_BY_NAME_TYPE = 'down'
    URL = None
    CORE_NAME = 'DIGIWORLD'
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


digi_world_constant = DigiWorldConstant()
