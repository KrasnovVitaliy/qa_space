import logging
from config_base import ConfigBase
import sys
import os


class Config(ConfigBase):
    VERSION = "1.0.0"
    IS_DEBUG = True

    PORT = 7080
    HOST = "0.0.0.0"

    DB_URI = 'sqlite:////db/qa_space.db'
    # Logging
    LOG_FORMAT = '%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s'
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = None

    AUTH_SERVICE_ADDRESS = "http://127.0.0.1:7000"

    NON_LOGIN_URLS = [
        'doc',
    ]

    os.chdir(os.path.dirname(__file__))
    PROJECT_DIR = os.getcwd()
    sys.path.append(PROJECT_DIR)
