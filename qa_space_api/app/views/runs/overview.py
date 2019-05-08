from aiohttp import web
import aiohttp_jinja2
import logging
import db
from aiohttp_session import get_session
import requests
import tokens_db
import datetime

from config import Config

logger = logging.getLogger(__name__)
config = Config()


class RunsOverviewView(web.View):
    @aiohttp_jinja2.template('not_implemented.html')
    async def get(self):
        return {
            'auth_service_address': config.AUTH_SERVICE_ADDRESS,
            'active_tab': 'runs',
        }
