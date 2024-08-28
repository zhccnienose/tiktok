from flask import send_from_directory
from flask_restful import Resource
from app.config import IMAGE_PATH


class TestHeadimg(Resource):

    def get(self):
        return send_from_directory(directory=IMAGE_PATH, path="6.jpg")
