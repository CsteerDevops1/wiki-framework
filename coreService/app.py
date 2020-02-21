import os
import db_api
from db_api import WikiPageDAO, SCHEMA_PATH
from flask import Flask, request
from flask_restx import Api, Resource, fields, reqparse
from dotenv import load_dotenv
import json
from datetime import datetime


# doesn't override any env variables, just set them from .env file if they don't exist
load_dotenv()
HOST = os.getenv('FLASK_HOST')
PORT = os.getenv('FLASK_PORT')
app = Flask(__name__)
app.config['ENV'] = os.getenv('FLASK_ENV')
api = Api(app)
DAO = WikiPageDAO() # a data access object which provides interface to database


with open(SCHEMA_PATH, 'r') as schema_file:
    s = schema_file.read()
    schema = json.loads(s)
schema_model = api.schema_model('model', schema['$jsonSchema']) # used for validation


query_params = {'_id' : "Object id",
                'name': "Name of stored object.",
                'creation_date': 'The date of creation object in ISO format.',}


@api.route('/api/wiki')
class WikiPage(Resource):
    @api.doc(params=query_params,
             description="Query params are used for filter.")
    @api.param('X-Fields', _in="header", description="Header to specify returning fields in csv.")
    def get(self):
        projection = [x.strip() for x in request.headers.get('X-Fields').split(",")]
        resp = DAO.get(dict(request.args), projection)
        return resp


    @api.doc(params=query_params,
             description="Query params are used for filter. This request is\
                          only SETTING NEW VALUES. Returns amount of updated objects.")
    @api.expect(schema_model)
    def put(self):
        new_data = db_api.set_modification(dict(api.payload))
        filter = dict(request.args)
        updated = DAO.update(new_data, filter)
        return updated, 200

    
    @api.expect(schema_model, validate=True)
    def post(self):
        data = dict(api.payload)
        resp = DAO.create(data)
        if resp is None:
            return "Document didn't created", 500
        else:
            return resp, 201

    @api.doc(params=query_params,
             description="Query params are used for filter. Returns amount of deleted objects.")
    def delete(self):
        filter = dict(request.args)
        deleted = DAO.delete(filter)
        return deleted, 200

app.run(HOST, PORT)
