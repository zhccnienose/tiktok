from flask import send_file
from flask_restful import Resource
from app.config import IMAGE_PATH


class UserAvatar(Resource):

    def get(self, img_name):
        return send_file(IMAGE_PATH + img_name)
