from flask_restful import Resource


class TestHw(Resource):

    def get(self):
        return "hello world"
