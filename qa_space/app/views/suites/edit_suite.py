from aiohttp import web
import aiohttp_jinja2
import logging
import db
from aiohttp_session import get_session
import tokens_db

from config import Config

logger = logging.getLogger(__name__)
config = Config()


class EditSuiteView(web.View):
    @aiohttp_jinja2.template('suites/edit_suite.html')
    async def get(self):
        get_params = self.request.rel_url.query
        logger.debug("Getting suites with params: {}".format(get_params))

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        suite_id = None
        if 'id' in get_params:
            suite_id = get_params['id']

        if not suite_id:
            logger.warning("No suite id param in request")
            return web.HTTPNotFound()

        suite = db.session.query(db.Suites) \
            .filter(db.Suites.creator == session_data['id']) \
            .filter(db.Suites.deleted == None) \
            .filter(db.Suites.id == suite_id) \
            .first()

        if not suite:
            logger.warning("suite did not find in db")
            return web.HTTPNotFound()

        suite_data = suite.to_json()
        logger.debug("Found suite: {}".format(suite_data))

        return {
            'auth_service_address': config.AUTH_SERVICE_ADDRESS,
            'suite': suite_data,
            'active_tab': 'suites',
        }

    async def post(self):
        get_params = self.request.rel_url.query
        logger.debug("Getting suites with params: {}".format(get_params))

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        post_data = await self.request.post()
        logger.debug("Received login request data: {}".format(post_data))

        suite_id = None
        if 'id' in get_params:
            suite_id = get_params['id']

        if not suite_id:
            logger.warning("No suite id param in request")
            return web.HTTPNotFound()
        logger.debug("Suite id: {}".format(suite_id))

        suite = db.session.query(db.Suites) \
            .filter(db.Suites.creator == session_data['id']) \
            .filter(db.Suites.deleted == None) \
            .filter(db.Suites.id == suite_id) \
            .first()

        if not suite:
            logger.warning("Suite did not find in db")
            return web.HTTPNotFound()

        suite.name = post_data['name']
        suite.description = post_data['description']
        db.session.commit()

        return web.HTTPFound("/suites?project={}".format(suite.project))
