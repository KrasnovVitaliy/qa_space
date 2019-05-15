from aiohttp import web
import aiohttp_jinja2
import logging

from config import Config

logger = logging.getLogger(__name__)
config = Config()


class LoginView(web.View):
    @aiohttp_jinja2.template('auth_users/login.html')
    async def get(self):
        return {
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL,
        }
