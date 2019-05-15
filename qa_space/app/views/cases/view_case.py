from aiohttp import web
import aiohttp_jinja2
import logging
import db
from aiohttp_session import get_session
import tokens_db

from config import Config

logger = logging.getLogger(__name__)
config = Config()


class ViewCaseView(web.View):
    @aiohttp_jinja2.template('cases/view_case.html')
    async def get(self):
        get_params = self.request.rel_url.query
        logger.debug("Getting cases with params: {}".format(get_params))

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        case_id = None
        if 'id' in get_params:
            case_id = get_params['id']

        if not case_id:
            logger.warning("No case id param in request")
            return web.HTTPNotFound()

        case = db.session.query(db.Cases) \
            .filter(db.Cases.creator == session_data['id']) \
            .filter(db.Cases.deleted == None) \
            .filter(db.Cases.id == case_id) \
            .first()

        if not case:
            logger.warning("case did not find in db")
            return web.HTTPNotFound()

        case_data = case.to_json()
        logger.debug("Found case: {}".format(case_data))

        steps = db.session.query(db.Steps) \
            .filter(db.Steps.case == case_id) \
            .all()

        steps_data = []

        for step in steps:
            steps_data.append(step.to_json())

        case_data["steps"] = steps_data

        case_tag_relations = db.session.query(db.CasesTagsRelation) \
            .filter(db.CasesTagsRelation.case == case.id) \
            .all()

        tags = []
        for relation in case_tag_relations:
            tag = db.session.query(db.Tags) \
                .filter(db.Tags.id == relation.tag) \
                .first()

            tags.append(tag.name)

        case_data['tags'] = ",".join(tags)

        return {
            'auth_service_address': config.AUTH_SERVICE_EXTERNAL,
            'case': case_data,
            'active_tab': 'projects',
        }

    # async def post(self):
    #     get_params = self.request.rel_url.query
    #     logger.debug("Getting cases with params: {}".format(get_params))
    #
    #     session = await get_session(self.request)
    #     logger.debug("Decode auth section")
    #     session_data = tokens_db.decode_token(session['auth'])
    #     logger.debug("Decoded auth section data: {}".format(session_data))
    #
    #     post_data = await self.request.post()
    #     logger.debug("Received login request data: {}".format(post_data))
    #
    #     case_id = None
    #     if 'id' in get_params:
    #         case_id = get_params['id']
    #
    #     if not case_id:
    #         logger.warning("No case id param in request")
    #         return web.HTTPNotFound()
    #     logger.debug("Suite id: {}".format(case_id))
    #
    #     case = db.session.query(db.Cases) \
    #         .filter(db.Cases.creator == session_data['id']) \
    #         .filter(db.Cases.deleted == None) \
    #         .filter(db.Cases.id == case_id) \
    #         .first()
    #
    #     if not case:
    #         logger.warning("Suite did not find in db")
    #         return web.HTTPNotFound()
    #
    #     case.name = post_data['name']
    #     case.description = post_data['description']
    #     db.session.commit()
    #
    #     return web.HTTPFound("/cases?suite={}".format(case.suite))
