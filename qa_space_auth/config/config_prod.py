import logging
from config_base import ConfigBase
import os
import sys


class Config(ConfigBase):
    VERSION = "1.0.0"
    IS_DEBUG = False

    PORT = 7000
    HOST = "0.0.0.0"

    DB_URI = 'postgresql://postgres:postgres@db:5432/qa_space_auth'

    # Logging
    LOG_FORMAT = '%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s'
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = None

    TOKENS_SECRET = "nzIxhdYtE4UUDITCHst9bhvSJsuhPMbYNostg28oM"
    COOKIE_SECRET = "kioQTiAtFMoncsZOYRnj5IvagCndNV2e9LFy1RNEMOU="
    MASTER_API_KEY = "a4e2cbe005ad54e2d8d101fcd2618f87"

    QA_SPACE_INTERNAL = 'http://qa_space:8080'
    QA_SPACE_EXTERNAL = 'http://127.0.0.1:8080'

    os.chdir(os.path.dirname(__file__))
    PROJECT_DIR = os.getcwd()
    sys.path.append(PROJECT_DIR)
