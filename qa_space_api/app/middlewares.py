from aiohttp import web
from config import Config
import logging

logger = logging.getLogger(__name__)
config = Config()


@web.middleware
async def auth_middleware(request, handler):
    try:
        splitted_path = request.url.path.split("/")
        if splitted_path[1] in config.NON_LOGIN_URLS:
            response = await handler(request)
            return response

        params = request.rel_url.query
        if 'api_key' not in params:
            return web.json_response({"error": "No API key specified"}, status=400)
        #
        # session = await get_session(request)
        # logger.debug("Received session: {}".format(session))
        #
        # logger.debug("Is auth section in cookies session")
        # if 'auth' not in session:
        #     logger.debug("No auth sections in cookies")
        #     return web.HTTPFound('/login')
        #
        # logger.debug("Decode auth section")
        # data = tokens_db.decode_token(session['auth'])
        # logger.debug("Decoded auth section data: {}".format(data))


    except web.HTTPException as ex:
        logger.warning("Http error")
        if ex.status != 404:
            raise

    response = await handler(request)
    return response
