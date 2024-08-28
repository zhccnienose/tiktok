from flask import Blueprint
from flask_restful import Api

from .action import FirendAction
from .list import FriendList

friend_bp = Blueprint('friend', __name__, url_prefix='/friends')
friend = Api(friend_bp)

friend.add_resource(FirendAction, '/action', methods=['POST'])
friend.add_resource(FriendList, '/list', methods=['GET'])
