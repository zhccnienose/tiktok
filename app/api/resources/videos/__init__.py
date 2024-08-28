from flask import Blueprint
from flask_restful import Api

from .publish import VideoPublish
from .feed import VideoFeed
from .video_file import VideoFile
from .video_cover import VideoCover
from .list import VideoList
from .search import VideoSearch
from .hot import VideoHot

video_bp = Blueprint('videos', __name__, url_prefix='/video')
video = Api(video_bp)

video.add_resource(VideoPublish, "/publish", methods=['POST'])
video.add_resource(VideoFeed, '/feed/', methods=['GET'])
video.add_resource(VideoList, '/list', methods=['GET'])
video.add_resource(VideoFile, "/files/<video_name>", methods=['GET'])
video.add_resource(VideoCover, "/covers/<video_name>", methods=['GET'])
video.add_resource(VideoSearch, "/search", methods=['POST'])
video.add_resource(VideoHot, "/popular", methods=['GET'])
