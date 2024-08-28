from flask import Blueprint
from flask_restful import Api

from .actions import LikeActions
from .list import LikeList

like_bp = Blueprint('likes', __name__, url_prefix='/like')
like = Api(like_bp)

like.add_resource(LikeActions, '/action', methods=['POST'])
like.add_resource(LikeList, '/list', methods=['GET'])
