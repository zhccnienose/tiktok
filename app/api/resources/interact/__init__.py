from flask import Blueprint
from flask_restful import Api

from .follow import Follow
from .follow_list import FollowList
from .fan_list import FanList

interact_bp = Blueprint('interact', __name__, url_prefix='/')
interact = Api(interact_bp)

interact.add_resource(Follow, '/relation/action', methods=['POST'])
interact.add_resource(FollowList, '/following/list', methods=['GET'])
interact.add_resource(FanList, '/follower/list', methods=['GET'])
