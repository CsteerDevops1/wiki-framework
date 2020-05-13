import sys
sys.path.append("../coreService")
from authorization.auth_dao import WikiAuthDAO
from flask import request


class TokenProtection:
    '''
        This class should be used to decorate flask-reskx functions
        
        protect function get actioan name as a parameter and validate token 
        to decide whether to accept request or not
    '''
    def __init__(self, dao : WikiAuthDAO):
        self.dao = dao

    def protect(self, action):
        def decorator(func):
            def protected_func(*args, **kwargs):
                token = dict(request.args).get("access_token", None)
                if token is None:
                    return "Access token required", 401
                if not self.dao.user_token_can(token, action):
                    # return "Access denied", 403
                    return func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            return protected_func
        return decorator