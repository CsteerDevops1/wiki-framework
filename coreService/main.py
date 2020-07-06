import sys
sys.path.append("../coreService")
sys.path.append("../coreService/wiki_api")
sys.path.append("../coreService/authorization")
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from wiki_api.api_app import app as api_application, HOST, PORT
from authorization.auth_app import app as auth_application
from werkzeug.serving import run_simple
from werkzeug.contrib.fixers import ProxyFix


middleware = DispatcherMiddleware(api_application, {
    '/api/wiki/auth': auth_application,
})

middleware = ProxyFix(middleware)

# not recommended for production
run_simple(HOST, int(PORT), middleware)