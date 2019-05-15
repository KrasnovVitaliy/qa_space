from aiohttp import web
import aiohttp_jinja2
import logging

from config import Config

logger = logging.getLogger(__name__)
config = Config()


class SignUpView(web.View):
    @aiohttp_jinja2.template('auth_users/sign_up.html')
    async def get(self):
        return {
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL,
        }
