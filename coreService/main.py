from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from api_app import app as api_application, HOST, PORT
from auth_app import app as auth_application
from werkzeug.serving import run_simple

middleware = DispatcherMiddleware(api_application, {
    '/api/wiki/auth': auth_application,
})

# not recommended for production
run_simple(HOST, int(PORT), middleware)