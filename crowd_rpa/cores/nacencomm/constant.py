class NacencommConstant:
    FILE_PATH = './RPA_TEMP/misa.pdf'
    URL_KEYWORD = 'Tra cứu tại Website (Search on Website):'
    CODE_BILL_KEYWORD = 'Mã tra cứu hóa đơn (Invoice code):'
    LAST_KEYWORD = 'Mã CQT: '

    SEARCH_BTN_BY_XPATH = '//*[@id="ctl01"]/div[8]/a[2]'
    CHOICE_RADIO_BY_XPATH = '//*[@id="tabTBSSHoadon_rdselect_RB1_I_D"]'
    ID_INPUT_BY_ID = 'tabTBSSHoadon_pnchuoi_txtChuoixt_I'
    SUBMIT_BTN_BY_ID = 'tabTBSSHoadon_pnchuoi_btnTracuu_CD'
    DOWNLOAD_ZIP_BY_ID = 'ASPxCallbackPanel1_btnDownload'
    URL = None
    CORE_NAME = 'NACENCOMM'
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


nacencomm_constant = NacencommConstant()
