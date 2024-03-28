from os.path import join, dirname
import yaml


def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


class Config:
    VERSION = "v0.1.0"
    TIME_RELOADING_PAGE = 2
    TIME_WAIT_PAGE = 10
    SCREEN_WIDTH_DEFAULT = 1920
    SLIDER_BAR_TIME_RELOAD_MIN = 1
    SLIDER_BAR_TIME_RELOAD_MAX = 20
    MAX_WORKERS = 8
    MAX_THREAD_POOL = 8
    TIME_SKIP_PAGE = 3
    TIME_SKIP_INTRO = 5
    DRIVER_TAG = "firefox"  # Optional ["firefox", "chrome", "undetected_chrome"]
    undetected_chrome = 3
    HEIGHT_IMAGE = 200
    SCALE_DEFAULT = 80
    WIDTH_DEFAULT = 1920
    SCALE_WIDTH_DEFAULT = 800
    COOKIE_EXPIRY_DAYS = 30
    MASTER_TOOLS_LOGO = "https://cdn-icons-png.flaticon.com/512/807/807262.png"
    PORTALS_CONFIG = load_config(join(dirname(__file__), 'portal_config.yaml'))
    TEST_ROOT_PTH = join(join(dirname(dirname(__file__)), 'tests'), 'output')
    IMG_CAPTCHA_DIR = join(join(dirname(dirname(__file__)), 'tests'), 'img_captcha')
    LOOKUP_PATTERNS = [
        r'Mã tra cứu: (\w+)',
        r'\(Invoice code\):\s*([A-Z0-9]+)',
        r'Mã tra cứu HĐĐT này: (\w+)',
        r'mã tra cứu:\s*([A-Z0-9]+)',
        r'Mã nhận hóa đơn :\s*([A-Z0-9]+)',
        r' Mã số tra cứu: \s*([A-Z0-9]+)',
        r'mã tra cứu: \s*([A-Z0-9]+)',
        r'Chuỗi xác thực \(Digest Value\): (.+)',
        r'MTC: ([A-F0-9]+)',
        r'Mã tra cứu:\s*([A-Z0-9]+)'
    ]
    COMPANY_PATTERNS = [
        r'mã công ty: \s*([A-Z0-9]+)',
        r'mã công ty: (\d+)',
        r' mã công ty: (\d+)',
        r'Mã số thuế \(Tax code\) : ([0-9 ]+)'
    ]
    USE_COMPANY_CODE_ATTR = 'USE_COMPANY_CODE'


cfg = Config()
