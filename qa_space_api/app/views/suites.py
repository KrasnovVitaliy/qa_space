from aiohttp import web
import logging
import db

from config import Config

logger = logging.getLogger(__name__)
config = Config()

from views.base_view import BaseView


class SuitesView(BaseView):
    """
    description: API suites endpoint
    """

    def __init__(self, request):
        super(SuitesView, self).__init__(request=request)
        self.db_instance = db.Suites
        self.post_required_fields = ['name', 'project']
        self.post_available_fields = ['name', 'description', 'project']
        self.post_unique_fields = ['name', 'project']

    async def __get_suite_cases(self, suite_id):
        cases = db.session.query(db.Cases) \
            .filter(db.Cases.creator == self.user_data['id']) \
            .filter(db.Cases.suite == suite_id) \
            .filter(db.Cases.deleted == None) \
            .all()

        cases_data = []
        for suite in cases:
            cases_data.append(suite.id)

        return cases_data

    async def get(self):
        """
            arg: id:int:suite id:required
            arg: api_key:str:user api key:required

            ret: id:int:suite id
            ret: create_date:datetime:suite creation datetime
            ret: update_date:datetime:suite update datetime
            ret: name:str:suite name
            ret: description:str:suite description
            ret: creator:int:suite creator user id
            ret: deleted:datetime:suite deleted datetime
            ret: cases:[int]:suite related cases
        """
        await super(SuitesView, self).get()
        if isinstance(self.ret_data, list):
            for suite in self.ret_data:
                suite['cases'] = await self.__get_suite_cases(suite_id=suite['id'])

        elif isinstance(self.ret_data, dict):
            suite = self.ret_data
            suite['cases'] = await self.__get_suite_cases(suite_id=suite['id'])

        return web.json_response(self.ret_data)

    async def post(self):
        """
            arg: api_key:str:user api key:required

            body: name:str:suite name:required
            body: description:str:suite description

            ret: id:int:suite id
            ret: create_date:datetime:suite creation datetime
            ret: update_date:datetime:suite update datetime
            ret: name:str:suite name
            ret: description:str:suite description
            ret: creator:int:suite creator user id
            ret: deleted:datetime:suite deleted datetime
            ret: cases:[int]:suite related cases
        """
        await super(SuitesView, self).post()
        return web.json_response(self.ret_data, status=201)

    async def put(self):
        """
            arg: id:int:suite id:required
            arg: api_key:str:user api key

            body: name:str:suite name
            body: description:str:suite description

            ret: id:int:suite id
            ret: create_date:datetime:suite creation datetime
            ret: update_date:datetime:suite update datetime
            ret: name:str:suite name
            ret: description:str:suite description
            ret: creator:int:suite creator user id
            ret: deleted:datetime:suite deleted datetime
            ret: cases:[int]:suite related cases
        """
        await super(SuitesView, self).put()
        return web.json_response(self.ret_data, status=200)

    async def delete(self):
        """
            arg: id:int:suite id:required
            arg: api_key:str:user api key:required
        """
        await super(SuitesView, self).delete()
        return web.json_response({}, status=200)
