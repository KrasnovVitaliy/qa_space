from aiohttp import web
import aiohttp_jinja2
import logging

from config import Config

logger = logging.getLogger(__name__)
config = Config()


class IndexView(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return web.HTTPFound("/projects")
