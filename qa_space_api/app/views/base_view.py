from aiohttp import web
import logging
import requests
import json
import db
import datetime
from config import Config

logger = logging.getLogger(__name__)
config = Config()


class BaseView(web.View):
    def __init__(self, request):
        super(BaseView, self).__init__(request=request)

        self.user_data = None
        self.post_required_fields = []
        self.post_available_fields = []
        self.post_unique_fields = []
        self.db_instance = None

    def __check_user_data(self):
        get_params = self.request.rel_url.query
        if 'api_key' not in get_params:
            return web.json_response({"error": "No API key specified"}, status=400)
        logger.debug("Getting projects with params: {}".format(get_params))
        uuid = get_params['api_key']

        rsp = requests.get("{}/api_token?uuid={}".format(config.AUTH_SERVICE_ADDRESS, uuid))
        if rsp.status_code != 200:
            logger.error("Auth response is {} expected 200. Error: {}".format(rsp.status_code, rsp.text))
            return web.json_response({"error": "Not found"}, status=404)
        user_data = rsp.json()
        return user_data

    async def __process_get_id_request(self, object_id):
        filters = {
            'creator': self.user_data['id'],
            'deleted': None,
            'id': object_id
        }
        db_object = db.session.query(self.db_instance).filter_by(**filters).first()
        # db_object = db.session.query(self.db_instance) \
        #     .filter(db.Projects.creator == self.user_data['id']) \
        #     .filter(db.Projects.deleted == None) \
        #     .filter(db.Projects.id == object_id) \
        #     .first()

        return db_object

    async def __process_get_list_request(self):
        filters = {
            'creator': self.user_data['id'],
            'deleted': None,
        }
        db_object = db.session.query(self.db_instance).filter_by(**filters).all()

        # db_object = db.session.query(self.db_instance) \
        #     .filter(db.Projects.creator == self.user_data['id']) \
        #     .filter(db.Projects.deleted == None) \
        #     .all()

        return db_object

    async def get(self):
        self.user_data = self.__check_user_data()

        get_params = self.request.rel_url.query
        if 'id' in get_params:
            db_object = await self.__process_get_id_request(object_id=get_params['id'])
            if not db_object:
                raise web.HTTPNotFound()
            self.ret_data = db_object.to_json()

        else:
            self.ret_data = []
            db_objects = await self.__process_get_list_request()
            for db_object in db_objects:
                self.ret_data.append(db_object.to_json())

    def __check_required_post_fields(self):
        for item in self.post_required_fields:
            if item not in self.data:
                rsp_data = {
                    "error": "Field {} not specified in request data".format(item)
                }
                raise web.HTTPBadRequest(text=json.dumps(rsp_data))

            if not self.data[item]:
                rsp_data = {
                    "error": "Field {} can not be empty".format(item)
                }
                raise web.HTTPBadRequest(text=json.dumps(rsp_data))

    def __check_unique_fields(self):
        filters = {}
        for field in self.post_unique_fields:
            filters[field] = self.data[field]

        db_objects = db.session.query(self.db_instance).filter_by(**filters).count()
        if db_objects > 0:
            rsp_data = {"error": "Such object already exists"}
            raise web.HTTPBadRequest(text=json.dumps(rsp_data))

    async def post(self):
        self.user_data = self.__check_user_data()
        self.data = await self.request.json()
        logger.debug("Received request data: {}".format(self.data))

        self.__check_required_post_fields()
        self.__check_unique_fields()

        db_object = self.db_instance()
        for field in self.post_available_fields:
            if field in self.data:
                setattr(db_object, field, self.data[field])
        db_object.creator = self.user_data['id']

        db.session.add(db_object)
        db.session.commit()

        self.ret_data = db_object.to_json()

    async def put(self):
        self.user_data = self.__check_user_data()
        get_params = self.request.rel_url.query
        if 'id' not in get_params:
            rsp_data = {'error': 'Id must be specified in request'}
            raise web.HTTPBadRequest(text=json.dumps(rsp_data))

        self.data = await self.request.json()

        db_object = await self.__process_get_id_request(object_id=get_params['id'])
        if not db_object:
            raise web.HTTPNotFound()

        for field in self.post_available_fields:
            if field in self.data:
                setattr(db_object, field, self.data[field])

        db.session.add(db_object)
        db.session.commit()

        self.ret_data = db_object.to_json()

    async def delete(self):
        self.user_data = self.__check_user_data()
        get_params = self.request.rel_url.query
        if 'id' not in get_params:
            rsp_data = {'error': 'Id must be specified in request'}
            raise web.HTTPBadRequest(text=json.dumps(rsp_data))

        db_object = await self.__process_get_id_request(object_id=get_params['id'])
        if not db_object:
            raise web.HTTPNotFound()

        db_object.deleted = datetime.datetime.now()
        db.session.commit()
