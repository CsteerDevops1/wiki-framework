from flask import Flask
from flask_admin import Admin
from auth_dao import WikiAuthDAO, ROLES, generate_user_token, ROLE_TTL
from dotenv import load_dotenv
import os
from auth_ui_view import BASIC_AUTH, UserView, RoleView, AUTH_DAO


app = Flask(__name__)

# doesn't override any env variables, just set them from .env file if they don't exist
load_dotenv()

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['BASIC_AUTH_USERNAME'] = os.getenv("BASIC_AUTH_USERNAME")
app.config['BASIC_AUTH_PASSWORD'] = os.getenv("BASIC_AUTH_PASSWORD")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

SSL_CERT_PATH = os.getenv("SSL_CERT_PATH")
SSL_KEY_PATH = os.getenv("SSL_KEY_PATH")

BASIC_AUTH.init_app(app)

admin = Admin(app, name='Wiki Auth', template_mode='bootstrap3', url="/api/wiki/auth/admin")
admin.add_view(UserView(AUTH_DAO.users_collection))
admin.add_view(RoleView(AUTH_DAO.roles_collection))

app.run(ssl_context=(SSL_CERT_PATH, SSL_KEY_PATH))