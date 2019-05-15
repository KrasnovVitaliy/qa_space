from aiohttp import web
import aiohttp_jinja2
import logging
import db
from aiohttp_session import get_session
import tokens_db

from config import Config

logger = logging.getLogger(__name__)
config = Config()


class NewCaseView(web.View):
    @aiohttp_jinja2.template('cases/new_case.html')
    async def get(self):
        get_params = self.request.rel_url.query
        logger.debug("Getting suites with params: {}".format(get_params))

        suite_id = None
        if 'suite' in get_params:
            suite_id = get_params['suite']

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        return {
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL,
            'suite_id': suite_id
        }

    async def post(self):
        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        post_data = await self.request.post()
        logger.debug("Received new case post data: {}".format(post_data))

        case = db.session.query(db.Cases) \
            .filter(db.Cases.creator == session_data['id']) \
            .filter(db.Cases.name == post_data['name']) \
            .filter(db.Cases.suite == post_data['suite']) \
            .filter(db.Cases.deleted == None) \
            .first()
        if case:
            return web.json_response({"error": "Such case name already in used for given suite"}, status=400)

        case = db.Cases()
        case.name = post_data['name']
        case.description = post_data['description']
        case.suite = post_data['suite']
        case.creator = session_data['id']
        case.priority = post_data['priority']
        case.case_type = post_data['case_type']
        case.behaviour = post_data['behaviour']
        case.preconditions = post_data['preconditions']
        case.postconditions = post_data['postconditions']

        db.session.add(case)
        db.session.commit()

        tags = post_data['tags'].replace(' ', '').split(',')
        for item in tags:
            tag = db.session.query(db.Tags).filter(db.Tags.name == item).first()
            if not tag:
                tag = db.Tags()
                tag.name = item
                tag.creator = session_data['id']
                db.session.add(tag)
                db.session.commit()

            case_tag_relation = db.session.query(db.CasesTagsRelation) \
                .filter(db.CasesTagsRelation.case == case.id) \
                .filter(db.CasesTagsRelation.tag == tag.id).first()

            if not case_tag_relation:
                case_tag_relation = db.CasesTagsRelation()
                case_tag_relation.case = case.id
                case_tag_relation.tag = tag.id
                db.session.add(case_tag_relation)
                db.session.commit()

        for item in post_data:
            if "step_" in item:
                step = db.Steps()
                step.position = item.split("_")[1]
                step.description = post_data[item]
                step.creator = session_data['id']
                step.case = case.id
                db.session.add(step)
        db.session.commit()

        return web.HTTPFound("/cases?suite={}".format(post_data['suite']))
