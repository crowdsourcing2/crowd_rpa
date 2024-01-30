class RosySoftConstant:
    TAB2_BUTTON_BY_CLASS_TYPE = 'tab2'
    TEXT_TAXCODE_BY_ID_TYPE = 'txtTaxCode2'
    TEXT_SEARCH_CODE_BY_ID_TYPE = 'txtInvID'
    SUBMIT_BTN_BY_ID_TYPE = '#content2 #btnSubmit'
    DOWNLOAD_PDF_XPATH = '//*[@class="row-fluid"]/div/div/article/div/div/div[2]/table/tbody/tr/td[2]/div/span[1]/img'
    DOWNLOAD_XML_XPATH = '//*[@class="row-fluid"]/div/div/article/div/div/div[2]/table/tbody/tr/td[2]/div/span[3]/img'

    URL = 'https://einv.rosysoft.vn:8386/Account/LogIn?ReturnUrl=%2f'
    URL_N = 'https://einv.rosysoft.vn:8386/RSeInvoiceSearch'
    META_DATA = {
        'URL': URL,
        'RPA_NAME': 'CORES.ROSY_SOFT.RPA',
        'DRIVER_NAME': 'chrome'
    }
    DELAY_OPEN_MAXIMUM_BROWSER = 0.2
    DELAY_TIME_LOAD_PAGE = 1.5
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 1.5
    DELAY_TIME_SKIP = 0.3


rosysoft_constant = RosySoftConstant()
