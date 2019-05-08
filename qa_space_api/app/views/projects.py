from aiohttp import web
import logging
import db

from config import Config

logger = logging.getLogger(__name__)
config = Config()

from views.base_view import BaseView


class ProjectsView(BaseView):
    """
    description: API project endpoint
    """

    def __init__(self, request):
        super(ProjectsView, self).__init__(request=request)
        self.db_instance = db.Projects
        self.post_required_fields = ['name']
        self.post_available_fields = ['name', 'description']
        self.post_unique_fields = ['name']

    async def __get_project_suites(self, project_id):
        suites = db.session.query(db.Suites) \
            .filter(db.Suites.creator == self.user_data['id']) \
            .filter(db.Suites.project == project_id) \
            .filter(db.Suites.deleted == None) \
            .all()

        suites_data = []
        for suite in suites:
            suites_data.append(suite.id)

        return suites_data

    async def get(self):
        """
            arg: id:int:project id:required
            arg: api_key:str:user api key:required

            ret: id:int:project id
            ret: create_date:datetime:project creation datetime
            ret: update_date:datetime:project update datetime
            ret: name:str:project name
            ret: description:str:project description
            ret: creator:int:project creator user id
            ret: deleted:datetime:project deleted datetime
            ret: suites:[int]:project related suites
        """
        await super(ProjectsView, self).get()
        if isinstance(self.ret_data, list):
            for project in self.ret_data:
                project['suites'] = await self.__get_project_suites(project_id=project['id'])

        elif isinstance(self.ret_data, dict):
            project = self.ret_data
            project['suites'] = await  self.__get_project_suites(project_id=project['id'])

        return web.json_response(self.ret_data)

    async def post(self):
        """
            arg: api_key:str:user api key:required

            body: name:str:project name:required
            body: description:str:project description

            ret: id:int:project id
            ret: create_date:datetime:project creation datetime
            ret: update_date:datetime:project update datetime
            ret: name:str:project name
            ret: description:str:project description
            ret: creator:int:project creator user id
            ret: deleted:datetime:project deleted datetime
            ret: suites:[int]:project related suites
        """

        await super(ProjectsView, self).post()
        return web.json_response(self.ret_data, status=201)

    async def put(self):
        """
            arg: id:int:project id:required
            arg: api_key:str:user api key:required

            body: name:str:project name
            body: description:str:project description

            ret: id:int:project id
            ret: create_date:datetime:project creation datetime
            ret: update_date:datetime:project update datetime
            ret: name:str:project name
            ret: description:str:project description
            ret: creator:int:project creator user id
            ret: deleted:datetime:project deleted datetime
            ret: suites:[int]:project related suites
        """

        await super(ProjectsView, self).put()
        return web.json_response(self.ret_data, status=200)

    async def delete(self):
        """
            arg: id:int:project id:required
            arg: api_key:str:user api key
        """

        await super(ProjectsView, self).delete()
        return web.json_response({}, status=200)
