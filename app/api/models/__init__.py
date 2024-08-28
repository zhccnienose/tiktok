from flask_sqlalchemy import SQLAlchemy
from app.config import REDIS_PORT, REDIS_DATABASE, REDIS_HOSTNAME, REDIS_PASSWORD
import redis

host = REDIS_HOSTNAME
port = REDIS_PORT
pwd = REDIS_PASSWORD
d = REDIS_DATABASE

db = SQLAlchemy()
r = redis.StrictRedis(host=host, port=port, password=pwd, db=d)
