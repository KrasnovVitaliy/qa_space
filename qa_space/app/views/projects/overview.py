from aiohttp import web
import aiohttp_jinja2
import logging
import db
from aiohttp_session import get_session
import requests
import tokens_db
import datetime
from config import Config

logger = logging.getLogger(__name__)
config = Config()


class ProjectsOverviewView(web.View):
    @aiohttp_jinja2.template('projects/overview.html')
    async def get(self, *args, **kwargs):
        params = self.request.rel_url.query
        logger.debug("Getting user with params: {}".format(params))

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        rsp = requests.get("{}/users?api_key={}&id={}".format(config.AUTH_SERVICE_ADDRESS, config.AUTH_MASTER_API_KEY, session_data['id']))
        if rsp.status_code != 200:
            logger.error("Auth response is {} expected 200. Error: {}".format(rsp.status_code, rsp.text))
            return web.HTTPFound('/login')
        user_data = rsp.json()

        projects = db.session.query(db.Projects).filter(db.Projects.creator == session_data['id']).filter(
            db.Projects.deleted == None).all()
        projects_data = []
        for project in projects:
            suites_count = db.session.query(db.Suites) \
                .filter(db.Suites.creator == session_data['id']) \
                .filter(db.Suites.project == project.id) \
                .filter(db.Suites.deleted == None) \
                .count()

            item = project.to_json()
            # item['creator'] = "{}+{}".format(user_data['first_name'], user_data['last_name'])
            item['creator'] = user_data
            item['suites'] = suites_count
            projects_data.append(item)

        logger.debug("Found projects: {}".format(projects_data))
        return {
            'auth_service_address': config.AUTH_SERVICE_ADDRESS,
            'projects': projects_data,
            'active_tab': 'projects',
        }

    async def delete(self):
        params = self.request.rel_url.query
        logger.debug("Removing project with params: {}".format(params))

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        project = db.session.query(db.Projects).filter(db.Projects.id == params['id']).filter(
            db.Projects.creator == session_data['id']).first()
        if not project:
            return web.json_response({
                "status": "error",
                "error": "No such project",
            })

        project.deleted = datetime.datetime.now()
        db.session.commit()
        logger.debug("Project removed")

        return web.json_response({"status": "ok"})
