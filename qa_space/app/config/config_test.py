import logging
from config_base import ConfigBase
import sys
import os


class Config(ConfigBase):
    VERSION = "1.0.0"
    IS_DEBUG = True

    PORT = 8080
    HOST = "0.0.0.0"

    # DB_URI = 'sqlite:////db/qa_space.db'
    DB_URI = 'postgresql://postgres:127.0.0.1@db:5432/qa_space_auth'

    # Logging
    LOG_FORMAT = '%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s'
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = None

    AUTH_SERVICE_ADDRESS = "http://127.0.0.1:7000"

    TOKENS_SECRET = "nzIxhdYtE4UUDITCHst9bhvSJsuhPMbYNostg28oM"
    COOKIE_SECRET = "kioQTiAtFMoncsZOYRnj5IvagCndNV2e9LFy1RNEMOU="
    AUTH_MASTER_API_KEY = "a4e2cbe005ad54e2d8d101fcd2618f87"

    NON_LOGIN_URLS = [
        'login',
        'logout',
        'sign_up',
        'static'
    ]

    os.chdir(os.path.dirname(__file__))
    PROJECT_DIR = os.getcwd()
    sys.path.append(PROJECT_DIR)
