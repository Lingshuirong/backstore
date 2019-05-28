import redis


class Config(object):
    DEBUG = True
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    SECRET_KEY = 'q7pBNcWPgmF6BqB6b5VICF7z7pI+90o0O4CaJsFGjzRsYiya9SEgUDytXvzFsIaR'

    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True

    PERMANENT_SESSION_LIFETIME = 31
    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_REFRESH_EACH_REQUEST = True

    JSON_AS_ASCII = False
    JSON_SORT_KEYS = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    JSONIFY_MIMETYPE = 'application/json'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bk:123456@127.0.0.1:6379/backstore'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    """开发环境"""
    pass


class Production(Config):
    """生产环境"""
    pass


configs = {
    "dev": Development,
    "pro": Production
}
