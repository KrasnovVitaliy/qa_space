from aiohttp import web
import aiohttp_jinja2
import logging
from aiohttp_session import get_session
import requests
import json
from config import Config
from .base_view import BaseView

logger = logging.getLogger(__name__)
config = Config()


class ProfileView(BaseView):
    def __init__(self, request):
        super(ProfileView, self).__init__(request=request)

        self.post_required_fields = [
            "first_name",
            "last_name",
            "email",
            "password"
        ]

    async def get(self):
        await super(ProfileView, self).get()
        return web.json_response({"profile": self.user_data}, status=200)

    async def post(self):
        await super(ProfileView, self).post()
        return web.json_response({}, status=200)

        # if 'password' in data:
        #     if 'password_repeat' not in data:
        #         return web.HTTPError()
        #     if data['password_repeat'] != data['password']:
        #         return web.HTTPError()
        # user_data = {}
        # for key in ['first_name', 'last_name', 'email', 'password']:
        #     if key in data:
        #         if data[key]:
        #             user_data[key] = data[key]
        #
        # ret = requests.put("{}/users?id={}".format(config.AUTH_SERVICE_INTERNAL, self.user_data['id']),
        #                    data=json.dumps(user_data))
        #
        # if ret.status_code != 200:
        #     return web.HTTPError()
        #
        # return web.HTTPFound("/edit_profile")
