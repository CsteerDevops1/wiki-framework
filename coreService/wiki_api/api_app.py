import os
import sys
sys.path.append("../coreService")
import api_dao
from api_dao import WikiPageDAO, SCHEMA_PATH
from autosuggest import get_possible_typos
import flask
from flask import Flask, request, url_for
from flask_restx import Api, Resource, fields, reqparse, abort
from dotenv import load_dotenv
import json
from datetime import datetime
from authorization.auth_dao import WikiAuthDAO
from token_protection import TokenProtection


class CustomAPI(Api): # this method should be overrided to make it work behind reverse proxy
    @property
    def specs_url(self):
        '''
        The Swagger specifications absolute url (ie. `swagger.json`)

        :rtype: str
        '''
        return url_for(self.endpoint('specs'), _external=False)


# ---------------------------- SETUP SECTION ------------------------------------------------------------------------
# doesn't override any env variables, just set them from .env file if they don't exist
load_dotenv()
HOST = os.getenv('FLASK_HOST')
PORT = os.getenv('FLASK_PORT')
app = Flask(__name__)
app.config['ENV'] = os.getenv('FLASK_ENV')
api = CustomAPI(app, version='1.0', title='Wiki page API', description='REST API to mongodb', doc="/api/wiki/doc/")
api = api.namespace("Wiki page", description='Stored content for wiki project', path="/") # swagger ui representation
DAO = WikiPageDAO() # a data access object which provides interface to database
auth_protect = TokenProtection(WikiAuthDAO())


with open(SCHEMA_PATH, 'r') as schema_file:
    s = schema_file.read()
    schema = json.loads(s)
schema_model = api.schema_model('model', schema['$jsonSchema']) # used for validation


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# parametres which you should use in filters
query_params = {'_id' : "Object id",
                'label' : 'Stable/Unstable label of stored object.',
                'name': "Name of stored object.",
                'russian_name': "Russian translation for name property.",
                'creation_date': 'The date of creation object in ISO format.',
                'description': 'English description of word, better use it with regex on.',
                'regex': 'Boolean, determines whether to use regular expressions in search query,\
                        can be True or False, default False. Search is case insensitive. Wrong patterns are ignored.',\
                'access_token': 'User\'s access token, This param is required for PUT, DELETE, POST methods.'}

def str_to_bool(s : str) -> bool:
    '''cast string representation to bool type'''
    if s is None: return False 
    return s.lower() in ["true", "1", "yes", "y"]

# ---------------------------- SETUP SECTION ------------------------------------------------------------------------


@api.route('/api/wiki')
class WikiPage(Resource):
    @api.doc(params=query_params,
             description="Query params are used for filter.")
    @api.param('X-Fields', _in="header", description="Header to specify returning fields in csv.")
    @api.response(200, 'Success')
    @api.doc(params={'limit' : 'Maximum amount of objects to be returned'})
    def get(self):
        # extract all the given params in request
        if request.headers.get('X-Fields') is not None:
            projection = [x.strip() for x in request.headers.get('X-Fields').split(",")]
        else:
            projection = None
        filter = dict(request.args)
        if "access_token" in filter:
            del filter["access_token"]

        # set regex search flag
        regex_flag = filter.get("regex", False)
        if regex_flag is not False: # cast string representation to bool type
            regex_flag = str_to_bool(regex_flag)
            del filter["regex"]

        resp = DAO.get(filter, projection, regex_flag)
        return resp


    @api.doc(params=query_params,
             description="Query params are used for filter. This request is\
                          only SETTING NEW VALUES. Returns amount of updated objects.")
    @api.expect(schema_model)
    @api.response(200, 'Success')
    @api.doc(params={'mod' : 'Mod which should be used in mongodb update query. Default is "$set"'})
    @auth_protect.protect(action="edit")
    def put(self):
        payload = dict(api.payload)
        if 'label' in payload:
            del payload["label"] # you can't set label value via this resource
        filter = dict(request.args)  
        mod = filter.pop('mod', '$set')
        new_data = api_dao.set_modification(payload, mod)
        del filter["access_token"]
        filter["label"] = "Unstable" # you can only modify Unstable objects
        updated = DAO.update(new_data, filter)
        return updated, 200


    @api.doc(params={'access_token': 'User\'s access token, This param is required for PUT, DELETE, POST methods.'},\
             description="Data in attachments should be encoded in base64, max document size in database is ~10.8Mb")
    @api.expect(schema_model, validate=True)
    @api.response(201, 'Success')
    @api.response(500, 'Document didn\'t created, internal error')
    @api.response(400, 'Document failed validation')
    @auth_protect.protect(action="create")
    def post(self):
        data = dict(api.payload)
        if 'label' not in data: # default label for new objects
            data['label'] = "Unstable"
        resp = DAO.create(data)
        if resp is None:
            return "Document didn't created", 500
        else:
            return resp, 201

    @api.doc(params=query_params,
             description="Query params are used for filter. Returns amount of deleted objects.")
    @api.response(200, 'Success')
    @auth_protect.protect(action="delete")
    def delete(self):
        filter = dict(request.args)
        del filter["access_token"]
        if len(filter.keys()) == 0:
            return "Attempt to DELETE without params.", 400
        deleted = DAO.delete(filter)
        return deleted, 200


@api.route('/api/wiki/autosuggest')
class Autosuggest(Resource):
    @api.doc(params={"data" : "Word or part of a word which should be completed or corrected. Used for 'name' field in db.",
                     "complete" : "Bool, set it to True if you need to autocomplete the word.",
                     "correct" : "Bool, set it to True if you need to correct possible typos in the word."},
             description="This request should be used for fuzzy search in db. Returns json with 'completed'\
                          or 'corrected' or both fields (see params) and arrays of found objects.")
    @api.param('X-Fields', _in="header", description="Header to specify returning fields in csv.")
    @api.response(200, 'Success')
    @api.response(400, 'Wrond querry params')
    def get(self):
        # extract all the given params in request
        if request.headers.get('X-Fields') is not None:
            projection = [x.strip() for x in request.headers.get('X-Fields').split(",")]
        else:
            projection = None
        data = request.args.get("data", None)
        if data is None:
            abort(400)
        data = get_possible_typos(data) # generate regex pattern to correct input data
        resp = {"corrected" : "not requested", "completed" : "not requested"}
        if str_to_bool(request.args.get("complete", None)):
            resp["completed"] = DAO.get({"name" : f"^{data}"}, projection, True)
        if str_to_bool(request.args.get("correct", None)):
            resp["corrected"] = DAO.get({"name" : fr"^{data}\b"}, projection, True)
        return resp


label_filed = api.model('PageLabel', {
    'label': fields.String,
})

@api.route('/api/wiki/page_label')
class PageLabel(Resource):
    @api.doc(params=query_params,
             description="Query params are used for filter. This request is\
                          only SETTING NEW VALUES. Returns amount of updated objects.")
    @api.expect(label_filed, validate=True)
    @api.response(200, 'Success')
    @auth_protect.protect(action="set_label")
    def put(self):
        new_data = api_dao.set_modification({'label': api.payload['label']})
        filter = dict(request.args)
        del filter["access_token"]
        updated = DAO.update(new_data, filter)
        return updated, 200


if __name__ == "__main__":
    app.run(HOST, PORT)
