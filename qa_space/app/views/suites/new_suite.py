from aiohttp import web
import aiohttp_jinja2
import logging
import db
from aiohttp_session import get_session
import tokens_db

from config import Config

logger = logging.getLogger(__name__)
config = Config()


class NewSuiteView(web.View):
    @aiohttp_jinja2.template('suites/new_suite.html')
    async def get(self):
        get_params = self.request.rel_url.query
        logger.debug("Getting suites with params: {}".format(get_params))

        project_id = None
        if 'project' in get_params:
            project_id = get_params['project']

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        return {
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL,
            'project_id': project_id
        }

    async def post(self):
        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        post_data = await self.request.post()
        logger.debug("Received login request data: {}".format(post_data))

        suite = db.session.query(db.Suites) \
            .filter(db.Suites.creator == session_data['id']) \
            .filter(db.Suites.name == post_data['name']) \
            .filter(db.Suites.project == post_data['project']) \
            .filter(db.Suites.deleted == None) \
            .first()
        if suite:
            return web.json_response({"error": "Such suite name already in used"}, status=400)

        suite = db.Suites()
        suite.name = post_data['name']
        suite.project = post_data['project']
        suite.description = post_data['description']
        suite.creator = session_data['id']

        db.session.add(suite)
        db.session.commit()

        return web.HTTPFound("/cases?suite={}".format(suite.id))
