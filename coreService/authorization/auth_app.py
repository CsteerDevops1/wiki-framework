from flask import Flask, request, url_for
from flask_restx import Api, Resource
from flask_admin import Admin
from auth_dao import WikiAuthDAO, ROLES, generate_user_token, ROLE_TTL
from dotenv import load_dotenv
import os
from auth_ui_view import BASIC_AUTH, UserView, RoleView, AUTH_DAO


class CustomAPI(Api): # this method should be overrided to make it work behind reverse proxy
    @property
    def specs_url(self):
        '''
        The Swagger specifications absolute url (ie. `swagger.json`)

        :rtype: str
        '''
        return url_for(self.endpoint('specs'), _external=False)


app = Flask(__name__)

# doesn't override any env v ariables, just set them from .env file if they don't exist
load_dotenv()

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['BASIC_AUTH_USERNAME'] = os.getenv("BASIC_AUTH_USERNAME")
app.config['BASIC_AUTH_PASSWORD'] = os.getenv("BASIC_AUTH_PASSWORD")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

BASIC_AUTH.init_app(app)

admin = Admin(app, name='Wiki Auth', template_mode='bootstrap3', url="/admin")
admin.add_view(UserView(AUTH_DAO.users_collection))
admin.add_view(RoleView(AUTH_DAO.roles_collection))

api = CustomAPI(app, version='1.0', title='Wiki authorization API', doc="/doc")
api = api.namespace("Wiki auth", description="Send mail or tg_login in params. New user will be created/updated and returned.", path="/")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@api.route('/login')
class WikiAuth(Resource):
    @api.doc(params={"mail" : "User mail", "tg_login" : "User telegram login"})
    @api.param('mail', _in="query", description="User mail for auth")
    def get(self): # too much logic in here tbh
        params = dict(request.args)
        filter = {}
        filter["mail"] = params.get("mail", None)
        filter["tg_login"] = params.get("tg_login", None)
        if filter["mail"] is None and filter["tg_login"] is None:
            return "You should pass mail/tg_login to params", 400
        AUTH_DAO.check_user_roles_ttl()
        user = AUTH_DAO.users.get({**filter}) # filter can change in place
        if len(user) > 1: # iternal error
            return "Multiple users found", 400
        elif len(user) == 0: # create if user doesn't exist or update
            if filter["mail"] is not None:
                user_t = AUTH_DAO.users.get({"mail" : filter["mail"]})
                if len(user_t) != 0: # tg_login was set in params, but it is not in db
                    user_t = user_t[0]
                    AUTH_DAO.users.update({'$push': {'auth_methods_submitted': "telegram"}}, {"_id" : user_t["_id"]})
                    AUTH_DAO.users.update({'$set': {'tg_login': filter["tg_login"]}}, {"_id" : user_t["_id"]})
                    return AUTH_DAO.users.get({"mail" : filter["mail"]})[0], 200
            if filter["tg_login"] is not None:
                user_t = AUTH_DAO.users.get({"tg_login" : filter["tg_login"]})
                if len(user_t) != 0: # mail was set in params, but it is not in db
                    user_t = user_t[0]
                    AUTH_DAO.users.update({'$push': {'auth_methods_submitted': filter["mail"][filter["mail"].find("@")+1:]}}, {"_id" : user_t["_id"]})
                    AUTH_DAO.users.update({'$set': {'mail': filter["mail"]}}, {"_id" : user_t["_id"]})
                    return AUTH_DAO.users.get({"tg_login" : filter["tg_login"]})[0], 200
            auth_m = params.get("mail", "").find("@")
            if auth_m != -1:
                auth_m = filter["mail"][auth_m+1:]
                filter["auth_methods_submitted"] = [auth_m]
            if filter.get("tg_login", None) is not None:
                filter["auth_methods_submitted"] = filter.get("auth_methods_submitted", []) + ["telegram"]
            user = AUTH_DAO.create_user(filter)
            AUTH_DAO.create_role("USER", user["_id"]) # default role
            del user["_id"]
            user["role"] = "USER" # update role field, because role was created after user
            return user, 200
        else: # return user info if exist
            user = user[0]
            del user["_id"]
            return user, 200
        

if __name__ == "__main__":
    SSL_CERT_PATH = os.getenv("SSL_CERT_PATH")
    SSL_KEY_PATH = os.getenv("SSL_KEY_PATH")
    app.run(ssl_context=(SSL_CERT_PATH, SSL_KEY_PATH))