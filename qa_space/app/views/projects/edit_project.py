from aiohttp import web
import aiohttp_jinja2
import logging
import db
from aiohttp_session import get_session
import tokens_db

from config import Config

logger = logging.getLogger(__name__)
config = Config()


class EditProjectView(web.View):
    @aiohttp_jinja2.template('projects/edit_project.html')
    async def get(self):
        get_params = self.request.rel_url.query
        logger.debug("Getting projects with params: {}".format(get_params))

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        project_id = None
        if 'id' in get_params:
            project_id = get_params['id']

        if not project_id:
            logger.warning("No project id param in request")
            return web.HTTPNotFound()

        project = db.session.query(db.Projects) \
            .filter(db.Projects.creator == session_data['id']) \
            .filter(db.Projects.deleted == None) \
            .filter(db.Projects.id == project_id) \
            .first()

        if not project:
            logger.warning("Project did not find in db")
            return web.HTTPNotFound()

        project_data = project.to_json()
        logger.debug("Found project: {}".format(project_data))

        return {
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL,
            'project': project_data,
            'active_tab': 'projects',
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

        project_id = None
        if 'id' in get_params:
            project_id = get_params['id']

        if not project_id:
            logger.warning("No project id param in request")
            return web.HTTPNotFound()

        project = db.session.query(db.Projects) \
            .filter(db.Projects.creator == session_data['id']) \
            .filter(db.Projects.deleted == None) \
            .filter(db.Projects.id == project_id) \
            .first()

        if not project:
            logger.warning("Project did not find in db")
            return web.HTTPNotFound()

        project.name = post_data['name']
        project.description = post_data['description']
        db.session.commit()

        return web.HTTPFound("/projects")
