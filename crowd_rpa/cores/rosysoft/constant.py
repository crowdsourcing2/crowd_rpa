class RosySoftConstant:
    FILE_PATH = './RPA_TEMP/rosysoft.pdf'
    # URL_KEYWORD = 'PortalLink'  # tag name contains data
    URL_KEYWORD = 'Trang tra cứu:'
    # CODE_BILL_KEYWORD = 'Key'
    CODE_BILL_KEYWORD = 'Mã tra cứu:'
    LAST_KEYWORD = '(Cần kiểm tra, đối chiếu khi lập, giao nhận hóa đơn)'

    TAX_CODE_KEYWORD = 'Mã số thuế(Tax code):'
    LAST_TAXT_KEYWORD = 'Địa chỉ(Address):'

    TAB2_BUTTON_BY_ID_TYPE = 'tab2'
    TEXT_TAXCODE_BY_ID_TYPE = 'txtTaxCode2'
    TEXT_SEARCH_CODE_BY_ID_TYPE = 'txtInvID'
    SUBMIT_BTN_BY_ID_TYPE = '#content2 #btnSubmit'
    DOWNLOAD_PDF_XPATH = '//*[@class="row-fluid"]/div/div/article/div/div/div[2]/table/tbody/tr/td[2]/div/span[1]/img'
    DOWNLOAD_XML_XPATH = '//*[@class="row-fluid"]/div/div/article/div/div/div[2]/table/tbody/tr/td[2]/div/span[3]/img'
    URL = None
    URL_N = 'https://einv.rosysoft.vn:8386/RSeInvoiceSearch'
    CORE_NAME = 'ROSYSOFT'
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
    DELAY_TIME_LOAD_PAGE = 1.5
    DELAY_CLICK_DOWNLOAD_EVERY_FILE = 1.5
    DELAY_TIME_SKIP = 0.3


rosysoft_constant = RosySoftConstant()
