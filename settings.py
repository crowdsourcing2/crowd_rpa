import os
import yaml
import tldextract

from pathlib import Path


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
    PORTALS_CONFIG = load_config('portal_config.yaml')


cfg = Config()
