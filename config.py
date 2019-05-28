import redis
import pymysql
import logging
from DBUtils.PooledDB import PooledDB, SharedDBConnection


class Config(object):
    DEBUG = True
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    SECRET_KEY = 'q7pBNcWPgmF6BqB6b5VICF7z7pI+90o0O4CaJsFGjzRsYiya9SEgUDytXvzFsIaR'

    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True

    # PERMANENT_SESSION_LIFETIME = 31
    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_REFRESH_EACH_REQUEST = True

    JSON_AS_ASCII = False
    JSON_SORT_KEYS = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    JSONIFY_MIMETYPE = 'application/json'

    POOL = PooledDB(
        creator=pymysql,
        maxconnections=10,
        mincached=2,
        maxcached=6,
        maxshared=3,
        blocking=True,
        maxusage=None,
        setsession=[],
        ping=0,
        host='127.0.0.1',
        port=3306,
        user='bk',
        password='123456',
        database='backstore',
        charset='utf8'
    )


class Development(Config):
    """开发环境"""
    LOGGING_LEVEL = logging.DEBUG


class Production(Config):
    """生产环境"""
    LOGGING_LEVEL = logging.INFO


configs = {
    "dev": Development,
    "pro": Production
}
