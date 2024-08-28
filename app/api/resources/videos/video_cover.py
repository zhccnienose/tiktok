from flask import send_from_directory
from flask_restful import Resource
from app.config import COVER_PATH


class VideoCover(Resource):
    def get(self, video_name):
        return send_from_directory(COVER_PATH, video_name)
