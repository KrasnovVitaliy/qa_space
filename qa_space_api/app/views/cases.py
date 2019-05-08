from aiohttp import web
import logging
import db

from config import Config

logger = logging.getLogger(__name__)
config = Config()

from views.base_view import BaseView


class CasesView(BaseView):
    """
        description: API cases endpoint
    """
    def __init__(self, request):
        super(CasesView, self).__init__(request=request)
        self.db_instance = db.Cases
        self.post_required_fields = ['name']
        self.post_available_fields = ['name', 'description', 'suite', 'priority', 'case_type', 'behaviour',
                                      'preconditions', 'postconditions']
        self.post_unique_fields = ['name', 'suite']

    async def __get_cases_steps(self, case_id):
        steps = db.session.query(db.Steps) \
            .filter(db.Steps.case == case_id) \
            .all()

        steps_data = []
        for step in steps:
            steps_data.append(
                {
                    "id": step.id,
                    "position": step.position,
                    "description": step.description
                }
            )
        return steps_data

    async def __get_cases_tags(self, case_id):
        case_tag_relations = db.session.query(db.CasesTagsRelation) \
            .filter(db.CasesTagsRelation.case == case_id) \
            .all()

        tags = []
        for relation in case_tag_relations:
            tag = db.session.query(db.Tags) \
                .filter(db.Tags.id == relation.tag) \
                .first()

            tags.append(tag.name)

        return tags

    async def get(self):
        """
            arg: id:int:case id:required
            arg: api_key:str:user api key:required

            ret: id:int:case id
            ret: create_date:datetime:case creation datetime
            ret: update_date:datetime:case update datetime
            ret: name:str:case name
            ret: description:str:case description
            ret: creator:int:case creator user id
            ret: suite:int:related suit id
            ret: priority:str:case priority
            ret: case_type:str:case type
            ret: behaviour:str:case behaviour
            ret: preconditions:str:case preconditions
            ret: postconditions:str:case postconditions
            ret: steps:[{step}]:case steps
            ret: tags:[string]:case tags
            ret: deleted:datetime:project deleted datetime
        """

        await super(CasesView, self).get()
        if isinstance(self.ret_data, list):
            pass
            for case in self.ret_data:
                case['steps'] = await self.__get_cases_steps(case_id=case['id'])
                case['tags'] = await self.__get_cases_tags(case_id=case['id'])

        elif isinstance(self.ret_data, dict):
            case = self.ret_data
            case['steps'] = await self.__get_cases_steps(case_id=case['id'])
            case['tags'] = await self.__get_cases_tags(case_id=case['id'])

        return web.json_response(self.ret_data)

    async def post(self):
        """
            arg: api_key:str:user api key:required

            body: name:str:case name
            body: description:str:case description
            body: suite:int:related suit id
            body: priority:str:case priority
            body: case_type:str:case type
            body: behaviour:str:case behaviour
            body: preconditions:str:case preconditions
            body: postconditions:str:case postconditions

            ret: id:int:case id
            ret: create_date:datetime:case creation datetime
            ret: update_date:datetime:case update datetime
            ret: name:str:case name
            ret: description:str:case description
            ret: creator:int:case creator user id
            ret: suite:int:related suit id
            ret: priority:str:case priority
            ret: case_type:str:case type
            ret: behaviour:str:case behaviour
            ret: preconditions:str:case preconditions
            ret: postconditions:str:case postconditions
            ret: steps:[{step}]:case steps
            ret: tags:[string]:case tags
            ret: deleted:datetime:project deleted datetime
        """
        await super(CasesView, self).post()
        return web.json_response(self.ret_data, status=201)

    async def put(self):
        """
            arg: id:int:case id:required
            arg: api_key:str:user api key:required

            body: name:str:case name
            body: description:str:case description
            body: suite:int:related suit id
            body: priority:str:case priority
            body: case_type:str:case type
            body: behaviour:str:case behaviour
            body: preconditions:str:case preconditions
            body: postconditions:str:case postconditions

            ret: id:int:case id
            ret: create_date:datetime:case creation datetime
            ret: update_date:datetime:case update datetime
            ret: name:str:case name
            ret: description:str:case description
            ret: creator:int:case creator user id
            ret: suite:int:related suit id
            ret: priority:str:case priority
            ret: case_type:str:case type
            ret: behaviour:str:case behaviour
            ret: preconditions:str:case preconditions
            ret: postconditions:str:case postconditions
            ret: steps:[{step}]:case steps
            ret: tags:[string]:case tags
            ret: deleted:datetime:project deleted datetime
        """
        await super(CasesView, self).put()
        return web.json_response(self.ret_data, status=200)

    async def delete(self):
        """
                    arg: id:int:case id:required
                    arg: api_key:str:user api key:required
        """
        await super(CasesView, self).delete()
        return web.json_response({}, status=200)
