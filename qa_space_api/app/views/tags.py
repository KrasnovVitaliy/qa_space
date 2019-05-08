from aiohttp import web
import logging
import db

from config import Config

logger = logging.getLogger(__name__)
config = Config()

from views.base_view import BaseView


class TagsView(BaseView):
    def __init__(self, request):
        """
            description: API tags endpoint
        """
        super(TagsView, self).__init__(request=request)
        self.db_instance = db.Tags
        self.post_required_fields = ['name']
        self.post_available_fields = ['name']
        self.post_unique_fields = ['name']

    async def get(self):
        """
            arg: id:int:tag id:required
            arg: api_key:str:user api key:required

            ret: id:int:tag id
            ret: create_date:datetime:tag creation datetime
            ret: update_date:datetime:tag update datetime
            ret: name:str:tag name
            ret: creator:int:tag creator user id
            ret: deleted:datetime:project deleted datetime
        """
        await super(TagsView, self).get()
        return web.json_response(self.ret_data)

    async def post(self):
        """
            arg: api_key:str:user api key:required

            body: name:str:tag name:required

            ret: id:int:tag id
            ret: create_date:datetime:tag creation datetime
            ret: update_date:datetime:tag update datetime
            ret: name:str:tag name
            ret: creator:int:tag creator user id
            ret: deleted:datetime:project deleted datetime
        """
        await super(TagsView, self).post()
        return web.json_response(self.ret_data, status=201)

    async def put(self):
        """
            arg: id:int:tag id:required
            arg: api_key:str:user api key:required

            body: name:str:tag name

            ret: id:int:tag id
            ret: create_date:datetime:tag creation datetime
            ret: update_date:datetime:tag update datetime
            ret: name:str:tag name
            ret: creator:int:tag creator user id
            ret: deleted:datetime:project deleted datetime
        """

        await super(TagsView, self).put()
        return web.json_response(self.ret_data, status=200)

    async def delete(self):
        """

            arg: api_key:str:user api key:required
        """
        await super(TagsView, self).delete()
        return web.json_response({}, status=200)
