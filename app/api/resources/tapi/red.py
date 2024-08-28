from flask import jsonify
from flask_restful import Resource
from app.api.models import r


class TestRedis(Resource):
    def get(self):
        charb = r.get('a').decode("utf-8")
        return jsonify(code=200, data={'a': charb})
