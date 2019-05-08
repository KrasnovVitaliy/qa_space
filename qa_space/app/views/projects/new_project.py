from aiohttp import web
import aiohttp_jinja2
import logging
import db
from aiohttp_session import get_session
import tokens_db

from config import Config

logger = logging.getLogger(__name__)
config = Config()


class NewProjectView(web.View):
    @aiohttp_jinja2.template('projects/new_project.html')
    async def get(self):
        get_params = self.request.rel_url.query
        logger.debug("Getting projects with params: {}".format(get_params))

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        return {
            'auth_service_address': config.AUTH_SERVICE_ADDRESS,
            'active_tab': 'projects',
        }

    async def post(self):
        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        post_data = await self.request.post()
        logger.debug("Received login request data: {}".format(post_data))

        project = db.session.query(db.Projects)\
            .filter(db.Projects.creator == session_data['id'])\
            .filter(db.Projects.name == post_data['name']) \
            .filter(db.Projects.deleted == None) \
            .first()
        if project:
            return web.json_response({"error": "Such project name already in used"}, status=400)

        project = db.Projects()
        project.name = post_data['name']
        project.description = post_data['description']
        project.creator = session_data['id']

        db.session.add(project)
        db.session.commit()

        return web.HTTPFound("/suites?project={}".format(project.id))
