from datetime import timedelta

# SERVER_URL = 'http://47.115.212.55:5000'
# IMAGE_PATH = '/root/tiktok/static/images/'
# VIDEO_PATH = '/root/tiktok/static/videos/'
# COVER_PATH = '/root/tiktok/static/covers/'

SERVER_URL = 'http://127.0.0.1:5000'
IMAGE_PATH = 'D:\\pyprojects\\tiktok\\static\\images\\'
VIDEO_PATH = 'D:\\pyprojects\\tiktok\\static\\videos\\'
COVER_PATH = 'D:\\pyprojects\\tiktok\\static\\covers\\'

# MYSQL CONFIG
MYSQL_DIALECT = 'mysql'
MYSQL_DRIVER = 'pymysql'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '310257813'
MYSQL_HOSTNAME = '47.115.212.55'
MYSQL_PORT = '3306'
MYSQL_DATABASE = 'tiktok'

# redis 配置
REDIS_HOSTNAME = '47.115.212.55'
REDIS_PORT = 6379
REDIS_PASSWORD = '310257813'
REDIS_DATABASE = 2


class Config(object):
    DEBUG = True

    SECRET_KEY = b'#q)\\x00\xd6\x9f<iBQ\xd7;,\xe2E'
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
        MYSQL_DIALECT, MYSQL_DRIVER, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOSTNAME, MYSQL_PORT, MYSQL_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    JWT_HEADER_NAME = 'Access-Token'
    JWT_SECRET_KEY = b'#q)\\x00\xd6\x9f<iBQ\xd7;,\xe2E'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_RESFRESH_TOKEN_EXPIRES = timedelta(days=30)
