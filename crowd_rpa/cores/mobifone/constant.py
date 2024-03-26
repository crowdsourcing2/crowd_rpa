class MobifoneConstant:
    FILE_PATH = './RPA_TEMP/Mobifone.pdf'
    URL_KEYWORD = 'Mã nhận hóa đơn: 41N4GCGP8 tra cứu tại: '
    CODE_BILL_KEYWORD = '(Cần kiểm tra, đối chiếu khi lập, giao nhận hóa đơn)'
    LAST_KEYWORD = ' tra cứu tại: http://invoice.mobifone.vn'

    RELOAD_BTN_BY_ID_TYPE = 'reload-button'
    FORM_BTN_BY_XPATH_TYPE = '//*[@id="formgr"]/div/div[1]/div/div/div/div/div[4]/div[2]/button'
    ID_INPUT_BY_ID_TYPE = 'MA_NHAN_HOA_DON'
    CAPTCHA_IMG_BY_ID_TYPE = 'CaptchaImage'
    CAPTCHA_INPUT_BY_ID_TYPE = 'CaptchaInputText'
    ERROR_ALERT_BY_XPATH = '//*[@id="listresult"]'
    DOWNLOAD_BTN_BY_XPATH_TYPE = '//*[@id="formgr"]/div/div/div[1]/div/div/button[2]'
    URL = None
    CORE_NAME = 'MOBIFONE'
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


mobifone_constant = MobifoneConstant()
