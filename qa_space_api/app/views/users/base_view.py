from aiohttp import web
import logging
import requests
import json
from config import Config

logger = logging.getLogger(__name__)
config = Config()


class BaseView(web.View):
    def check_user_data(self):
        get_params = self.request.rel_url.query
        if 'api_key' not in get_params:
            return web.json_response({"error": "No API key specified"}, status=400)
        logger.debug("Getting projects with params: {}".format(get_params))
        uuid = get_params['api_key']

        rsp = requests.get("{}/api_token?uuid={}".format(config.AUTH_SERVICE_INTERNAL, uuid))
        if rsp.status_code != 200:
            logger.error("Auth response is {} expected 200. Error: {}".format(rsp.status_code, rsp.text))
            return web.json_response({"error": "Not found"}, status=404)
        user_data = rsp.json()
        return user_data

    async def get(self):
        self.user_data = self.check_user_data()

    async def post(self):
        self.user_data = self.check_user_data()

        self.data = await self.request.json()
        logger.debug("Received login request data: {}".format(self.data))

        for item in self.post_required_fields:
            if item not in self.data:
                rsp_data = {
                    "error": "Field {} not specified in request data".format(item)
                }
                raise web.HTTPBadRequest(text=json.dumps(rsp_data))

            if not self.data[item]:
                rsp_data = {
                    "error": "Field {} can not be empty".format(item)
                }
                raise web.HTTPBadRequest(text=json.dumps(rsp_data))

    async def put(self):
        self.user_data = self.check_user_data()

    async def delete(self):
        self.user_data = self.check_user_data()
