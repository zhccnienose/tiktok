from flask import send_from_directory
from flask_restful import Resource
from app.config import VIDEO_PATH


# 返回视频文件
class VideoFile(Resource):
    def get(self, video_name):
        return send_from_directory(VIDEO_PATH, video_name)
