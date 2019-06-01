# 实例化本地文件
import redis
from flask import Flask
from flask_session import Session
from config import configs
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS


# 设置mysql连接对象
db = SQLAlchemy()
# 定义全局redis_store
redis_store = None


def setUpLogging(level):
    "根据开发环境配置日志等级"

    # 设置日志等级
    logging.basicConfig(level=level)
    # 创建日志记录器, 指定日志保存路径,每个文件大小
    file_log_handler = RotatingFileHandler("log/backstore.log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 日志记录格式
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    file_log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_handler)


def get_app(config_name):
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(configs[config_name])

    # 开始session
    Session(app)

    # 创建连接到redis数据库连接对象
    global redis_store
    redis_store = redis.StrictRedis(host=configs[config_name].REDIS_HOST, port=configs[config_name].REDIS_PORT)

    from backstage.api_1_0 import api
    app.register_blueprint(api)

    # 初始化日志设置
    setUpLogging(level=configs[config_name].LOGGING_LEVEL)

    print(app.url_map)

    # 设置跨域
    CORS(app, supports_credentials=True)

    return app
