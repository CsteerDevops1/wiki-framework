from flask import Flask, Response, redirect
from flask_admin import Admin
from pymongo import MongoClient
from flask_admin.contrib.pymongo import ModelView
from wtforms.form import Form
from wtforms.fields import TextField, DateField, SelectField, FieldList, StringField
from flask_admin.form import Select2Widget
from werkzeug.exceptions import HTTPException
from flask_basicauth import BasicAuth
from pymongo.errors import CollectionInvalid
from flask_admin.model.fields import InlineFormField, InlineFieldList
from bson.objectid import ObjectId

import secrets

app = Flask(__name__)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
app.config['SECRET_KEY'] = '123456790'

basic_auth = BasicAuth(app)
client = MongoClient("mongodb://localhost:27017")

def get_user_collection(client):
    db = client["wikiDB"]
    try:
        db.create_collection("wiki_users_collection")
        collection = db.wiki_users_collection
    except CollectionInvalid: # means that collection exists
        collection = db.wiki_users_collection
    return collection

def get_roles_collection(client):
    db = client["wikiDB"]
    try:
        db.create_collection("wiki_roles_collection")
        collection = db.wiki_roles_collection
    except CollectionInvalid: # means that collection exists
        collection = db.wiki_roles_collection
    return collection

def set_user_role(user_id, role):
    if user_id is None or role is None:
        print("set_user_roels() called with None")
        return
    global client
    user_col = get_user_collection(client)
    print("Updated : ", end="")
    print(user_col.update_many(update={"$set" : { "role" : role }}, filter={"_id" : ObjectId(user_id)}).modified_count)

def delete_user_roles(user_id):
    global client
    roles_col = get_roles_collection(client)
    print("Deleted : ", end="")
    print(roles_col.delete_many({"user_id" : str(user_id)}).deleted_count)



class AuthException(HTTPException):
    def __init__(self, message):
        super(AuthException, self).__init__(message, Response(
            message, 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

class ProtectedModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated. Refresh the page.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

class UserForm(Form):
    access_token = StringField('access_token')
    mail = StringField('mail', default="")
    tg_login = StringField('tg_login', default="")
    auth_methods_submitted = InlineFieldList(StringField("auth_method"))
    role = StringField("role", default="")

class UserView(ProtectedModelView):
    column_list = ('access_token', 'mail', 'auth_methods_submitted', 'tg_login', 'role', "_id")
    form = UserForm
    column_searchable_list = ['tg_login', 'mail', 'role']
    # column_filters = ['role']
    # column_editable_list = ['mail', 'auth_methods_submitted', 'tg_login']
    form_widget_args = {
        'access_token':{
            'disabled':True
        },
        'role':{
            'disabled':True
        },
        '_id':{
            'disabled':True
        },
    }

    def create_form(self, obj=None):
        form = ProtectedModelView.create_form(self, obj=obj)
        if form.access_token.data is not None and form.access_token.data == "":
            form.access_token.data = secrets.token_hex(16)
        return form

    def after_model_delete(self, model):
        delete_user_roles(model["_id"])


def get_user_choices():
    global client
    user_col = get_user_collection(client)
    res = user_col.find(filter={"role" : ""}, projection=["mail", "_id", "tg_login"])
    res = [(x["_id"], x["mail"] if x["mail"] != "" else x["tg_login"] ) for x in res]
    return res


class RoleForm(Form):
    role = StringField("role")
    user_id = SelectField('user_id', widget=Select2Widget(), validate_choice=False)
    expiration_date = StringField("expiration_date")

class RoleView(ProtectedModelView):
    column_list = ('role', 'user_id', 'expiration_date')
    form = RoleForm
    

    def edit_form(self, obj):
        form = ProtectedModelView.edit_form(self, obj)
        set_user_role(form.user_id.data, form.role.data)
        form.user_id.choices = get_user_choices()
        return form

    def create_form(self, obj=None):
        form = ProtectedModelView.create_form(self, obj=obj)
        set_user_role(form.user_id.data, form.role.data)
        form.user_id.choices = get_user_choices()
        return form

    def after_model_delete(self, model):
        set_user_role(model["user_id"], "")

    



admin = Admin(app, name='Wiki Auth', template_mode='bootstrap3', url="/api/wiki/auth/admin")
admin.add_view(UserView(get_user_collection(client)))
admin.add_view(RoleView(get_roles_collection(client)))


app.run(ssl_context=('/home/mikhail/cloud_steering_projects/fullchain.pem', '/home/mikhail/cloud_steering_projects/privkey.pem'))