from enum import Enum


class CollectorStatus(Enum):
    NF_PORTAL = 'NF_PORTAL'  # Lấy đường dẫn tra cứu trong pdf
    NF_LOOKUP_INFO = 'NF_LOOKUP_INFO'  # Lấy mã tra cứu
    NF_INVOICE = 'NF_INVOICE'  # Lấy mã hóa đơn
    INVALID_DOWNLOAD_INFO = 'INVALID_DOWNLOAD_INFO'  # lấy xml và pdf
    ERROR_CAPTCHA = 'ERROR_CAPTCHA'  # Khi mà portal mà có captcha mà ko xử lí đc
    ERROR = 'ERROR'  # Something went wrong
    SUBMITTED = 'SUBMITTED'  # qua hết step đúng
    SUBMITTED_ERROR = "SUBMITTED_ERROR"


class ExtractorStatus(Enum):
    INVALID_MONEY = 'INVALID_MONEY'
    PARSER_ERROR = 'PARSER_ERROR'
    XML_NOT_FOUND = 'XML_NOT_FOUND'
    SUBMITTED = 'SUBMITTED'


class ProcessStatus(Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'


class FlowName(Enum):
    GET_PORTAL = 'GET_PORTAL'
    LOOKUP_INFO = 'LOOKUP_INFO'
    DOWNLOAD_INFO = 'DOWNLOAD_INFO'
    SUBMITTED = 'SUBMITTED'
