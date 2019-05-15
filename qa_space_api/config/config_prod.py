import logging
from config_base import ConfigBase
import sys
import os


class Config(ConfigBase):
    VERSION = "1.0.0"
    IS_DEBUG = False

    PORT = 7080
    HOST = "0.0.0.0"

    DB_URI = 'postgresql://postgres:postgres@db:5432/qa_space'

    # Logging
    LOG_FORMAT = '%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s'
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = None

    AUTH_SERVICE_INTERNAL = "http://qa_space_auth:7000"
    AUTH_SERVICE_EXTERNAL = "http://127.0.0.1:7000"

    NON_LOGIN_URLS = [
        'doc',
    ]

    os.chdir(os.path.dirname(__file__))
    PROJECT_DIR = os.getcwd()
    sys.path.append(PROJECT_DIR)
