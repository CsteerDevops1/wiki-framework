from auth_dao import WikiAuthDAO, ROLES, generate_user_token, ROLE_TTL
from flask import Response, redirect
from wtforms.form import Form
from wtforms.fields import TextField, DateField, SelectField, FieldList, StringField
from flask_admin.form import Select2Widget
from werkzeug.exceptions import HTTPException
from flask_basicauth import BasicAuth
from flask_admin.model.fields import InlineFormField, InlineFieldList
from datetime import datetime
from flask_admin.contrib.pymongo import ModelView


BASIC_AUTH = BasicAuth()
AUTH_DAO = WikiAuthDAO()


class AuthException(HTTPException):
    def __init__(self, message):
        super(AuthException, self).__init__(message, Response(
            message, 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))


class ProtectedModelView(ModelView):
    def is_accessible(self):
        if not BASIC_AUTH.authenticate():
            raise AuthException('Not authenticated. Refresh the page.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(BASIC_AUTH.challenge())


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
            form.access_token.data = generate_user_token()
        return form

    def action_form(self, obj=None):
        form = ProtectedModelView.action_form(self, obj=obj)
        AUTH_DAO.check_user_roles_ttl()
        return form

    def after_model_delete(self, model):
        AUTH_DAO.roles.delete({"user_id": str(model["_id"])})


class RoleForm(Form):
    role = SelectField("role", widget=Select2Widget(), choices=[(x, x) for x in ROLES])
    user_id = SelectField('user_id', widget=Select2Widget(), validate_choice=False)
    creation_date = DateField(label="creation_date")


class RoleView(ProtectedModelView):
    column_list = ('role', 'user_id', 'creation_date')
    form = RoleForm

    form_widget_args = {
        'creation_date':{
            'disabled':True
        },
    }
    
    action_disallowed_list = ['delete']


    def edit_form(self, obj):
        form = ProtectedModelView.edit_form(self, obj)
        AUTH_DAO.set_user_role(form.role.data, form.user_id.data)
        return form

    def create_form(self, obj=None):
        form = ProtectedModelView.create_form(self, obj=obj)
        AUTH_DAO.set_user_role(form.role.data, form.user_id.data)
        form.user_id.choices = AUTH_DAO.get_noroles_user_choices()
        form.creation_date.data = datetime.utcnow()
        return form

    def after_model_delete(self, model):
        print(AUTH_DAO.remove_role(str(model["user_id"])))
