from aiohttp import web
import aiohttp_jinja2
import logging
from aiohttp_session import get_session
import tokens_db
import requests
import json
from config import Config

logger = logging.getLogger(__name__)
config = Config()


class EditProfileView(web.View):
    @aiohttp_jinja2.template('auth_users/edit_profile.html')
    async def get(self):
        get_params = self.request.rel_url.query
        logger.debug("Getting projects with params: {}".format(get_params))

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        rsp = requests.get("{}/users?api_key={}&id={}".format(config.AUTH_SERVICE_ADDRESS, config.AUTH_MASTER_API_KEY,
                                                              session_data['id']))
        if rsp.status_code != 200:
            logger.error("Auth response is {} expected 200. Error: {}".format(rsp.status_code, rsp.text))
            return web.HTTPFound('/login')
        user_data = rsp.json()

        if not user_data:
            return web.HTTPNotFound()

        return {
            'auth_service_address': config.AUTH_SERVICE_ADDRESS,
            'profile': user_data,
            'active_tab': 'profile',
        }

    async def post(self):
        get_params = self.request.rel_url.query
        logger.debug("Getting projects with params: {}".format(get_params))

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        post_data = await self.request.post()
        logger.debug("Received login request data: {}".format(post_data))

        if 'password' in post_data:
            if 'password_repeat' not in post_data:
                return web.HTTPError()
            if post_data['password_repeat'] != post_data['password']:
                return web.HTTPError()
        user_data = {}
        for key in ['first_name', 'last_name', 'email', 'password']:
            if key in post_data:
                if post_data[key]:
                    user_data[key] = post_data[key]

        ret = requests.put("{}/users?id={}".format(config.AUTH_SERVICE_ADDRESS, session_data['id']),
                           data=json.dumps(user_data))

        if ret.status_code != 200:
            return web.HTTPError()

        return web.HTTPFound("/edit_profile")
