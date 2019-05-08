from aiohttp import web
import aiohttp_jinja2
import logging
import db
from aiohttp_session import get_session
import tokens_db

from config import Config

logger = logging.getLogger(__name__)
config = Config()


class EditCaseView(web.View):
    @aiohttp_jinja2.template('cases/edit_case.html')
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
            'auth_service_address': config.AUTH_SERVICE_ADDRESS,
            'case': case_data,
            'active_tab': 'projects',
        }

    async def post(self):
        get_params = self.request.rel_url.query
        logger.debug("Getting cases with params: {}".format(get_params))

        session = await get_session(self.request)
        logger.debug("Decode auth section")
        session_data = tokens_db.decode_token(session['auth'])
        logger.debug("Decoded auth section data: {}".format(session_data))

        post_data = await self.request.post()
        logger.debug("Received login request data: {}".format(post_data))

        case_id = None
        if 'id' in get_params:
            case_id = get_params['id']

        if not case_id:
            logger.warning("No case id param in request")
            return web.HTTPNotFound()
        logger.debug("Suite id: {}".format(case_id))

        case = db.session.query(db.Cases) \
            .filter(db.Cases.creator == session_data['id']) \
            .filter(db.Cases.deleted == None) \
            .filter(db.Cases.id == case_id) \
            .first()

        if not case:
            logger.warning("Suite did not find in db")
            return web.HTTPNotFound()

        case.name = post_data['name']
        case.name = post_data['name']
        case.description = post_data['description']
        case.suite = post_data['suite']
        case.creator = session_data['id']
        case.priority = post_data['priority']
        case.case_type = post_data['case_type']
        case.behaviour = post_data['behaviour']
        case.preconditions = post_data['preconditions']
        case.postconditions = post_data['postconditions']
        db.session.commit()

        db.session.query(db.Steps) \
            .filter(db.Steps.case == case_id) \
            .delete()

        for item in post_data:
            if "step_" in item:
                step = db.Steps()
                step.position = item.split("_")[1]
                step.description = post_data[item]
                step.creator = session_data['id']
                step.case = case.id
                db.session.add(step)
        db.session.commit()

        db.session.query(db.CasesTagsRelation) \
            .filter(db.CasesTagsRelation.case == case_id) \
            .delete()

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

        return web.HTTPFound("/cases?suite={}".format(post_data['suite']))
