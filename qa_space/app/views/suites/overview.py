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


class SuitesOverviewView(web.View):
    @aiohttp_jinja2.template('suites/overview.html')
    async def get(self):
        params = self.request.rel_url.query
        logger.debug("Getting suite with params: {}".format(params))

        if 'project' not in params:
            return web.HTTPNotFound()

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        rsp = requests.get("{}/users?api_key={}&id={}".format(config.AUTH_SERVICE_INTERNAL, config.AUTH_MASTER_API_KEY,
                                                              session_data['id']))
        if rsp.status_code != 200:
            logger.error("Auth response is {} expected 200. Error: {}".format(rsp.status_code, rsp.text))
            return web.HTTPFound('/login')
        user_data = rsp.json()

        suites = db.session.query(db.Suites) \
            .filter(db.Suites.creator == session_data['id']) \
            .filter(db.Suites.project == params['project']) \
            .filter(db.Suites.deleted == None) \
            .all()
        suites_data = []
        for suite in suites:
            cases_count = db.session.query(db.Cases) \
                .filter(db.Cases.creator == session_data['id']) \
                .filter(db.Cases.suite == suite.id) \
                .filter(db.Cases.deleted == None) \
                .count()

            item = suite.to_json()
            # item['creator'] = "{}+{}".format(user_data['first_name'], user_data['last_name'])
            item['creator'] = user_data
            item['cases_count'] = cases_count
            suites_data.append(item)

        logger.debug("Found suites: {}".format(suites_data))

        project = db.session.query(db.Projects) \
            .filter(db.Projects.creator == session_data['id']) \
            .filter(db.Projects.id == params['project']) \
            .filter(db.Projects.deleted == None) \
            .first()
        return {
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL,
            'suites': suites_data,
            'project': project,
            'active_tab': 'projects',
        }

    async def delete(self):
        params = self.request.rel_url.query
        logger.debug("Removing suite with params: {}".format(params))

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        suite = db.session.query(db.Suites).filter(db.Suites.id == params['id']).filter(
            db.Suites.creator == session_data['id']).first()
        if not suite:
            return web.json_response({
                "status": "error",
                "error": "No such suite",
            })

        suite.deleted = datetime.datetime.now()
        db.session.commit()
        logger.debug("Suite removed")

        return web.json_response({"status": "ok"})
