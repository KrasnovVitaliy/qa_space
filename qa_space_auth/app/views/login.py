from aiohttp import web
from aiohttp_cors import CorsViewMixin
import logging
import time

import tokens_db
from config import Config
import db
from aiohttp_session import get_session

logger = logging.getLogger(__name__)
config = Config()


class LoginView(web.View, CorsViewMixin):
    async def post(self):
        data = await self.request.post()
        logger.debug("Received login request data: {}".format(data))
        logger.debug("Is email and password fields present")
        if "email" not in data or "password" not in data:
            return web.json_response({"error": "No email or password field in request body"}, status=400)

        logger.debug("Get user from db")
        user = db.session.query(db.Users).filter(db.Users.email == data['email']).filter(
            db.Users.deleted == None).first()
        if not user:
            return web.json_response({"error": "User not found"}, status=404)
        logger.debug("User found: {}".format(user.to_json()))

        if not tokens_db.check_password(data['password'], user.pass_hash):
            return web.json_response({"error": "Incorrect password"}, status=400)

        logger.debug("Creating JWT")
        jwt = tokens_db.encode_token(
            {
                'id': user.id,
                'login_date': int(time.time())
            }
        )

        logger.debug("Encoded JWT: {}".format(jwt))
        session = await get_session(self.request)
        session['auth'] = jwt.decode("utf-8")
        return web.HTTPFound(config.QA_SPACE_ADDRESS_INDEX)
