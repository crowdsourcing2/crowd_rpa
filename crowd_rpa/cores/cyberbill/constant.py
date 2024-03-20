class CyberBillConstant:
    INPUT_ID_BY_NAME ='MaSoBiMat'
    PATH_PDF_FILE ='./RPA_TEMP/cyberbill.pdf'
    CAPTCHA_IMG_BY_XPATH ='/html/body/app-root/ng-component/ng-component/div/div/div/div/div/div[2]/div/form/div[2]/img'
    CAPTCHA_INPUT_BY_XPATH = '/html/body/app-root/ng-component/ng-component/div/div/div/div/div/div[2]/div/form/div[3]/input'
    BUTTON_SEARCH_BY_XPATH ='/html/body/app-root/ng-component/ng-component/div/div/div/div/div/div[2]/div/form/div[4]/button'
    ERROR_ALERT_BY_CLASS ='toast-message'
    DOWNLOAD_PDF_XPATH = '/html/body/app-root/ng-component/ng-component/popup-modal/div/div/div/div[3]/button[2]'
    DOWNLOAD_XML_XPATH = '/html/body/app-root/ng-component/ng-component/popup-modal/div/div/div/div[3]/button[1]'
    URL = None
    CORE_NAME = 'CYBERBILL'
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
    RETRY_MAX = 5


cyber_bill_constant = CyberBillConstant()


