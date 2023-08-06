import json

from functools import wraps
from flask import request, g
from flask_douwa import redis, Douwa
from flask_douwa import reqparse

TOKEN_PREFIX = "douwa:token:"
TOKEN_EXPIRES = 3600
TOKEN_EXPIRES2 = 3600 * 12 * 30
PERMISSION_PREFIX = "duowa:permission:"


def authorization(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        prefix = TOKEN_PREFIX
        ttl = TOKEN_EXPIRES

        user = None
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization')[7:]
        else:
            parserd = reqparse.RequestParser()
            parserd.add_argument('access_token', "token", type=str,  location='args')
            urlargs = parserd.parse_args()
            if "access_token" in urlargs:
                token = urlargs["access_token"]
            else:
                token = None

        if token:
            key = prefix + token
            user_cached = redis.get(key)
            if user_cached:
                try:
                    user = json.loads(user_cached)
                except Exception as e:
                    user = None
                    raise Exception(e)
        if not user:
            error_str = "用户没有登录!"
            reqparse.abort(401, message=error_str)
        if token not in Douwa.client_access:
            expired = redis.ttl(key)
            if expired:
                redis.expire(key, ttl)
        else:
            redis.expire(key, TOKEN_EXPIRES2)

        g.user = user
        return f(*args, **kwargs)

    return decorated_function


def permission(name):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            userrole = set(g.user["roles"])
            key = PERMISSION_PREFIX + name
            dd = redis.smembers(key)
            if userrole & dd:
                return func(*args, **kwargs)
            else:
                error_str = "没有操作权限!"
                reqparse.abort(401, message=error_str)
        return inner
    return wrapper


def error(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            data = f(*args, **kwargs)
            return data
        except Exception as e:
            if hasattr(e, "data"):
                return json.dumps(e.data, ensure_ascii=False)
            else:
                raise e
    return decorated_function
