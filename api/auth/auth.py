from functools import wraps
from base64 import b64decode
from flask import request, g
from hashlib import md5
from db.dao import Session, User




class BasicAuthHandler():

    def __init__(self):
        pass

    def registerUserHandler(self, f):
        self.getUserInfoFromdb = f
        def inner(username):
            f(username)
        return inner
        

    def require_authentication(self, role=None):
        def inner(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                value = request.headers['Authorization'].encode('utf-8')
                scheme, credentials = value.split(b' ', 1)
                username, password = b64decode(credentials).split(b':', 1)
                digest = md5(password).hexdigest()
                password, roles = self.getUserInfoFromdb(username)
                if password is not None and password == digest:
                    if role is None or role in roles:
                        g.authtoken = credentials
                        g.name = username
                        return func(*args, **kwargs)
                    else:
                        return '', 403
                else:
                    return '', 401
            return wrapper
        return inner



    