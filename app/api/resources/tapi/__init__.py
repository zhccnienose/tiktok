from flask import Blueprint
from flask_restful import Api

from .helloworld import TestHw
from .sql import TestSql
from .red import TestRedis
from .head_img import TestHeadimg

test_bp = Blueprint('test', __name__, url_prefix='/test')
test = Api(test_bp)

test.add_resource(TestHw, '/helloworld')
test.add_resource(TestSql, "/mysql")
test.add_resource(TestRedis, "/redis")
test.add_resource(TestHeadimg, '/images')
